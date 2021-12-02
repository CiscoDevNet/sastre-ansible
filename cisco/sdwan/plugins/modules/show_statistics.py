#! /usr/bin/env python3
DOCUMENTATION = """
module: show_statistics
short_description: Statistics commands. Faster, but data is 30 min or more old.Allows historical data queries.
description: This show statistics module connects to SD-WAN vManage using HTTP REST to 
             retrieve different data.This module contains multiple arguments with 
             connection and filter details to retrieve devices,data. 
             The retrieved data will be displayed to console in table
             format or can be exported as csv/json files.
             When multiple filters are defined, the result is an AND of all filters.
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
  cmd:
    description:
    - group of, or specific command to execute.
      Group options are all, bfd, control, interface, omp, system. 
      Command options are bfd sessions, control connections, control local-properties, interface cedge,
      interface vedge, omp peers, system info.
    required: true
    type: list
  detail:
    description:
    - Detailed output (i.e. more columns)
    required: false
    type: bool
    default: False
  simple:
    description:
    - Simple output (i.e. less columns)
    required: false
    type: bool
    default: False
  days:
    description: 
    - Query statistics from <days> ago (default is now)
    required: false
    type: int
    default: 0
  hours:
    description: 
    - Query statistics from <hours> ago (default is now)
    required: false
    type: int
    default: 0
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
- name: Show state data
  cisco.sdwan.show_statistics:
    regex: ".*"
    reachable: true
    site: "100"
    system_ip: 10.1.0.2
    save_csv: show_statistics_csv
    save_json: show_statistics_json
    cmd:
      - all
    detail: true
    days: 1
    hours: 1
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
    timeout: 300
- name: Show state data
  cisco.sdwan.show_statistics:
    not_regex: ".*"
    reachable: true
    site: "100"
    system_ip: 10.1.0.2
    save_csv: show_statistics_csv
    save_json: show_statistics_json
    cmd:
      - all
    detail: true
    days: 1
    hours: 1
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
    timeout: 300
"""

RETURN = """
stdout:
  description: Status of show statistics
  returned: always apart from low level errors
  type: str
  sample: 'Task show statistics completed successfully'
stdout_lines:
  description: The value of stdout split into a list
  returned: always apart from low level errors
  type: list
  sample: show table view data
"""
from ansible.module_utils.basic import AnsibleModule
from cisco_sdwan.tasks.implementation import TaskShow, ShowStatisticsArgs
from pydantic import ValidationError
from cisco_sdwan.tasks.common import TaskException
from cisco_sdwan.base.rest_api import RestAPIException
from cisco_sdwan.base.models_base import ModelException
from ansible_collections.cisco.sdwan.plugins.module_utils.common import common_arg_spec, module_params, run_task


def main():
    argument_spec = common_arg_spec()
    argument_spec.update(
        regex=dict(type="str"),
        not_regex=dict(type="str"),
        reachable=dict(type="bool"),
        site=dict(type="str"),
        system_ip=dict(type="str"),
        save_csv=dict(type="str"),
        save_json=dict(type="str"),
        cmd=dict(type="list", elements="str", required=True),
        detail=dict(type="bool"),
        simple=dict(type="bool"),
        days=dict(type="int"),
        hours=dict(type="int")
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=[('regex', 'not_regex'), ('detail', 'simple')],
        supports_check_mode=True
    )

    try:
        task_args = ShowStatisticsArgs(
            **module_params('regex', 'not_regex', 'reachable', 'site', 'system_ip', 'save_csv', 'save_json', 'cmd',
                            'detail', 'simple', 'days', 'hours', module_param_dict=module.params)
        )
        task_result = run_task(TaskShow, task_args, module.params)

        result = {
            "changed": False
        }
        module.exit_json(**result, **task_result)

    except ValidationError as ex:
        module.fail_json(msg=f"Invalid show statistics parameter: {ex}")
    except (RestAPIException, ConnectionError, FileNotFoundError, ModelException, TaskException) as ex:
        module.fail_json(msg=f"Show statistics error: {ex}")


if __name__ == "__main__":
    main()
