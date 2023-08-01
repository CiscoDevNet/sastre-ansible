#! /usr/bin/env python3
# -*- coding: utf-8 -*-

DOCUMENTATION = """
module: transform_updatepwd
short_description: Transform update password configuration items
description: The transform update task can be used to update password.
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
  tag:
    description:
    - Tag for selecting items to transform. Available tags are template_feature, policy_profile, policy_definition,
      all, policy_list, policy_vedge, policy_voice, policy_vsmart, template_device, policy_security,
      policy_customapp. Special tag "all" selects all items.
    required: true
    type: str
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
  regex:
    description:
    - Regular expression selecting item names to transform
    required: false
    type: str
  not_regex:
    description:
    - Regular expression selecting item names NOT to transform
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
- name: Transform update password
  cisco.sastre.transform_updatepwd:
    output: transform_update_configs
    workdir: transform_update
    no_rollover: false
    tag: "template_device"
    regex: "cedge_1"
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
- name: Transform update password from vmanage
  cisco.sastre.transform_updatepwd:
    output: transform_update_configs
    tag: "template_device"
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
"""

RETURN = """
stdout:
  description: Status of Transform udpate password
  returned: always apart from low level errors
  type: str
  sample: 'Task transform update password: set completed successfully.vManage address 198.18.1.10'
stdout_lines:
  description: The value of stdout split into a list
  returned: always apart from low level errors
  type: list
  sample: ['Task transform update password: set completed successfully.vManage address 198.18.1.10']
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
        output=dict(type="str", required=True),
        workdir=dict(type="str"),
        no_rollover=dict(type="bool"),
        tag=dict(type="str", required=True),
        regex=dict(type="str"),
        not_regex=dict(type="str")
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=[('regex', 'not_regex')],
        supports_check_mode=True
    )

    try:
        from cisco_sdwan.tasks.implementation import TaskTransform, TransformUpdatePasswordArgs
        task_args = TransformUpdatePasswordArgs(
            **module_params('output', 'workdir', 'no_rollover', 'tag', 'regex', 'not_regex',
                            module_param_dict=module.params)
        )
        task_result = run_task(TaskTransform, task_args, module.params)

        result = {
            "changed": False
        }
        module.exit_json(**result, **task_result)

    except ImportError:
        module.fail_json(msg="This module requires Sastre-Pro Python package")
    except ValidationError as ex:
        module.fail_json(msg=f"Invalid transform update password parameter: {ex}")
    except (RestAPIException, ConnectionError, FileNotFoundError, ModelException, TaskException) as ex:
        module.fail_json(msg=f"Transform update password error: {ex}")


if __name__ == "__main__":
    main()
