#! /usr/bin/env python3
DOCUMENTATION = """
module: show_devices
short_description: Show Device List
description: This show devices module connects to SD-WAN vManage using HTTP REST to 
             retrieve different data.This module contains multiple arguments with 
             connection and filter details to retrieve devices,data. 
             The retrieved data will be displayed to console in table
             format or can be exported as csv/json files.
             When multiple filters are defined, the result is an AND of all filters.
notes: 
- Tested against 20.4.1.1
options: 
  exclude:
    description:
    - Exclude table rows matching the regular expression
    required: false
    type: str
  include:
    description:
    - Include table rows matching the regular expression, exclude all other rows
    required: false
    type: str
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
  save_csv:
    description:
    - Export results as CSV files under the specified directory
    required: false
    type: str
  save_json:
    description:
    - Export results as JSON-formatted file
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
- name: Show devices data
  cisco.sdwan.show_devices:
    regex: ".*"
    include: ".*"
    reachable: true
    site: "100"
    system_ip: 10.1.0.2
    save_csv: show_devices_csv
    save_json: show_devices_json
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
    timeout: 300
- name: Show devices data
  cisco.sdwan.show_devices:
    not_regex: ".*"
    reachable: true
    site: "100"
    system_ip: 10.1.0.2
    save_csv: show_devices_csv
    save_json: show_devices_json
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
    timeout: 300
"""

RETURN = """
stdout:
  description: Status of show devices
  returned: always apart from low level errors
  type: str
  sample: 'Task show devices completed successfully'
stdout_lines:
  description: The value of stdout split into a list
  returned: always apart from low level errors
  type: list
  sample: show table view data
"""
from ansible.module_utils.basic import AnsibleModule
from cisco_sdwan.tasks.implementation import TaskShow, ShowDevicesArgs
from pydantic import ValidationError
from cisco_sdwan.tasks.common import TaskException
from cisco_sdwan.base.rest_api import RestAPIException
from cisco_sdwan.base.models_base import ModelException
from ansible_collections.cisco.sdwan.plugins.module_utils.common import common_arg_spec, module_params, run_task


def main():
    argument_spec = common_arg_spec()
    argument_spec.update(
        exclude=dict(type="str"),
        include=dict(type="str"),
        regex=dict(type="str"),
        not_regex=dict(type="str"),
        reachable=dict(type="bool"),
        site=dict(type="str"),
        system_ip=dict(type="str"),
        save_csv=dict(type="str"),
        save_json=dict(type="str")
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=[('regex', 'not_regex')],
        supports_check_mode=True
    )

    try:
        task_args = ShowDevicesArgs(
            **module_params('exclude', 'include', 'regex', 'not_regex', 'reachable', 'site', 'system_ip', 'save_csv', 'save_json',
                            module_param_dict=module.params)
        )
        task_result = run_task(TaskShow, task_args, module.params)

        result = {
            "changed": False
        }
        module.exit_json(**result, **task_result)

    except ValidationError as ex:
        module.fail_json(msg=f"Invalid show devices parameter: {ex}")
    except (RestAPIException, ConnectionError, FileNotFoundError, ModelException, TaskException) as ex:
        module.fail_json(msg=f"Show devices error: {ex}")


if __name__ == "__main__":
    main()
