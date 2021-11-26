#! /usr/bin/env python3
DOCUMENTATION = """
module: list_transform
short_description: List configuration items or device certificate information from vManage or a local backup. Display as table or export as csv file.
description: The list task can be used to show items from a target vManage,
             or a backup directory. Matching criteria can contain item tag(s) 
             and regular expression.When multiple filters are defined, the result 
             is an AND of all filters.A log file is created under a "logs" directory.
             This "logs" directoryis relative to directory where Ansible runs.
notes: 
- Tested against 20.4.1.1
options: 
  regex:
    description:
    - Regular expression selecting items to list, match on original item names.
    required: false
    type: str
  not_regex:
    description:
    - Regular expression selecting items NOT to list, match on original item names.
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
  name_regex:
    description:
    - name-regex used to transform an existing item name. Variable {name} is
      replaced with the original template name. Sections of the original template
      name can be selected using the {name <regex>} format. Where  is a
      regular expression that must contain at least one capturing group. Capturing
      groups identify sections of the original name to keep.
      For transform option, this param is mandatory.
    required: true
    type: str
  address:
    description:
    - vManage IP address or can also be defined via VMANAGE_IP environment variable
    required: true
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
  cisco.sdwan.list_transform:
    tags:
        - template_feature
        - policy_vedge
    regex: ".*"
    workdir: backup_198.18.1.10_20210720 
    name_regex: '{name}'
    save_csv: list_config_csv
    save_json: list_config_json
- name: List Configuration
  cisco.sdwan.list_transform:
    tags:
        - template_feature
        - policy_vedge
    not_regex: ".*"
    save_csv: list_config_csv
    save_json: list_config_json
    name_regex: '{name}'
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
    timeout: 300
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
from cisco_sdwan.tasks.implementation import TaskList, ListTransformArgs
from cisco_sdwan.tasks.common import TaskException
from cisco_sdwan.base.rest_api import RestAPIException
from cisco_sdwan.base.models_base import ModelException
from ansible_collections.cisco.sdwan.plugins.module_utils.common import common_arg_spec, module_params, run_task


def main():
    """main entry point for module execution
    """
    argument_spec = common_arg_spec()
    argument_spec.update(
        regex=dict(type="str"),
        not_regex=dict(type="str"),
        workdir=dict(type="str"),
        save_csv=dict(type="str"),
        save_json=dict(type="str"),
        tags=dict(type="list", elements="str", required=True),
        name_regex=dict(type="str", required=True)
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=[('regex', 'not_regex')],
        supports_check_mode=True
    )

    try:
        task_args = ListTransformArgs(
            **module_params('regex', 'not_regex', 'workdir', 'save_csv', 'save_json', 'tags', 'name_regex',
                            module_param_dict=module.params)
        )
        task_result = run_task(TaskList, task_args, module.params)

        result = {
            "changed": False
        }
        module.exit_json(**result, **task_result)

    except ValidationError as ex:
        module.fail_json(msg=f"Invalid list transform parameter: {ex}")
    except (RestAPIException, ConnectionError, FileNotFoundError, ModelException, TaskException) as ex:
        module.fail_json(msg=f"List transform error: {ex}")


if __name__ == "__main__":
    main()
