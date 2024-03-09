#! /usr/bin/env python3
# -*- coding: utf-8 -*-

DOCUMENTATION = """
module: show_realtime
short_description: Realtime commands. Slower, but up-to-date data. vManage collect data from devices in realtime.
description: This show realtime module connects to SD-WAN vManage using HTTP REST to 
             retrieve different data.This module contains multiple arguments with 
             connection and filter details to retrieve devices,data. 
             The retrieved data will be displayed to console in table
             format or can be exported as csv/json files.
             When multiple filters are defined, the result is an AND of all filters.
notes: 
- Tested against 20.10
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
  cmd:
    description:
    - group of, or specific command to execute.
      Group options are all, app-route, bfd, control, dpi, interface, omp, software, system, tunnel.
      Command options are app-route sla-class, app-route stats, bfd sessions, control connections, 
      control local-properties, dpi summary, interface info, omp adv-routes, omp peers, omp summary, 
      software info, system status, tunnel stats.
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
- name: Show realtime data
  cisco.sastre.show_realtime:
    include: ".*"
    regex: ".*"
    reachable: true
    site: "100"
    system_ip: 10.1.0.2
    save_csv: show_realtime_csv
    save_json: show_realtime_json
    cmd:
      - all
    detail: true
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
- name: Show realtime data
  cisco.sastre.show_realtime:
    exclude: ".*"
    not_regex: ".*"
    reachable: true
    site: "100"
    system_ip: 10.1.0.2
    save_csv: show_realtime_csv
    save_json: show_realtime_json
    cmd:
      - all
    detail: true
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
"""

RETURN = """
stdout:
  description: Status of show realtime
  returned: always apart from low level errors
  type: str
  sample: 'Task show realtime completed successfully'
stdout_lines:
  description: The value of stdout split into a list
  returned: always apart from low level errors
  type: list
  sample: show table view data
"""
from ansible.module_utils.basic import AnsibleModule
from pydantic import ValidationError
from cisco_sdwan.tasks.common import TaskException
from cisco_sdwan.base.rest_api import RestAPIException
from cisco_sdwan.base.models_base import ModelException
from cisco_sdwan.tasks.implementation import TaskShow, ShowRealtimeArgs
from ansible_collections.cisco.sastre.plugins.module_utils.common import common_arg_spec, module_params, run_task


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
        save_json=dict(type="str"),
        cmd=dict(type="list", elements="str", required=True),
        detail=dict(type="bool"),
        simple=dict(type="bool")
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=[('regex', 'not_regex'), ('detail', 'simple')],
        supports_check_mode=True
    )

    try:
        task_args = ShowRealtimeArgs(
            **module_params('exclude', 'include', 'regex', 'not_regex', 'reachable', 'site', 'system_ip', 'save_csv',
                            'save_json', 'cmd', 'detail', 'simple', module_param_dict=module.params)
        )
        task_result = run_task(TaskShow, task_args, module.params)

        result = {
            "changed": False
        }
        module.exit_json(**result, **task_result)

    except ValidationError as ex:
        module.fail_json(msg=f"Invalid show realtime parameter: {ex}")
    except (RestAPIException, ConnectionError, FileNotFoundError, ModelException, TaskException) as ex:
        module.fail_json(msg=f"Show realtime error: {ex}")


if __name__ == "__main__":
    main()
