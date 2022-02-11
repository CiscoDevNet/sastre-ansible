#! /usr/bin/env python3
DOCUMENTATION = """
module: inventory
short_description: Inventory device List
description: This inventory module connects to SD-WAN vManage using HTTP REST to 
             retrieve inventory device list.This module returns list of SD-WAN devices 
             from vManage with multiple filter options. 
             When multiple filters are defined, the result is an AND of all filters.
             When no filter is defined all devices are returned.
notes: 
- Tested against 20.4.1.1
options: 
  regex:
    description:
    - Regular expression matching device name, type or model to display
    required: false
    type: str
  not_regex:
    description:
    - Regular expression matching device name, type or model NOT to display.
    required: false
    type: str
  reachable:
    description:
    - Display only reachable devices
    required: false
    type: bool
    default: False
  site:
    description:
    - Select devices with site ID.
    required: false
    type: str
  system_ip:
    description:
    - Select device with system IP.
    required: false
    type: str
  device_type:
    description:
    - Match on device type to include. Supported values are 'vmanage', 'vsmart', 'vbond', 'vedge', 'cedge'
    required: false
    type: str
  address:
    description:
    - vManage IP address or can also be defined via VMANAGE_IP environment variable
    required: True
    type: str
  port:
    description: 
    - vManage port number or can also be defined via VMANAGE_PORT environment variable
    required: false
    type: int
    default: 8443
  user:
   description: 
   - username or can also be defined via VMANAGE_USER environment variable.
   required: true
   type: str
  password:
    description: 
    - password or can also be defined via VMANAGE_PASSWORD environment variable.
    required: true
    type: str
  tenant:
    description: 
    - tenant name, when using provider accounts in multi-tenant deployments.
    required: false
    type: str
  timeout:
    description: 
    - vManage REST API timeout in seconds
    required: false
    type: int
    default: 300
"""

EXAMPLES = """
- name: Get inventory devices
  cisco.sdwan.inventory:
    regex: ".*"
    reachable: true
    site: "100"
    system_ip: 10.1.0.2
    device_type: 'vmanage'
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
    timeout: 300
- name: Get inventory devices
  cisco.sdwan.inventory:
    not_regex: ".*"
    reachable: true
    site: "100"
    system_ip: 10.1.0.2
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
    timeout: 300
"""

RETURN = """
stdout:
  description: Status of inventory devices
  returned: always apart from low level errors
  type: str
  sample: 'Task inventory completed successfully'
stdout_lines:
  description: The value of stdout split into a list
  returned: always apart from low level errors
  type: list
  sample: show table view data
"""
from ansible.module_utils.basic import AnsibleModule
from pydantic import ValidationError
from cisco_sdwan.base.rest_api import RestAPIException
from ansible_collections.cisco.sdwan.plugins.module_utils.common import common_arg_spec, module_params
from ansible_collections.cisco.sdwan.plugins.module_utils.common_inventory import get_matched_devices, InventoryArgs


def main():
    argument_spec = common_arg_spec()
    argument_spec.update(
        regex_list=dict(type="list", elements="str"),
        regex=dict(type="str"),
        not_regex=dict(type="str"),
        reachable=dict(type="bool"),
        site=dict(type="str"),
        system_ip=dict(type="str"),
        device_type=dict(type="str")
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=[('regex', 'not_regex', 'regex_list')],
        supports_check_mode=True
    )

    try:
        task_args = InventoryArgs(**module_params('regex_list', 'regex', 'not_regex', 'reachable', 'site', 'system_ip',
                                                  'device_type', module_param_dict=module.params))
        task_result = get_matched_devices(module.params, task_args)

        result = {
            "changed": False,
            "json": task_result
        }
        module.exit_json(**result)

    except ValidationError as ex:
        module.fail_json(msg=f"Invalid inventory parameter: {ex}")
    except (RestAPIException, ConnectionError) as ex:
        module.fail_json(msg=f"inventory error: {ex}")


if __name__ == "__main__":
    main()
