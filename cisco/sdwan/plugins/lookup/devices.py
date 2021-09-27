#!/usr/bin/python
from cisco_sdwan.base.rest_api import Rest, RestAPIException, LoginFailedException
from requests.exceptions import ConnectionError
from ansible.errors import AnsibleLookupError, AnsibleOptionsError
from ansible.utils.display import Display
from ansible.plugins.lookup import LookupBase
DOCUMENTATION = """
lookup: devices
author: Satish Kumar Kamavaram (sakamava@cisco.com)
version_added: "1.0"
short_description: Fetches list of SD-WAN devices based on device type
description:
    - This lookup returns list of SD-WAN devices from vManage with an argument to filter by device type.
options:
    _terms:
        description: base url to connect to SD-WAN vmanage
        required: True
        type: list
    device_type:
        description: >
            Determines the device type to be fetched from vmanage. By default all devices will be returned.
            Supported values are 'vmanage','vsmart','vbond','vedge'
        required: False
        type: str
    timeout_secs:
        description: REST http timeout value in seconds
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
RETURN= """
    _raw:
        description: Returns list of dictionary of devices with these keys deviceId, uuid, host-name, node-type, site-id
        type: list
"""

display = Display()
FIELDS_TO_KEEP = {"deviceId", "uuid", "host-name",
                  "site-id", "device-type", "device-model"}
CEDGE = 'cedge'
VEDGE = 'vedge'


def trim_fields(devices_entry: dict) -> dict:
    return {k: v for k, v in devices_entry.items() if k in FIELDS_TO_KEEP}


class LookupModule(LookupBase):
    def parse_optional_args(self, **kwargs):
        optional_args = [
            ('timeout_secs', int, 'an integer', 120),
            ('device_type', str, 'an string', None)
        ]
        for arg_name, arg_type, arg_hint, arg_default in optional_args:
            arg_val = kwargs.get(arg_name)
            if arg_val is None:
                arg_val = arg_default
            elif not isinstance(arg_val, arg_type):
                raise AnsibleOptionsError(
                    f"Parameter {arg_name} must be {arg_hint}")

            setattr(self, arg_name, arg_val)

    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        self.parse_optional_args(**kwargs)

        device_list = []
        for term in terms:
            try:
                with Rest(term, variables.get('ansible_user'), variables.get('ansible_password'),
                          timeout=self.timeout_secs) as api:
                    response = api.get('device')
                    display.vvv(f"Device API Response... {response}")
                    display.display(
                        f"Total devices returned by vmanage = {len(response['data'])}")
                    device_list.extend(trim_fields(devices) for devices in response['data']
                                       if self.device_type is None or devices['device-type'] == self.device_type)
                    if self.device_type is None or self.device_type == VEDGE:
                        response = api.get('device/models')
                        display.vvv(
                            f"Device Models API Response... {response}")
                        cedges = {
                            elem['name'] for elem in response['data'] if elem['templateClass'] == CEDGE}
                        for device in device_list:
                            if device['device-model'] in cedges:
                                device['device-type'] = CEDGE
                    if self.device_type is not None:
                        display.display(
                            f"Found {len(device_list)} devices for device type '{self.device_type}'")
                    for device in device_list:
                        device.pop('device-model')
                        device['node-type'] = device.pop('device-type')
            except (LoginFailedException, ConnectionError, RestAPIException) as ex:
                raise AnsibleLookupError(ex) from None
        return device_list
