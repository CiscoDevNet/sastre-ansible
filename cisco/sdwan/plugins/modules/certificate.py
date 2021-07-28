#!/usr/bin/python

DOCUMENTATION = """

"""

EXAMPLES = """
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
    validate_existing_file_type
)

sub_task_list = ['restore','set']  

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
        
    result = {"changed": False }
   
    vManage_ip = module.params[ADDRESS]    
    cert_args = None
    sub_task_name = None

    if module.params[sub_task_list[0]]:
        sub_task_name = sub_task_list[0] 
        cert_common_args = get_cert_common_args(module,sub_task_list[0])
        cert_args = get_cert_restore_args(module,sub_task_name,cert_common_args)
    elif module.params[sub_task_list[1]]:
        sub_task_name  = sub_task_list[1]              
        cert_common_args = get_cert_common_args(module,sub_task_list[1])  
        cert_args = get_cert_set_args(module,sub_task_name,cert_common_args)
 
    certificate_validations(sub_task_name,module)        

    log.debug(f"Task Certificate: {sub_task_name} started.")
    task_certificate = TaskCertificate()
    try:
        process_task(task_certificate,module,**cert_args)
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
    regex = module.params[sub_task][REGEX]
    validate_regex(REGEX,regex,module)
    if sub_task == sub_task_list[0]:
        workdir = module.params[sub_task][WORKDIR]
        validate_existing_file_type(WORKDIR,get_workdir(workdir,module.params[ADDRESS]),module)

if __name__ == "__main__":
    main()