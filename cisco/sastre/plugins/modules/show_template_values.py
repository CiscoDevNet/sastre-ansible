#! /usr/bin/env python3
DOCUMENTATION = """
module: show_template_values
short_description: Show template values about device templates on vManage or from a local backup. Display as table or export as csv/json file.
description: 
        - The Show template task can be used to show device templates from a target vManage or a backup directory. 
        - Criteria can contain regular expression with matching or not matching device or feature template names.
notes: 
- Tested against 20.4.1.1
options: 
  templates:
    description:
    - Regular expression selecting device templates to inspect.
      Match on template name or ID. 
    required: false
    type: str
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
    - Save teamplate value as json file
    required: false
    type: str
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
- name: Show Template values from local backup directory
  cisco.sastre.show_template_values:
    workdir: backup_198.18.1.10_20210720
    save_csv: show_temp_csv
    save_json: show_temp_json
- name: Show Template values from vManage
  cisco.sastre.show_template_values:
    save_csv: show_temp_csv
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
"""

RETURN = """
stdout:
  description: Status of Show Template Values
  returned: always apart from low level errors
  type: str
  sample: Show Template values data in string format
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
from ansible_collections.cisco.sastre.plugins.module_utils.common import common_arg_spec, module_params, run_task, SASTRE_PRO_MSG


def main():
    argument_spec = common_arg_spec()
    argument_spec.update(
        templates=dict(type="str"),
        exclude=dict(type="str"),
        include=dict(type="str"),
        workdir=dict(type="str"),
        save_csv=dict(type="str"),
        save_json=dict(type="str")
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    try:
        from cisco_sdwan.tasks.implementation import TaskShowTemplate, ShowTemplateValuesArgs 
        task_args = ShowTemplateValuesArgs(
            **module_params('templates', 'exclude', 'include', 'workdir', 'save_csv', 'save_json',
                            module_param_dict=module.params)
        )
        task_result = run_task(TaskShowTemplate, task_args, module.params)

        result = {
            "changed": False
        }
        module.exit_json(**result, **task_result)

    except ImportError:
        module.fail_json(msg=SASTRE_PRO_MSG)
    except ValidationError as ex:
        module.fail_json(msg=f"Invalid show template values parameter: {ex}")
    except (RestAPIException, ConnectionError, FileNotFoundError, ModelException, TaskException) as ex:
        module.fail_json(msg=f"Show template values error: {ex}")


if __name__ == "__main__":
    main()
