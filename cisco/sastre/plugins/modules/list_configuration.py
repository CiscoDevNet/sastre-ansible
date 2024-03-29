#! /usr/bin/env python3
# -*- coding: utf-8 -*-

DOCUMENTATION = """
module: list_configuration
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
  tags:
    description:
    - Defines one or more tags for selecting groups of items. Multiple tags should be
      configured as list. Available tags are template_feature, policy_profile, policy_definition,
      all, policy_list, policy_vedge, policy_voice, policy_vsmart, template_device, policy_security,
      policy_customapp. Special tag "all" selects all items, including WAN edge certificates and 
      device configurations.
    required: true
    type: list
    elements: str
    choices:
    - "template_feature"
    - "policy_profile"
    - "policy_definition"
    - "all"
    - "policy_list"
    - "policy_vedge"
    - "policy_voice"
    - "policy_vsmart"
    - "template_device"
    - "policy_security"
    - "policy_customapp"
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
- name: List Configuration
  cisco.sastre.list_configuration:
    tags:
        - template_feature
        - policy_vedge
    include: ".*"
    workdir: backup_198.18.1.10_20210720 
    save_csv: list_config_csv
    save_json: list_config_json
- name: List Configuration
  cisco.sastre.list_configuration:
    tags:
        - template_feature
        - policy_vedge
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
  sample: 'Task List: configuration completed successfully.vManage address 198.18.1.10'
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
from cisco_sdwan.tasks.implementation import TaskList, ListConfigArgs
from ansible_collections.cisco.sastre.plugins.module_utils.common import common_arg_spec, module_params, run_task


def main():
    argument_spec = common_arg_spec()
    argument_spec.update(
        exclude=dict(type="str"),
        include=dict(type="str"),
        workdir=dict(type="str"),
        save_csv=dict(type="str"),
        save_json=dict(type="str"),
        tags=dict(type="list", elements="str", required=True)
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )
    try:
        task_args = ListConfigArgs(
            **module_params('exclude', 'include', 'workdir', 'save_csv', 'save_json', 'tags',
                            module_param_dict=module.params)
        )
        task_result = run_task(TaskList, task_args, module.params)

        result = {
            "changed": False
        }
        module.exit_json(**result, **task_result)

    except ValidationError as ex:
        module.fail_json(msg=f"Invalid list configuration parameter: {ex}")
    except (RestAPIException, ConnectionError, FileNotFoundError, ModelException, TaskException) as ex:
        module.fail_json(msg=f"List configuration error: {ex}")


if __name__ == "__main__":
    main()
