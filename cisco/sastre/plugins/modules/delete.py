#! /usr/bin/env python3
DOCUMENTATION = """
module: delete
short_description: Delete configuration items on SD-WAN vManage.
description: This delete module connects to SD-WAN vManage using HTTP REST to 
             delete configuration items. This module contains multiple arguments with 
             connection and filter details to delete all or specific configurtion data.
notes: 
- Tested against 20.4.1.1
options: 
  regex:
    description:
    - Regular expression matching item names to be deleted, within selected tags
    required: false
    type: str
  not_regex:
    description:
    - Regular expression matching item names NOT to delete, within selected tags
    required: false
    type: str
  dryrun:
    description:
    - dry-run mode. Items matched for removal are listed but not deleted.
    required: false
    type: bool
    default: False
  detach:
    description:
    - USE WITH CAUTION! Detach devices from templates and deactivate vSmart policy 
      before deleting items. This allows deleting items that are associated with 
      attached templates and active policies.
    required: false
    type: bool
    default: False
  tag:
    description:
    - Tag for selecting items to be deleted. Available tags are template_feature, policy_profile, policy_definition,
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
- name: "Delete vManage configuration"
  cisco.sastre.delete: 
    address: "198.18.1.10"
    port: 8443
    user: admin
    password: admin
    timeout: 300
    regex: ".*"
    dryrun: True
    detach: False
    tag: "template_device"
- name: "Delete vManage configuration with some vManage config arguments saved in environment variables"
  cisco.sastre.delete: 
    not_regex: ".*"
    dryrun: True
    detach: False
    tag: "all"
- name: "Delete vManage configuration with all defaults"
  cisco.sastre.delete: 
    address: "198.18.1.10"
    user: admin
    password: admin
    tag: "template_device"
"""

RETURN = """
stdout:
  description: Status of delete
  returned: always apart from low level errors
  type: str
  sample: 'Delete completed successfully'
stdout_lines:
  description: The value of stdout split into a list
  returned: always apart from low level errors
  type: list
  sample: ['Delete completed successfully']
"""
from ansible.module_utils.basic import AnsibleModule
from pydantic import ValidationError
from cisco_sdwan.tasks.common import TaskException
from cisco_sdwan.base.rest_api import RestAPIException
from cisco_sdwan.base.models_base import ModelException
from cisco_sdwan.tasks.implementation import TaskDelete, DeleteArgs
from ansible_collections.cisco.sastre.plugins.module_utils.common import common_arg_spec, module_params, run_task


def main():
    argument_spec = common_arg_spec()
    argument_spec.update(
        regex=dict(type="str"),
        not_regex=dict(type="str"),
        dryrun=dict(type="bool"),
        detach=dict(type="bool"),
        tag=dict(type="str", required=True)
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=[('regex', 'not_regex')],
        supports_check_mode=True
    )

    try:
        task_args = DeleteArgs(
            **module_params('regex', 'not_regex', 'dryrun', 'detach', 'tag', module_param_dict=module.params)
        )
        task_result = run_task(TaskDelete, task_args, module.params)

        result = {
            "changed": False
        }
        module.exit_json(**result, **task_result)

    except ValidationError as ex:
        module.fail_json(msg=f"Invalid delete parameter: {ex}")
    except (RestAPIException, ConnectionError, FileNotFoundError, ModelException, TaskException) as ex:
        module.fail_json(msg=f"Delete error: {ex}")


if __name__ == "__main__":
    main()
