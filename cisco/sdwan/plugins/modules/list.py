#!/usr/bin/python

DOCUMENTATION = """
module: cisco.sdwan.list
author: Satish Kumar Kamavaram (sakamava@cisco.com)
short_description: List configuration items or device certificate information from vManage or a local backup. Display as table or export as csv file.
description: The list task can be used to show items from a target vManage,
             or a backup directory. Matching criteria can contain item tag(s) 
             and regular expression.When multiple filters are defined, the result 
             is an AND of all filters.A log file is created under a "logs" directory.
             This "logs" directoryis relative to directory where Ansible runs.
notes: 
- Tested against 20.4.1.1
options: 
  regex:
    description:
    - For configuration option, regular expression selecting items to list. Match on item names or item IDs.
      For certificate option,  regular expression selecting devices to list. Match on hostname or chassis/uuid. Use "^-$" to match devices without a hostname.
      For transform option, regular expression selecting items to list, match on original item names
    required: false
    type: str
  workdir:
    description:
    - list will read from the specified directory instead of target vManage. Either workdir or vManage address/user/password is mandatory
    required: false
    type: str
  csv:
    description:
    - Export table as a csv file
    required: false
    type: str
  tags:
    description:
    - Defines one or more tags for selecting groups of items. Multiple tags should be
      configured as list. Available tags are template_feature, policy_profile, policy_definition,
      all, policy_list, policy_vedge, policy_voice, policy_vsmart, template_device, policy_security,
      policy_customapp. Special tag "all" selects all items, including WAN edge certificates and 
      device configurations.
      For configuration option, this param is mandatory.
      For transform option, this param is mandatory.
    required: false
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
  name_regex:
    description:
    - name-regex used to transform an existing item name. Variable {name} is
      replaced with the original template name. Sections of the original template
      name can be selected using the {name <regex>} format. Where  is a
      regular expression that must contain at least one capturing group. Capturing
      groups identify sections of the original name to keep.
      For transform option, this param is mandatory.
    required: false
    type: str
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
- name: List Configuration
  cisco.sdwan.list:
    configuration: 
        tags:
            - template_feature
            - policy_vedge
        regex: ".*"
        workdir: backup_198.18.1.10_20210720 
        csv: csvtest.csv
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
    timeout: 300
    pid: "2"
    verbose: DEBUG
- name: List Certificate
  cisco.sdwan.list:
    certificate:
        regex: ".*"
        workdir: backup_198.18.1.10_20210720
        csv: list_cert.csv
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
    timeout: 300
    pid: "2"
    verbose: DEBUG
- name: List Transform
  cisco.sdwan.list:
    transform: 
        tags:
            - template_feature
        name_regex: '{name}'
        regex: ".*"
        workdir: backup_198.18.1.10_20210720
        csv: csvtest.csv
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
  description: Status of list
  returned: always apart from low level errors
  type: str
  sample: 'Task List: configuration completed successfully.vManage address 198.18.1.10'
stdout_lines:
  description: The value of stdout split into a list
  returned: always apart from low level errors
  type: list
  sample: show table view data
"""
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import env_fallback
import logging
import copy
from cisco_sdwan.tasks.implementation._list import (
    TaskList
)
from ansible_collections.cisco.sdwan.plugins.module_utils.common import (
    ADDRESS,REGEX,VERBOSE,USER,PASSWORD,
    TAGS,CSV,WORKDIR,NAME_REGEX,
    set_log_level,update_vManage_args,process_task,tag_list,
    validate_regex,validate_existing_file_type,validate_filename,
    validate_non_empty_type,validate_ext_template_type
)

sub_task_list = ['configuration','transform','certificate'] 

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

    update_vManage_args(argument_spec,False)

    module = AnsibleModule(
        argument_spec=argument_spec, mutually_exclusive=[sub_task_list], required_one_of=[sub_task_list], supports_check_mode=True
    )
    set_log_level(module.params[VERBOSE])
    log = logging.getLogger(__name__)
    log.debug(f"Task List started.")
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
        list_args = get_list_transform_args(module,sub_task_name,list_common_args)
    elif module.params[sub_task_list[2]]:
        sub_task_name  = sub_task_list[2]
        list_common_args = get_list_common_args(module,sub_task_list[2]) 
        list_args = get_list_certificate_args(sub_task_name,list_common_args)
  
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
    validate_regex(REGEX,module.params[sub_task][REGEX],module)
    validate_filename(CSV,module.params[sub_task][CSV],module)
    workdir = module.params[sub_task][WORKDIR]
    validate_existing_file_type(WORKDIR,workdir,module)

    if workdir is None: 
        validate_non_empty_type(ADDRESS,module.params[ADDRESS],module)
        validate_non_empty_type(USER,module.params[USER],module)    
        validate_non_empty_type(PASSWORD,module.params[PASSWORD],module)     

    if sub_task == sub_task_list[1]:
        validate_ext_template_type(NAME_REGEX,module.params[sub_task][NAME_REGEX],module)

if __name__ == "__main__":
    main()