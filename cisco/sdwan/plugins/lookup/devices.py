#! /usr/bin/env python3
from cisco_sdwan.base.rest_api import RestAPIException
from ansible.errors import AnsibleLookupError, AnsibleOptionsError
from ansible.utils.display import Display
from ansible.plugins.lookup import LookupBase
from pydantic import ValidationError 
from ansible_collections.cisco.sdwan.plugins.module_utils.common_lookup import is_mutually_exclusive, get_plugin_inventory_args
from ansible_collections.cisco.sdwan.plugins.module_utils.common_inventory import get_inventory_devices,  get_inventory_task_args

DOCUMENTATION = """
lookup: devices
version_added: "1.1"
short_description: Fetches list of SD-WAN devices from vManage
description:
    - This lookup returns list of SD-WAN devices from vManage with multiple filter options.
    - When more than one filter condition is defined match is an 'and' of all conditions.
    - When no filter is defined all devices are returned.
    - Following parameters must be configured in ansible inventor file
      - ansible_host
      - ansible_user
      - ansible_password
      - vmanage_port
      - tenant
      - timeout
options:
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
"""
EXAMPLES = """
    - name: Fetch devices for vedge device type
      ansible.builtin.set_fact:
        device_list: "{{ query('cisco.sdwan.devices',  device_type='vedge') }}"
    - name: Fetch all devices
      ansible.builtin.set_fact:
        device_list: "{{ query('cisco.sdwan.devices') }}"
"""
RETURN = """
    _raw:
        description: Returns list of devices matching the criteria. Each entry is a dictionary containing the following 
        keys: uuid, name, system_ip, site_id, state, model, version, device_type
        type: list
"""

display = Display()

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        mutual_exclusive_fields = ('regex', 'not_regex')
        if is_mutually_exclusive(mutual_exclusive_fields, **kwargs):
            raise AnsibleOptionsError(f"Parameters are mutually exclusive: {mutual_exclusive_fields}")
        
        device_list = []
        try:
            task_args = get_inventory_task_args(kwargs)
            device_list = get_inventory_devices(get_plugin_inventory_args(variables),task_args)
            display.display(f"Matched devices: {len(device_list)}")
        except ValidationError as ex:
             raise AnsibleLookupError(ex)
        except (RestAPIException, ConnectionError) as ex:
            raise AnsibleLookupError(ex) from None

        return device_list