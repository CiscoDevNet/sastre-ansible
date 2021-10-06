#! /usr/bin/env python3
from typing import NamedTuple
from cisco_sdwan.base.rest_api import Rest, RestAPIException
from cisco_sdwan.base.models_vmanage import Device
from cisco_sdwan.tasks.common import regex_search
from ansible.errors import AnsibleLookupError, AnsibleOptionsError
from ansible.utils.display import Display
from ansible.plugins.lookup import LookupBase

DOCUMENTATION = """
lookup: devices
version_added: "1.0"
short_description: Fetches list of SD-WAN devices from vManage
description:
    - This lookup returns list of SD-WAN devices from vManage with multiple filter options.
    - When more than one filter condition is defined match is an 'and' of all conditions.
    - When no filter is defined all devices are returned.
options:
    _terms:
        description: base url to connect to SD-WAN vmanage
        required: True
        type: list
    device_type:
        description: >
            Match on device type to include. 
            Supported values are 'vmanage', 'vsmart', 'vbond', 'vedge', 'cedge'
        required: False
        type: str
    regex:
        description: >
            Regular expression matching on the device name to include.
        required: False
        type: str
    not_regex:
        description: >
            Regular expression matching on the device name to not include.
        required: False
        type: str
    reachable:
        description: >
            When set to true, only include devices in reachable state.
        required: False
        type: bool
    site:
        description: >
            Include devices matching this site id.
        required: False
        type: str
    system_ip:
        description: >
            Include devices matching this system ip.
        required: False
        type: str
    timeout_secs:
        description: REST API timeout value in seconds
        required: False
        Default: 120
        type: int
"""
EXAMPLES = """
    - name: Fetch devices for vedge device type
      ansible.builtin.set_fact:
        device_list: "{{ query('cisco.sdwan.devices', 'https://198.18.1.10:8443', device_type='vedge') }}"
    - name: Fetch all devices
      ansible.builtin.set_fact:
        device_list: "{{ query('cisco.sdwan.devices', 'https://198.18.1.10:8443') }}"
"""
RETURN = """
    _raw:
        description: Returns list of devices matching the criteria. Each entry is a dictionary containing the following 
        keys: uuid, name, system_ip, site_id, state, model, version, device_type
        type: list
"""

display = Display()


iter_fields = ('uuid', 'host-name', 'deviceId', 'site-id', 'reachability', 'device-type', 'device-model', 'version')


class DeviceInfo(NamedTuple):
    uuid: str
    name: str
    system_ip: str
    site_id: str
    state: str
    model: str
    version: str
    device_type: str


class LookupModule(LookupBase):
    def parse_optional_args(self, **kwargs):
        optional_args = [
            ('timeout_secs', int, 'an integer', 120),
            ('regex', str, 'a string', None),
            ('not_regex', str, 'a string', None),
            ('reachable', bool, 'a boolean', False),
            ('site', str, 'a string', None),
            ('system_ip', str, 'a string', None),
            ('device_type', str, 'a string', None)
        ]
        for arg_name, arg_type, arg_hint, arg_default in optional_args:
            arg_val = kwargs.get(arg_name)
            if arg_val is None:
                arg_val = arg_default
            elif not isinstance(arg_val, arg_type):
                raise AnsibleOptionsError(f"Parameter {arg_name} must be {arg_hint}")

            setattr(self, arg_name, arg_val)

    def device_info_iter(self, api, cedge_models):
        def device_type(device_class, device_model):
            if device_class == 'vedge':
                return 'cedge' if device_model in cedge_models else 'vedge'
            return device_class

        for uuid, name, system_ip, site_id, state, d_class, model, version in Device.get_raise(api).iter(*iter_fields):
            d_type = device_type(d_class, model)
            regex = self.regex or self.not_regex
            if ((regex is None or regex_search(regex, name, inverse=self.regex is None)) and
                (not self.reachable or state == 'reachable') and
                (self.site is None or site_id == self.site) and
                (self.system_ip is None or system_ip == self.system_ip) and
                (self.device_type is None or d_type == self.device_type)):
                yield DeviceInfo(uuid, name, system_ip, site_id, state, model, version, d_type)

            continue

    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        self.parse_optional_args(**kwargs)

        device_list = []
        try:
            for term in terms:
                with Rest(term, variables.get('ansible_user'), variables.get('ansible_password'),
                          timeout=self.timeout_secs) as api:
                    cedge_set = {
                        elem['name'] for elem in api.get('device/models')['data'] if elem['templateClass'] == 'cedge'
                    }
                    device_list.extend(elem._asdict() for elem in self.device_info_iter(api, cedge_set))
                    display.display(f"Matched devices: {len(device_list)}")

        except (RestAPIException, ConnectionError) as ex:
            raise AnsibleLookupError(ex) from None

        return device_list
