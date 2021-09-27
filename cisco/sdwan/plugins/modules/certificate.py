#!/usr/bin/python

DOCUMENTATION = """
module: certificate
author: Satish Kumar Kamavaram (sakamava@cisco.com)
short_description: Restore device certificate validity status from a backup or set to a desired value (i.e. valid, invalid or staging).
description: The certificate task can be used to items from backup directory or to a
             set of desired value to target vManage. Matching criteria can contain 
             regular expression.A log file is created under a "logs" directory.
             This "logs" directoryis relative to directory where Ansible runs.
notes: 
- Tested against 20.4.1.1
options: 
  regex:
    description:
    - Regular expression selecting devices to modify certificate status. Matches on
      the hostname or chassis/uuid. Use "^-$" to match devices without a hostname.'
    required: false
    type: str
  dryrun:
    description:
    - dry-run mode. List modifications that would be performed without pushing changes to vManage.
    required: false
    type: bool
    default: False
  workdir:
    description:
    - restore source from default or specified location
      For restore option, this param is mandatory.
    required: false
    type: str
  status:
    description:
    - WAN edge certificate status
      For set option, this param is mandatory.
    required: false
    type: str
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
- name: Certificate Set
  cisco.sdwan.certificate:
    set:
        status: valid
        regex: ".*"
        dryrun: True
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
    timeout: 300
    pid: "2"
    verbose: DEBUG
- name: Certificate restore
  cisco.sdwan.certificate:
    restore:
        regex: ".*"
        workdir: backup_198.18.1.10_20210720
        dryrun: True
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
    timeout: 300
    pid: "2"
    verbose: DEBUG
"""

RETURN = """
stdout:
  description: Status of Certificate
  returned: always apart from low level errors
  type: str
  sample: 'Task Certificate: restore completed successfully.vManage address 198.18.1.10'
stdout_lines:
  description: The value of stdout split into a list
  returned: always apart from low level errors
  type: list
  sample: ['Task Certificate: restore completed successfully.vManage address 198.18.1.10']
"""
from sys import modules
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import env_fallback
import logging
import copy
from cisco_sdwan.tasks.implementation._certificate import (
    TaskCertificate
)
from ansible_collections.cisco.sdwan.plugins.module_utils.common import (
    ADDRESS,REGEX,VERBOSE,
    DRYRUN,STATUS,WORKDIR,
    set_log_level,update_vManage_args,process_task,
    get_workdir,validate_regex,
    validate_existing_file_type,get_env_args
)

sub_task_list = ['set','restore']  

def main():
    """main entry point for module execution
    """
  
    cert_base_args = dict(
        regex=dict(type="str", default=None),
        dryrun=dict(type="bool", default=False)
    )

    argument_spec = dict(
        restore=dict(type="dict",apply_defaults=True, options = update_restore_option_args(cert_base_args)),
        set=dict(type="dict",options = update_set_option_args(cert_base_args))
    )

    update_vManage_args(argument_spec)
    
    module = AnsibleModule(
        argument_spec=argument_spec, mutually_exclusive=[sub_task_list], required_one_of=[sub_task_list], supports_check_mode=True
    )
    set_log_level(module.params[VERBOSE])
    log = logging.getLogger(__name__)
    log.debug(f"Task Certificate started.")
    result = {"changed": False }
   
    vManage_ip = module.params[ADDRESS]    
    cert_args = None
    sub_task_name = None

    if module.params[sub_task_list[0]]:
        sub_task_name = sub_task_list[0] 
        cert_common_args = get_cert_common_args(module,sub_task_list[0])
        cert_args = get_cert_set_args(module,sub_task_name,cert_common_args)
    elif module.params[sub_task_list[1]]:
        sub_task_name  = sub_task_list[1]              
        cert_common_args = get_cert_common_args(module,sub_task_list[1])  
        cert_args = get_cert_restore_args(module,sub_task_name,cert_common_args)
        
 
    certificate_validations(sub_task_name,module)        

    log.debug(f"Task Certificate: {sub_task_name} started.")
    task_certificate = TaskCertificate()
    try:
        process_task(task_certificate,get_env_args(module),**cert_args)
    except Exception as ex:
        module.fail_json(msg=f"Task Certificate: {sub_task_name} failed , check the logs for more details... {ex}")
        
    log.debug(f"Task Certificate: {sub_task_name} completed successfully.")
    
    dryrun = module.params[sub_task_name][DRYRUN]
    result["changed"] = False if dryrun else True
    result.update(
            {"stdout": "Task Certificate: {} completed successfully.vManage address {}".format("DRY-RUN mode: " if dryrun else ""+sub_task_name,vManage_ip) }
    )    
    module.exit_json(**result)


def get_cert_common_args(module, sub_task):
    cert_common_args = {
                        'command':sub_task,
                        'regex':module.params[sub_task][REGEX],
                        'dryrun':module.params[sub_task][DRYRUN]
                        }
    return cert_common_args


def get_cert_restore_args(module, sub_task, cert_common_args):
    workdir = module.params[sub_task][WORKDIR]
    restore_args = {
                    'workdir': get_workdir(workdir,module.params[ADDRESS]),
                    'source_iter':TaskCertificate.restore_iter
                    }                           
    cert_common_args.update(restore_args)
    return cert_common_args 


def get_cert_set_args(module, sub_task, cert_common_args):
    restore_args = {
                    'status':module.params[sub_task][STATUS],
                    'source_iter':TaskCertificate.set_iter
                    }             
    cert_common_args.update(restore_args)  
    return cert_common_args

def update_restore_option_args(cert_base_args):
    temp_cert_base_args = copy.copy(cert_base_args)
    temp_cert_base_args.update(dict(
                workdir=dict(type="str")
            ))
    return temp_cert_base_args         

def update_set_option_args(cert_base_args):
    temp_set_base_args = copy.copy(cert_base_args)
    temp_set_base_args.update(dict(
                status=dict(type="str", required=True, choices=['invalid', 'staging', 'valid'])
            ))
    return temp_set_base_args  

def certificate_validations(sub_task,module):
    validate_regex(REGEX,module.params[sub_task][REGEX],module)
    if sub_task == sub_task_list[1]:
        workdir = module.params[sub_task][WORKDIR]
        validate_existing_file_type(WORKDIR,get_workdir(workdir,module.params[ADDRESS]),module)

if __name__ == "__main__":
    main()