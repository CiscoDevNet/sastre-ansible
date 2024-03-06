#! /usr/bin/env python3
# -*- coding: utf-8 -*-

DOCUMENTATION = """
module: transform_password
short_description: Retrieves encrypted fields from vManage configuration items and generates recipe file for transform_recipe task.
description: The transform build-recipe task can be used to retrieve encrypted fields in vManage configuration
             items either from workdir or target vManage. The retrieved encrypted fields are used to create a recipe 
             file, which can be used by the transform recipe task to modify the encrypted values.
notes: 
- Tested against 20.10
options: 
  recipe_file:
    description:
    - Save recipe file, to be used with transform_recipe task
    required: false
    type: str
  workdir:
    description: 
    - transform password will read from the specified directory instead of target vManage
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
- name: Transform build-recipe from local backup
  cisco.sastre.transform_build_recipe:
    recipe_file: transform_build_recipe.yml
    workdir: transform_build_recipe
    
- name: Transform build-recipe from vManage
  cisco.sastre.transform_build_recipe:
    recipe_file: transform_build_recipe.yml
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
"""

RETURN = """
stdout:
  description: Status of Transform build recipe
  returned: always apart from low level errors
  type: str
  sample: 'Task transform build recipe: set completed successfully.vManage address 198.18.1.10'
stdout_lines:
  description: The value of stdout split into a list
  returned: always apart from low level errors
  type: list
  sample: ['Task transform build recipe: set completed successfully.vManage address 198.18.1.10']
"""
from pydantic import ValidationError
from ansible.module_utils.basic import AnsibleModule
from cisco_sdwan.tasks.common import TaskException
from cisco_sdwan.base.rest_api import RestAPIException
from cisco_sdwan.base.models_base import ModelException
from cisco_sdwan.tasks.implementation import TaskTransform, TransformBuildRecipeArgs
from ansible_collections.cisco.sastre.plugins.module_utils.common import common_arg_spec, module_params, run_task


def main():
    argument_spec = common_arg_spec()
    argument_spec.update(
        recipe_file=dict(type="str"),
        workdir=dict(type="str")
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    try:
        task_args = TransformBuildRecipeArgs(
            **module_params('recipe_file', 'workdir', module_param_dict=module.params)
        )
        task_result = run_task(TaskTransform, task_args, module.params)

        result = {
            "changed": False
        }
        module.exit_json(**result, **task_result)

    except ValidationError as ex:
        module.fail_json(msg=f"Invalid transform build-recipe parameter: {ex}")
    except (RestAPIException, ConnectionError, FileNotFoundError, ModelException, TaskException) as ex:
        module.fail_json(msg=f"Transform build-recipe error: {ex}")


if __name__ == "__main__":
    main()
