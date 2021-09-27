#!/usr/bin/python

DOCUMENTATION = """
module: backup
author: Satish Kumar Kamavaram (sakamava@cisco.com)
short_description: Save SD-WAN vManage configuration items to local backup
description: This backup module connects to SD-WAN vManage using HTTP REST and 
             returned HTTP responses are stored to default or configured argument
             local backup folder. This module contains multiple arguments with 
             connection and filter details to backup all or specific configurtion data.
             A log file is created under a "logs" directory. This "logs" directory
             is relative to directory where Ansible runs.
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
  regex:
    description:
    - Regular expression matching item names to be backed up, within selected tags
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
  verbose:
    description:
    - Defines to control log level for the logs generated under "logs/sastre.log" when Ansible script is run.
      Supported log levels are NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL
    required: false
    type: str
    default: "DEBUG"
    choices:
    - "NOTSET"
    - "DEBUG"
    - "INFO"
    - "WARNING"
    - "ERROR"
    - "CRITICAL"
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
  timeout:
    description: 
    - vManage REST API timeout in seconds
    required: false
    type: int
    default: 300
  pid:
    description: 
    - CX project id or can also be defined via CX_PID environment variable. 
      This is collected for AIDE reporting purposes only.
    required: false
    type: str
    default: 0
"""

EXAMPLES = """
- name: "Backup vManage configuration"
  cisco.sdwan.backup: 
    address: "198.18.1.10"
    port: 8443
    user: admin
    password: admin
    timeout: 300
    pid: "2"
    verbose: INFO
    workdir: /home/user/backups
    no_rollover: false
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
    pid: "2"
    verbose: INFO
    workdir: /home/user/backups
    no_rollover: false
    regex: ".*"
    tags: "all"
- name: "Backup vManage configuration with some vManage config arguments saved in environment variables"
  cisco.sdwan.backup: 
    timeout: 300
    verbose: INFO
    workdir: /home/user/backups
    no_rollover: false
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
from ansible.module_utils.basic import env_fallback
import logging
from cisco_sdwan.tasks.implementation._backup import (
    TaskBackup,
)
from  ansible_collections.cisco.sdwan.plugins.module_utils.common import (
    ADDRESS,WORKDIR,REGEX,TAGS,NO_ROLLOVER,VERBOSE,
    set_log_level,update_vManage_args,validate_regex,process_task,tag_list,
    get_workdir,get_env_args
)


def main():
    """main entry point for module execution
    """
    argument_spec = dict(
        workdir=dict(type="str"),
        no_rollover=dict(type="bool", default=False),
        regex=dict(type="str"),
        tags=dict(type="list", elements="str", required=True,choices=tag_list),
    )
    update_vManage_args(argument_spec)
    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )
    
    set_log_level(module.params[VERBOSE])
    log = logging.getLogger(__name__)
    log.debug("Task Backup started.")
    
    result = {"changed": False }
   
    workdir = get_workdir(module.params[WORKDIR],module.params[ADDRESS])
    regex = module.params[REGEX]
    validate_regex(REGEX,regex,module)
    
    task_backup = TaskBackup()
    backupArgs = {'workdir':workdir,'no_rollover':module.params[NO_ROLLOVER],'regex':regex,'tags':module.params[TAGS]}
    try:
        process_task(task_backup,get_env_args(module),**backupArgs)
    except Exception as ex:
        module.fail_json(msg=f"Failed to take backup , check the logs for more detaills... {ex}")
  
    log.debug("Task Backup completed successfully.")
    result.update(
        {"stdout": f"Successfully backed up files at {workdir}"}
    )
    module.exit_json(**result)

if __name__ == "__main__":
    main()