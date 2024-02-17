#! /usr/bin/env python3
# -*- coding: utf-8 -*-

DOCUMENTATION = """
module: encrypt
short_description: encrypts password
description: This encrypt module connects to SD-WAN vManage using HTTP REST to 
             convert plain text password to encrypted password
notes: 
- Tested against 20.10
options: 
  pwd:
    description:
    - plain text password
    required: True
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
- name: "encrypt password"
  cisco.sastre.encrypt:
    address: "198.18.1.10"
    port: 8443
    user: "admin"
    password:"admin"
    pwd: "admin123"
- name: "encrypt password with some vManage config arguments saved in environment variables"
  cisco.sastre.encrypt: 
    pwd: "admin123"
"""

RETURN = """
stdout:
  description: Status of encrypt password
  returned: always apart from low level errors
  type: str
  sample: 'Successfully completed encrypt'
stdout_lines:
  description: The value of stdout split into a list
  returned: always apart from low level errors
  type: list
  sample: ['Successfully completed encrypt']
"""

from ansible.module_utils.basic import AnsibleModule
from pydantic import ValidationError
from cisco_sdwan.tasks.common import TaskException
from cisco_sdwan.base.rest_api import RestAPIException
from cisco_sdwan.base.models_base import ModelException
from cisco_sdwan.tasks.implementation import TaskEncrypt, EncryptArgs
from ansible_collections.cisco.sastre.plugins.module_utils.common import common_arg_spec, module_params, run_task


def main():
    argument_spec = common_arg_spec()
    argument_spec.update(
        values=dict(type="list", elements="str", required=True)
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    try:
        task_args = EncryptArgs(
            **module_params('values', module_param_dict=module.params)
        )
        task_result = run_task(TaskEncrypt, task_args, module.params)

        result = {
            "changed": False
        }
        module.exit_json(**result, **task_result)

    except ValidationError as ex:
        module.fail_json(msg=f"Invalid encrypt parameter: {ex}")
    except (RestAPIException, ConnectionError, FileNotFoundError, ModelException, TaskException) as ex:
        module.fail_json(msg=f"encrypt error: {ex}")


if __name__ == "__main__":
    main()
