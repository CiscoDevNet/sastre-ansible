#! /usr/bin/env python3
DOCUMENTATION = """
module: restore
short_description: Restore configuration items from a local backup to SD-WAN vManage. 
description: This restore module connects to SD-WAN vManage using HTTP REST to 
             updated configuration data stored in local default backup or configured 
             local backup folder. This module contains multiple arguments with 
             connection and filter details to restore all or specific configurtion data.
notes: 
- Tested against 20.4.1.1
options: 
  workdir:
    description: 
    - Defines the location (in the local machine) where vManage data files are located.
      By default, it follows the format "backup_<address>_<yyyymmdd>". The workdir
      argument can be used to specify a different location. workdir is under a 'data' 
      directory. This 'data' directory is relative to the directory where Ansible 
      script is run.
    required: false
    type: str
    default: "backup_<address>_<yyyymmdd>"
  regex:
    description:
    - Regular expression matching item names to restore, within selected tags.
    required: false
    type: str
  not_regex:
    description:
    - Regular expression matching item names NOT to restore, within selected tags.
    required: false
    type: str
  tag:
    description:
    - Tag for selecting items to be restored. Items that are dependencies of the 
      specified tag are automatically included. Available tags are template_feature, policy_profile, policy_definition,
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
  dryrun:
    description:
    - dry-run mode. Items to be restored are listed but not pushed to vManage.
    required: false
    type: bool
    default: False
  attach:
    description:
    - Attach devices to templates and activate vSmart policy after restoring items
    required: false
    type: bool
    default: False
  force:
    description:
    - Target vManage items with the same name as the corresponding item in workdir
      are updated with the contents from workdir. Without this option, those items
      are skipped and not overwritten.
    required: false
    type: bool
    default: False
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
- name: Restore vManage configuration
  cisco.sdwan.restore:
    address: "198.18.1.10"
    port: 8443
    user: "admin"
    password: "admin"
    timeout: 300
    workdir: "/home/user/backups"
    regex: ".*"
    dryrun: False
    attach: False
    force: False
    tag: "template_device"
- name: Restore all vManage configuration
  cisco.sdwan.restore:
    address: "198.18.1.10"
    port: 8443
    user: "admin"
    password: "admin"
    timeout: 300
    workdir: "/home/user/backups"
    regex: ".*"
    dryrun: False
    attach: False
    force: False
    tag: "all"
- name: Restore vManage configuration with some vManage config arguments saved in environment variables
  cisco.sdwan.restore:
    timeout: 300
    workdir: "/home/user/backups"
    not_regex: ".*"
    dryrun: False
    attach: False
    force: False
    tag: "all"
- name: Restore vManage configuration with all defaults
  cisco.sdwan.restore:
    address: "198.18.1.10"
    user: "admin"
    password: "admin"
    tag: "all"
"""

RETURN = """
stdout:
  description: Status of restore
  returned: always apart from low level errors
  type: str
  sample: "Successfully restored files from local backup_198.18.1.10_20210625 to vManage address 198.18.1.10"
stdout_lines:
  description: The value of stdout split into a list
  returned: always apart from low level errors
  type: list
  sample:  [ "Successfully restored files from local backup_198.18.1.10_20210625 to vManage address 198.18.1.10"]
"""
from ansible.module_utils.basic import AnsibleModule
from pydantic import ValidationError
from cisco_sdwan.tasks.utils import default_workdir
from cisco_sdwan.tasks.implementation import TaskRestore, RestoreArgs
from cisco_sdwan.tasks.common import TaskException
from cisco_sdwan.base.rest_api import RestAPIException
from cisco_sdwan.base.models_base import ModelException
from ansible_collections.cisco.sdwan.plugins.module_utils.common import common_arg_spec, module_params, run_task


def main():
    argument_spec = common_arg_spec()
    argument_spec.update(
        regex=dict(type="str"),
        not_regex=dict(type="str"),
        workdir=dict(type="str"),
        dryrun=dict(type="bool"),
        attach=dict(type="bool"),
        update=dict(type="bool"),
        tag=dict(type="str", required=True)
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=[('regex', 'not_regex')],
        supports_check_mode=True
    )

    try:
        task_args = RestoreArgs(
            workdir=module.params['workdir'] or default_workdir(module.params['address']),
            **module_params('regex', 'not_regex', 'dryrun', 'attach', 'update', 'tag',
                            module_param_dict=module.params)
        )
        task_result = run_task(TaskRestore, task_args, module.params)

        result = {
            "changed": False
        }
        module.exit_json(**result, **task_result)

    except ValidationError as ex:
        module.fail_json(msg=f"Invalid Restore parameter: {ex}")
    except (RestAPIException, ConnectionError, FileNotFoundError, ModelException, TaskException) as ex:
        module.fail_json(msg=f"Restore task error: {ex}")


if __name__ == "__main__":
    main()
