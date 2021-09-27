#!/usr/bin/python

DOCUMENTATION = """
module: restore
author: Satish Kumar Kamavaram (sakamava@cisco.com)
short_description: Restore configuration items from a local backup to SD-WAN vManage. 
description: This restore module connects to SD-WAN vManage using HTTP REST to 
             updated configuration data stored in local default backup or configured argument
             local backup folder. This module contains multiple arguments with 
             connection and filter details to restore all or specific configurtion data.
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
  regex:
    description:
    - Regular expression matching item names to be restored, within selected tags
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
- name: Restore vManage configuration
  cisco.sdwan.restore:
    address: "198.18.1.10"
    port: 8443
    user: "admin"
    password: "admin"
    timeout: 300
    pid: "2"
    verbose: "INFO"
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
    pid: "2"
    verbose: "INFO"
    workdir: "/home/user/backups"
    regex: ".*"
    dryrun: False
    attach: False
    force: False
    tag: "all"
- name: Restore vManage configuration with some vManage config arguments saved in environment variables
  cisco.sdwan.restore:
    timeout: 300
    verbose: "INFO"
    workdir: "/home/user/backups"
    regex: ".*"
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
from ansible.module_utils.basic import env_fallback
import logging
from cisco_sdwan.tasks.implementation._restore import (
    TaskRestore,
)
from cisco_sdwan.tasks.utils import (
    existing_file_type
)
from ansible_collections.cisco.sdwan.plugins.module_utils.common import (
    ADDRESS,WORKDIR,REGEX,VERBOSE,
    DRYRUN,TAG,ATTACH,FORCE,
    set_log_level,update_vManage_args,validate_regex,process_task,tag_list,
    get_workdir,get_env_args
)


def main():
    """main entry point for module execution
    """
    argument_spec = dict(
        workdir=dict(type="str"),
        regex=dict(type="str"),
        dryrun=dict(type="bool", default=False),
        attach=dict(type="bool", default=False),
        force=dict(type="bool", default=False),
        tag=dict(type="str", required=True, choices=tag_list),
    )
    update_vManage_args(argument_spec)
    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )
    set_log_level(module.params[VERBOSE])
    log = logging.getLogger(__name__)
    log.debug("Task Restore started.")
        
    result = {"changed": False }
   
    vManage_ip=module.params[ADDRESS]
    workdir = get_workdir(module.params[WORKDIR],vManage_ip)
        
    try:
        existing_file_type(workdir)
    except Exception as ex:
        log.critical(ex)
        module.fail_json(msg=f"Work directory {workdir} not found.")
        
    regex = module.params[REGEX]
    validate_regex(REGEX,regex,module)
    dryrun = module.params[DRYRUN]
    
    task_restore = TaskRestore()
    restore_args = {'workdir':workdir,'regex':regex,'dryrun':dryrun,'attach':module.params[ATTACH],'force':module.params[FORCE],'tag':module.params[TAG]}
    try:
        process_task(task_restore,get_env_args(module),**restore_args)
    except Exception as ex:
        module.fail_json(msg=f"Failed to restore , check the logs for more detaills... {ex}")
    
    log.debug("Task Restore completed successfully.")
    result["changed"] = False if dryrun else True
    result.update(
        {"stdout": "{}Successfully restored files from local {} folder to vManage address {}".format("DRY-RUN mode: " if dryrun else "",workdir,vManage_ip) }
    )
    module.exit_json(**result)

if __name__ == "__main__":
    main()