#!/usr/bin/python

DOCUMENTATION = """
"""

EXAMPLES = """
"""
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import env_fallback
import logging
import copy
from cisco_sdwan.tasks.implementation._list import (
    TaskList
)
from ansible_collections.cisco.sdwan.plugins.module_utils.common import (
    ADDRESS,REGEX,VERBOSE,
    TAGS,CSV,WORKDIR,NAME_REGEX,
    set_log_level,update_vManage_args,process_task,tag_list,
    validate_regex,validate_existing_file_type,validate_filename,
    validate_non_empty_type,validate_ext_template_type
)

sub_task_list = ['configuration','certificate','transform'] 

def main():
    """main entry point for module execution
    """
   
    list_base_args = dict(
                regex=dict(type="str", default=None),
                workdir=dict(type="str", default=None),
                csv=dict(type="str",default=None)
        )

    argument_spec = dict(
        configuration=dict(type="dict",aliases=["config"],
            options = update_configuration_option_args(list_base_args)),
        certificate=dict(type="dict",aliases=["cert"],apply_defaults=True,
            options = list_base_args),
        transform=dict(type="dict",
            options = update_transform_option_args(list_base_args))
    )

    update_vManage_args(argument_spec)
    #Firoz .. what is this?
    argument_spec.update(address=dict(type="str", required=False,fallback=(env_fallback, ['VMANAGE_IP'])))
    
    module = AnsibleModule(
        argument_spec=argument_spec, mutually_exclusive=[sub_task_list], required_one_of=[sub_task_list], supports_check_mode=True
    )
    set_log_level(module.params[VERBOSE])
    log = logging.getLogger(__name__)
        
    result = {"changed": False }
   
    vManage_ip = module.params[ADDRESS]    
    list_args = None
    sub_task_name = None

    if module.params[sub_task_list[0]]:
        sub_task_name = sub_task_list[0]            
        list_common_args = get_list_common_args(module,sub_task_list[0]) 
        list_args = get_list_configuration_args(module,sub_task_name,list_common_args)
    elif module.params[sub_task_list[1]]:
        sub_task_name  = sub_task_list[1]
        list_common_args = get_list_common_args(module,sub_task_list[1])  
        list_args = get_list_certificate_args(sub_task_name,list_common_args)
    elif module.params[sub_task_list[2]]:
        sub_task_name  = sub_task_list[2]
        list_common_args = get_list_common_args(module,sub_task_list[2]) 
        list_args = get_list_transform_args(module,sub_task_name,list_common_args)
  
    list_validations(sub_task_name,module)  
    
    log.debug(f"Task List: {sub_task_name} started.")
    task_output = []
    list_args.update({'task_output':task_output})
    task_list = TaskList()
    try:
        process_task(task_list,module,**list_args)
    except Exception as ex:
        module.fail_json(msg=f"Task List: {sub_task_name} failed , check the logs for more details... {ex}")
        
    log.debug(f"Task List: {sub_task_name} completed successfully.")
    if task_output and isinstance(task_output, list) and len(task_output):
        result.update({"stdout": ''.join(task_output)})
    else:
        result.update(
             {"stdout": "Task List: {} completed successfully. {}".format(sub_task_name,'vManage address '+vManage_ip if vManage_ip else 'Workdir: '+module.params[sub_task_name][WORKDIR]) }
        )    
    module.exit_json(**result)


def get_list_common_args(module, sub_task):
    list_common_args = {
                        'regex':module.params[sub_task][REGEX],
                        'workdir':module.params[sub_task][WORKDIR],
                        'csv':module.params[sub_task][CSV]
                    }
    return list_common_args


def get_list_configuration_args(module, sub_task, list_common_args):
    config_args = {
                        'subtask_info':f'list {sub_task}',
                        'subtask_handler':TaskList.config_table,
                        'tags':module.params[sub_task][TAGS]
                    }             
    list_common_args.update(config_args)  
    return list_common_args 

def get_list_certificate_args(sub_task, list_common_args):
    certificate_args = {
                        'subtask_info':f'list {sub_task}s',
                        'subtask_handler':TaskList.cert_table
                    }
    list_common_args.update(certificate_args)
    return list_common_args    

def get_list_transform_args(module, sub_task, list_common_args):
    transform_args = {
                    'subtask_info':'test name-regex',
                    'subtask_handler':TaskList.xform_table,
                    'tags':module.params[sub_task][TAGS],
                    'name_regex':module.params[sub_task][NAME_REGEX]
                }
    list_common_args.update(transform_args)
    return list_common_args          

def update_configuration_option_args(list_base_args):
    temp_list_base_args = copy.copy(list_base_args)
    temp_list_base_args.update(dict(
                tags=dict(type="list", elements="str", required=True,choices=tag_list),
            ))
    return temp_list_base_args         

def update_transform_option_args(list_base_args):
    temp_list_base_args = copy.copy(list_base_args)
    temp_list_base_args.update(dict(
                tags=dict(type="list", elements="str", required=True,choices=tag_list),
                name_regex=dict(type="str",required=True)
            ))
    return temp_list_base_args  

def list_validations(sub_task,module):
    regex = module.params[sub_task][REGEX]
    validate_regex(REGEX,regex,module)
    csv = module.params[sub_task][CSV]
    validate_filename(CSV,csv,module)
    workdir = module.params[sub_task][WORKDIR]
    validate_existing_file_type(WORKDIR,workdir,module)

    if workdir is None: 
        validate_non_empty_type(ADDRESS,module.params[ADDRESS],module)

    if sub_task == sub_task_list[2]:
        name_regex = module.params[sub_task][NAME_REGEX]
        validate_ext_template_type(NAME_REGEX,name_regex,module)

if __name__ == "__main__":
    main()