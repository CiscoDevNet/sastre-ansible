#! /usr/bin/env python3
# -*- coding: utf-8 -*-

DOCUMENTATION = """
module: show_events
short_description: Display vManage events.
description: This show events module connects to SD-WAN vManage using HTTP REST to 
             retrieve and display vManage events.This module contains multiple arguments with 
             connection and filter details to retrieve data. 
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
  max:
    description: 
    - Maximum number of records to retrieve (default is now)
    required: false
    type: int
    default: 100
  days:
    description: 
    - Retrieve records since <days> ago (default is now)
    required: false
    type: int
    default: 0
  hours:
    description: 
    - Retrieve records since <hours> ago (default is now)
    required: false
    type: int
    default: 1
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
- name: Show events data
  cisco.sastre.show_events:
    include: ".*"
    max: 1
    days: 1
    hours: 1
    detail: true
    save_csv: show_events_csv
    save_json: show_events_json
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
- name: Show events data
  cisco.sastre.show_events:
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
"""

RETURN = """
stdout:
  description: Status of show events
  returned: always apart from low level errors
  type: str
  sample: 'Task show events completed successfully'
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
from ansible_collections.cisco.sastre.plugins.module_utils.common import common_arg_spec, module_params, run_task


def main():
    argument_spec = common_arg_spec()
    argument_spec.update(
        exclude=dict(type="str"),
        include=dict(type="str"),
        max=dict(type="int"),
        days=dict(type="int"),
        hours=dict(type="int"),
        detail=dict(type="bool"),
        simple=dict(type="bool"),
        save_csv=dict(type="str"),
        save_json=dict(type="str")
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=[('detail', 'simple')],
        supports_check_mode=True
    )

    try:
        from cisco_sdwan.tasks.implementation import TaskShow, ShowEventsArgs
        task_args = ShowEventsArgs(
            **module_params('exclude', 'include', 'max', 'days', 'hours', 'detail', 'simple', 'save_csv', 'save_json',
                            module_param_dict=module.params)
        )
        task_result = run_task(TaskShow, task_args, module.params)

        result = {
            "changed": False
        }
        module.exit_json(**result, **task_result)

    except ImportError:
        module.fail_json(msg="This module requires Sastre-Pro Python package")
    except ValidationError as ex:
        module.fail_json(msg=f"Invalid show events parameter: {ex}")
    except (RestAPIException, ConnectionError, FileNotFoundError, ModelException, TaskException) as ex:
        module.fail_json(msg=f"Show events error: {ex}")


if __name__ == "__main__":
    main()
