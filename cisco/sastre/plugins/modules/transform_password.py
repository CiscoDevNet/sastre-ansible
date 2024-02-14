#! /usr/bin/env python3
# -*- coding: utf-8 -*-

DOCUMENTATION = """
module: transform_password
short_description: Transform retrieve encrypted passwords
description: The transform password task can be used to get encrypted passwords from tags and
             resources either from workdir or target vmanage and saves to yaml file.
notes: 
- Tested against 20.4.1.1
options: 
  save_pwd_file:
    description:
    - Save password file as yaml file
      This generated yml file can be used in transform_update module.
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
- name: Transform password
  cisco.sastre.transform_password:
    save_pwd_file: transform_password.yml
    workdir: transform_password
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
- name: Transform password from vmanage
  cisco.sastre.transform_password:
    save_pwd_file: transform_password.yml
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
"""

RETURN = """
stdout:
  description: Status of Transform password
  returned: always apart from low level errors
  type: str
  sample: 'Task transform password : set completed successfully.vManage address 198.18.1.10'
stdout_lines:
  description: The value of stdout split into a list
  returned: always apart from low level errors
  type: list
  sample: ['Task transform password: set completed successfully.vManage address 198.18.1.10']
"""
from pydantic import ValidationError
from ansible.module_utils.basic import AnsibleModule
from cisco_sdwan.tasks.common import TaskException
from cisco_sdwan.base.rest_api import RestAPIException
from cisco_sdwan.base.models_base import ModelException
from ansible_collections.cisco.sastre.plugins.module_utils.common import common_arg_spec, module_params, run_task


def main():
    argument_spec = common_arg_spec()
    argument_spec.update(
        save_pwd_file=dict(type="str"),
        workdir=dict(type="str")
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    try:
        from cisco_sdwan.tasks.implementation import TaskTransform, TransformPasswordArgs
        task_args = TransformPasswordArgs(
            **module_params('save_pwd_file', 'workdir', module_param_dict=module.params)
        )
        task_result = run_task(TaskTransform, task_args, module.params)

        result = {
            "changed": False
        }
        module.exit_json(**result, **task_result)

    except ImportError:
        module.fail_json(msg="This module requires Sastre-Pro Python package")
    except ValidationError as ex:
        module.fail_json(msg=f"Invalid transform password parameter: {ex}")
    except (RestAPIException, ConnectionError, FileNotFoundError, ModelException, TaskException) as ex:
        module.fail_json(msg=f"Transform password error: {ex}")


if __name__ == "__main__":
    main()
