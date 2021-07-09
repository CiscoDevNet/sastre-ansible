#!/usr/bin/python

DOCUMENTATION = """
module: cisco.sdwan.delete
author: Satish Kumar Kamavaram (sakamava@cisco.com)
short_description: Delete configuration items on SD-WAN vManage.
description: This delete module connects to SD-WAN vManage using HTTP REST to 
             delete configuration items. This module contains multiple arguments with 
             connection and filter details to delete all or specific configurtion data.
             A log file is created under a "logs" directory. This "logs" directory
             is relative to directory where Ansible runs.
notes: 
- Tested against 20.4.1.1
options: 
  regex:
    description:
    - Regular expression matching item names to be deleted, within selected tags
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
- name: "Delete vManage configuration"
  cisco.sdwan.delete: 
    address: "198.18.1.10"
    port: 8443
    user: admin
    password: admin
    timeout: 300
    pid: "2"
    verbose: INFO
    regex: ".*"
    dryrun: True
    detach: False
    tag: "template_device"
- name: "Delete vManage configuration with some vManage config arguments saved in environment variables"
  cisco.sdwan.delete: 
    timeout: 300
    verbose: INFO
    regex: ".*"
    dryrun: True
    detach: False
    tag: "all"
- name: "Delete vManage configuration with all defaults"
  cisco.sdwan.delete: 
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
  sample: 'Delete completed successfully.vManage address 198.18.1.10'
stdout_lines:
  description: The value of stdout split into a list
  returned: always apart from low level errors
  type: list
  sample: ['Delete completed successfully.vManage address 198.18.1.10']
"""
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import env_fallback
import logging
from cisco_sdwan.tasks.implementation._delete import (
    TaskDelete,
)
from ansible_collections.cisco.sdwan.plugins.module_utils.common import (
    ADDRESS,REGEX,VERBOSE,
    DRYRUN,TAG,DETACH,
    set_log_level,update_vManage_args,validate_regex,process_task,tag_list,
)


def main():
    """main entry point for module execution
    """
    argument_spec = dict(
        regex=dict(type="str"),
        dryrun=dict(type="bool", default=False),
        detach=dict(type="bool", default=False),
        tag=dict(type="str", required=True, choices=tag_list)
    )
    update_vManage_args(argument_spec)
    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )
    set_log_level(module.params[VERBOSE])
    log = logging.getLogger(__name__)
    log.debug("Task Delete started.")
        
    result = {"changed": False }
   
    vManage_ip=module.params[ADDRESS]
    regex = module.params[REGEX]
    validate_regex(REGEX,regex,module)
    dryrun = module.params[DRYRUN]
    
    task_delete = TaskDelete()
    delete_args = {'regex':regex,'dryrun':dryrun,'detach':module.params[DETACH],'tag':module.params[TAG]}
    try:
        process_task(task_delete,module,**delete_args)
    except Exception as ex:
        module.fail_json(msg=f"Failed to delete , check the logs for more detaills... {ex}")
        
    log.debug("Task Delete completed successfully.")
    result["changed"] = False if dryrun else True
    result.update(
        {"stdout": "{}Delete completed successfully.vManage address {}".format("DRY-RUN mode: " if dryrun else "", vManage_ip) }
    )
    module.exit_json(**result)

if __name__ == "__main__":
    main()