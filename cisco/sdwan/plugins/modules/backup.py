#! /usr/bin/env python3
DOCUMENTATION = """
module: backup
short_description: Save SD-WAN vManage configuration items to local backup
description: This backup module connects to SD-WAN vManage using HTTP REST and 
             returned HTTP responses are stored to default or configured argument
             local backup folder. This module contains multiple arguments with 
             connection and filter details to backup all or specific configurtion data.
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
  no_rollover:
    description:
    - By default, if workdir already exists (before a new backup is saved) the old workdir is 
      renamed using a rolling naming scheme. "True" disables the automatic rollover. "False"
      enables the automatic rollover
    required: false
    type: bool
    default: False
  save_running:
    description:
    - Include the running config from each node to the backup. This is useful for
      reference or documentation purposes. It is not needed by the restore task.
    required: false
    type: bool
    default: False
  regex:
    description:
    - Regular expression matching item names to be backed up, within selected tags
    required: false
    type: str
  not_regex:
    description:
    - Regular expression matching item names NOT to backup, within selected tags
    required: false
    type: str
  tags:
    description:
    - Defines one or more tags for selecting items to be backed up. Multiple tags should be
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
- name: "Backup vManage configuration"
  cisco.sdwan.backup: 
    address: "198.18.1.10"
    port: 8443
    user: admin
    password: admin
    timeout: 300
    workdir: /home/user/backups
    no_rollover: false
    save_running: true
    regex: ".*"
    tags: 
      - template_device
      - template_feature
- name: "Backup all vManage configuration"
  cisco.sdwan.backup: 
    address: "198.18.1.10"
    port: 8443
    user: admin
    password: admin
    timeout: 300
    workdir: /home/user/backups
    no_rollover: false
    save_running: true
    regex: ".*"
    tags: "all"
- name: "Backup vManage configuration with some vManage config arguments saved in environment variables"
  cisco.sdwan.backup: 
    timeout: 300
    workdir: /home/user/backups
    no_rollover: false
    save_running: true
    regex: ".*"
    tags: "all"
- name: "Backup vManage configuration with all defaults"
  cisco.sdwan.backup: 
    address: "198.18.1.10"
    user: admin
    password: admin
    tags: "all"
"""

RETURN = """
stdout:
  description: Status of backup
  returned: always apart from low level errors
  type: str
  sample: 'Successfully backed up files at backup_198.18.1.10_20210628'
stdout_lines:
  description: The value of stdout split into a list
  returned: always apart from low level errors
  type: list
  sample: ['Successfully backed up files at backup_198.18.1.10_20210628']
"""
from ansible.module_utils.basic import AnsibleModule
from pydantic import ValidationError
from cisco_sdwan.tasks.utils import default_workdir
from cisco_sdwan.tasks.common import TaskException
from cisco_sdwan.base.rest_api import RestAPIException
from cisco_sdwan.base.models_base import ModelException
from cisco_sdwan.tasks.implementation import TaskBackup, BackupArgs
from ansible_collections.cisco.sdwan.plugins.module_utils.common import common_arg_spec, module_params, run_task


def main():
    argument_spec = common_arg_spec()
    argument_spec.update(
        regex=dict(type="str"),
        not_regex=dict(type="str"),
        no_rollover=dict(type="bool"),
        save_running=dict(type="bool"),
        workdir=dict(type="str"),
        tags=dict(type="list", elements="str", required=True)
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=[('regex', 'not_regex')],
        supports_check_mode=True
    )

    try:
        task_args = BackupArgs(
            workdir=module.params['workdir'] or default_workdir(module.params['address']),
            **module_params('regex', 'not_regex', 'no_rollover', 'save_running', 'tags',
                            module_param_dict=module.params)
        )
        task_result = run_task(TaskBackup, task_args, module.params)

        result = {
            "changed": False
        }
        module.exit_json(**result, **task_result)

    except ValidationError as ex:
        module.fail_json(msg=f"Invalid backup parameter: {ex}")
    except (RestAPIException, ConnectionError, FileNotFoundError, ModelException, TaskException) as ex:
        module.fail_json(msg=f"Backup error: {ex}")


if __name__ == "__main__":
    main()
