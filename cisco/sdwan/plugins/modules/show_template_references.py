#!/usr/bin/python
DOCUMENTATION = """
module: show_template_references
short_description: Show template references about device templates on vManage or from a local backup. Display as table or export as csv/json file.
description: 
        - The Show template task can be used to show device templates from a target vManage or a backup directory. 
        - Criteria can contain regular expression with matching or not matching device or feature template names.
notes: 
- Tested against 20.4.1.1
options: 
  regex:
    description:
    - Regular expression matching device template names or IDs to inspect.
      regex and not_regex parameters are mutually exclusive 
    required: false
    type: str
  not_regex:
    description:
    - Regular expression matching device template names or IDs NOT to inspect.
      regex and not_regex parameters are mutually exclusive 
    required: false
    type: str
  workdir:
    description:
    - show-template will read from the specified directory instead of target vManage. Either workdir or vManage address/user/password is mandatory
    required: false
    type: str
  save_csv:
    description:
    - Export tables as csv files under the specified directory
    required: false
    type: str
  save_json:
    description:
    - Save teamplate references as json file
    required: false
    type: str
  with_refs:
    description:
    - Include only feature-templates with device-template references
    required: false
    type: bool
    default: False
  address:
    description:
    - vManage IP address or can also be defined via VMANAGE_IP environment variable.
      Either workdir or address/user/password parameter is mandatory
    required: false
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
     Either workdir or address/user/password parameter is mandatory
   required: false
   type: str
  password:
    description: 
    - password or can also be defined via VMANAGE_PASSWORD environment variable.
      Either workdir or address/user/password parameter is mandatory
    required: false
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
- name: Show Template references from local backup directory
  cisco.sdwan.show_template_references:
    regex: ".*"
    save_csv: show_temp_csv
    save_json: show_temp_json
    workdir: backup_198.18.1.10_20210720
    with_refs: True
- name: Show Template references from vManage
  cisco.sdwan.show_template_references:
    not_regex: ".*"
    save_csv: show_temp_csv
    save_json: show_temp_json
    with_refs: True
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
"""

RETURN = """
stdout:
  description: Status of Show Template references
  returned: always apart from low level errors
  type: str
  sample: Show Template references data in string format
stdout_lines:
  description: The value of stdout split into a list
  returned: always apart from low level errors
  type: list
  sample: show table view data
"""
from ansible.module_utils.basic import AnsibleModule
from pydantic import ValidationError
from cisco_sdwan.tasks.implementation import TaskShowTemplate, ShowTemplateRefArgs
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
        with_refs=dict(type="bool", default=False)
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=[('regex', 'not_regex')],
        supports_check_mode=True
    )

    try:
        task_args = ShowTemplateRefArgs(
            **module_params('regex', 'not_regex', 'workdir', 'save_csv', 'save_json', 'with_refs',
                            module_param_dict=module.params)
        )
        task_result = run_task(TaskShowTemplate, task_args, module.params)

        result = {
            "changed": False
        }
        module.exit_json(**result, **task_result)

    except ValidationError as ex:
        module.fail_json(msg=f"Invalid show template references parameter: {ex}")
    except (RestAPIException, ConnectionError, FileNotFoundError, ModelException, TaskException) as ex:
        module.fail_json(msg=f"Show template references error: {ex}")


if __name__ == "__main__":
    main()
