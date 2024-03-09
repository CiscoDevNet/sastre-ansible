#! /usr/bin/env python3
# -*- coding: utf-8 -*-

DOCUMENTATION = """
module: list_certificate
short_description: List configuration items or device certificate information from vManage or a local backup. Display as table or export as csv file.
description: The list task can be used to show items from a target vManage,
             or a backup directory. Matching criteria can contain item tag(s) 
             and regular expression.When multiple filters are defined, the result 
             is an AND of all filters. A log file is created under a "logs" directory.
             This "logs" directory is relative to directory where Ansible runs.
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
  workdir:
    description:
    - list will read from the specified directory instead of target vManage. Either workdir or vManage address/user/password is mandatory
    required: false
    type: str
  save_csv:
    description:
    - Export table as a csv file
    required: false
    type: str
  save_json:
    description:
    - Export table as a json file
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
- name: List Certificate
  cisco.sastre.list_certificate:
    include: ".*"
    workdir: backup_198.18.1.10_20210720 
    save_csv: list_config_csv
    save_json: list_config_json
- name: List Certificate
  cisco.sastre.list_certificate:
    exclude: ".*"
    save_csv: list_config_csv
    save_json: list_config_json
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
"""

RETURN = """
stdout:
  description: Status of list
  returned: always apart from low level errors
  type: str
  sample: 'Task List: certificate completed successfully.vManage address 198.18.1.10'
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
from cisco_sdwan.tasks.implementation import TaskList, ListCertificateArgs
from ansible_collections.cisco.sastre.plugins.module_utils.common import common_arg_spec, module_params, run_task


def main():
    argument_spec = common_arg_spec()
    argument_spec.update(
        exclude=dict(type="str"),
        include=dict(type="str"),
        workdir=dict(type="str"),
        save_csv=dict(type="str"),
        save_json=dict(type="str"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    try:
        task_args = ListCertificateArgs(
            **module_params('exclude', 'include', 'workdir', 'save_csv', 'save_json', module_param_dict=module.params)
        )
        task_result = run_task(TaskList, task_args, module.params)

        result = {
            "changed": False
        }
        module.exit_json(**result, **task_result)

    except ValidationError as ex:
        module.fail_json(msg=f"Invalid list certificate parameter: {ex}")
    except (RestAPIException, ConnectionError, FileNotFoundError, ModelException, TaskException) as ex:
        module.fail_json(msg=f"List certificate error: {ex}")


if __name__ == "__main__":
    main()
