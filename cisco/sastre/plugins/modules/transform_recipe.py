#! /usr/bin/env python3
DOCUMENTATION = """
module: transform_recipe
short_description: Transform using custom recipe
description: The transform recipe task can be used for custom recipe. A regular expression can be used to select item names to transform.
notes: 
- Tested against 20.4.1.1
options: 
  output:
    description: 
    - Directory to save transform result
    required: true
    type: str
  workdir:
    description: 
    - transform will read from the specified directory instead of target vManage
    required: false
    type: str
  no_rollover:
    description:
    - By default, if output directory already exists it is 
      renamed using a rolling naming scheme. "True" disables the automatic rollover. "False"
      enables the automatic rollover
    required: false
    type: bool
    default: False
  from_file:
    description: 
    - load custom report specification from YAML file
    required: false
    type: str
  from_json:
    description: 
    - load custom report specification from JSON-formatted string
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
- name: Transform recipe
  cisco.sastre.transform_recipe:
    output: transform_recipe
    workdir: /home/user/backup
    no_rollover: false
    from_file: recipe.yml
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
- name: Transform recipe
  cisco.sastre.transform_recipe:
    output: transform_recipe
    from_json: recipe.json
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
"""

RETURN = """
stdout:
  description: Status of Transform recipe
  returned: always apart from low level errors
  type: str
  sample: 'Task transform recipe : set completed successfully.vManage address 198.18.1.10'
stdout_lines:
  description: The value of stdout split into a list
  returned: always apart from low level errors
  type: list
  sample: ['Task transform recipe: set completed successfully.vManage address 198.18.1.10']
"""
from pydantic import ValidationError
from ansible.module_utils.basic import AnsibleModule
from cisco_sdwan.tasks.common import TaskException
from cisco_sdwan.base.rest_api import RestAPIException
from cisco_sdwan.base.models_base import ModelException
from ansible_collections.cisco.sastre.plugins.module_utils.common import common_arg_spec, module_params, run_task, SASTRE_PRO_MSG


def main():
    argument_spec = common_arg_spec()
    argument_spec.update(
        output=dict(type="str", required=True),
        workdir=dict(type="str"),
        no_rollover=dict(type="bool"),
        from_file=dict(type="str"),
        from_json=dict(type="str")
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=[('from_file', 'from_json')],
        supports_check_mode=True
    )

    try:
        from cisco_sdwan.tasks.implementation import TaskTransform, TransformRecipeArgs
        task_args = TransformRecipeArgs(
            **module_params('output', 'workdir', 'no_rollover', 'from_file', 'from_json',
                            module_param_dict=module.params)
        )
        task_result = run_task(TaskTransform, task_args, module.params)

        result = {
            "changed": False
        }
        module.exit_json(**result, **task_result)

    except ImportError:
        module.fail_json(msg=SASTRE_PRO_MSG)
    except ValidationError as ex:
        module.fail_json(msg=f"Invalid transform recipe parameter: {ex}")
    except (RestAPIException, ConnectionError, FileNotFoundError, ModelException, TaskException) as ex:
        module.fail_json(msg=f"Transform recipe error: {ex}")


if __name__ == "__main__":
    main()
