#!/usr/bin/python
DOCUMENTATION = """
module: cisco.sdwan.show_template
author: Satish Kumar Kamavaram (sakamava@cisco.com)
short_description: Show details about device templates on vManage or from a local backup. Display as table or export as csv file.
description: The Show template task can be used to show device templates from a target vManage,
             or a backup directory. Criteria can contain regular expression with matching
             device or feature template names depending on type of option specified.
             A log file is created under a "logs" directory.
             This "logs" directoryis relative to directory where Ansible runs.
notes: 
- Tested against 20.4.1.1
options: 
  regex:
    description:
    - For values option, regular expression matching device template names.
      For references option, regular expression matching feature template names to include.
    required: false
    type: str
  workdir:
    description:
    - show-template will read from the specified directory instead of target vManage. Either workdir or vManage address/user/password is mandatory
    required: false
    type: str
  csv:
    description:
    - Export tables as csv files under the specified directory
    required: false
    type: str
  name:
    description:
    - Device template name
      For values option, this param is applicable.
    required: false
    type: str
  id:
    description:
    - Device template id
      For values option, this param is applicable.
    required: false
    type: str
  with_refs:
    description:
    - Include only feature-templates with device-template references
      For references option, this param is applicable.
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
- name: Show Template values from local backup directory
  cisco.sdwan.show_template:
    values: 
        regex: ".*"
        workdir: backup_198.18.1.10_20210720
        csv: show_temp
        name: DC-vEdges
        id: 704bbc2f-aa9a-4068-84a2-fc31602ed553
    verbose: DEBUG
    pid: "2"
- name: Show Template values from vManage
  cisco.sdwan.show_template:
    values: 
        regex: ".*"
        csv: show_temp
        name: DC-vEdges
        id: 704bbc2f-aa9a-4068-84a2-fc31602ed553
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
    verbose: DEBUG
    pid: "2"
    timeout: 300
- name: Show Template references from local backup directory
  cisco.sdwan.show_template:
    references: 
        regex: ".*"
        csv: show_temp
        workdir: backup_198.18.1.10_20210720
        with_refs: True
    verbose: DEBUG
    pid: "2"
- name: Show Template references from vManage
  cisco.sdwan.show_template:
    references: 
        regex: ".*"
        csv: show_temp
        with_refs: True
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
    verbose: DEBUG
    pid: "2"
    timeout: 300
"""

RETURN = """
stdout:
  description: Status of Show Template
  returned: always apart from low level errors
  type: str
  sample: 'Task Show-template: values completed successfully.vManage address 198.18.1.10'
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
from cisco_sdwan.tasks.implementation._show_template import (
    TaskShowTemplate
)
from ansible_collections.cisco.sdwan.plugins.module_utils.common import (
    ADDRESS,REGEX,VERBOSE,WORKDIR,CSV,NAME,ID,WITH_REFS,USER,PASSWORD,
    set_log_level,update_vManage_args,process_task,
    validate_filename,validate_regex,validate_existing_file_type,
    validate_non_empty_type,validate_uuid_type
)

sub_task_list = ['values','references']  

def main():
    """main entry point for module execution
    """
    show_base_args = dict(
                regex=dict(type="str",required=False),
                workdir=dict(type="str",required=False),
                csv=dict(type="str",required=False)
        )

    argument_spec = dict(
        values=dict(type="dict",
            options = update_values_option_args(show_base_args)),
        references=dict(type="dict",aliases=["ref"],
            options = update_references_option_args(show_base_args))
    )

    update_vManage_args(argument_spec,False)

    module = AnsibleModule(
        argument_spec=argument_spec, mutually_exclusive=[sub_task_list], required_one_of=[sub_task_list], supports_check_mode=True
    )
    set_log_level(module.params[VERBOSE])
    log = logging.getLogger(__name__)
    log.debug(f"Task Show-template started.")
    result = {"changed": False }
   
    vManage_ip=module.params[ADDRESS]    
    show_args = None
    sub_task_name = None
    if module.params[sub_task_list[0]]:
        sub_task_name = sub_task_list[0] 
        show_common_args = get_show_common_args(module,sub_task_list[0])
        show_args = get_show_values_args(module,sub_task_name,show_common_args)
    elif module.params[sub_task_list[1]]:
        sub_task_name = sub_task_list[1] 
        show_common_args = get_show_common_args(module,sub_task_list[1])
        show_args = get_show_references_args(module,sub_task_name,show_common_args)
            
    show_validations(sub_task_name,module)          
    
    log.debug(f"Task Show-template: {sub_task_name} started.")
    task_output = []
    show_args.update({'task_output':task_output})
    task_show_template = TaskShowTemplate()
    try:
        process_task(task_show_template,module,**show_args)
    except Exception as ex:
        module.fail_json(msg=f"Task Show-template: {sub_task_name} failed , check the logs for more detaills... {ex}")
        
    log.debug(f"Task Show-template: {sub_task_name} completed successfully.")
    if task_output and isinstance(task_output, list) and len(task_output):
        result.update({"stdout": ''.join(task_output)})  
    else:
        result.update(
            {"stdout": "Task Show-template: {} completed successfully. {}".format(sub_task_name,'vManage address '+vManage_ip if vManage_ip else 'Workdir: '+module.params[sub_task_name][WORKDIR])}
        )    
    module.exit_json(**result)


def get_show_common_args(module, sub_task):
    show_common_args = {
                        'regex':module.params[sub_task][REGEX],
                        'csv':module.params[sub_task][CSV],
                        'workdir':module.params[sub_task][WORKDIR]
                    }
    return show_common_args


def get_show_values_args(module,sub_task,show_common_args):
    values_args = {
                        'subtask_info':sub_task,
                        'subtask_handler':TaskShowTemplate.values_table,
                        'name':module.params[sub_task][NAME],
                        'id':module.params[sub_task][ID]
                    }             
    show_common_args.update(values_args)  
    return show_common_args 

def get_show_references_args(module, sub_task, show_common_args):
    ref_args = {
                        'subtask_info':sub_task,
                        'subtask_handler':TaskShowTemplate.references_table,
                        'with_refs':module.params[sub_task][WITH_REFS]
                    }
    show_common_args.update(ref_args)
    return show_common_args    

def update_values_option_args(show_base_args):
    temp_show_base_args = copy.copy(show_base_args)
    temp_show_base_args.update(dict(
                name=dict(type="str",required=False),
                id=dict(type="str",required=False)
            ))
    return temp_show_base_args 

def update_references_option_args(show_base_args): 
    temp_show_base_args = copy.copy(show_base_args)
    temp_show_base_args.update(dict(
                with_refs=dict(type="bool",default=False,aliases=['with-refs'])
            ))
    return temp_show_base_args 
          
def show_validations(sub_task,module):
    validate_regex(REGEX,module.params[sub_task][REGEX],module)
    validate_filename(CSV,module.params[sub_task][CSV],module)
    workdir = module.params[sub_task][WORKDIR]
    validate_existing_file_type(WORKDIR,workdir,module)

    if workdir is None:
        validate_non_empty_type(ADDRESS,module.params[ADDRESS],module)
        validate_non_empty_type(USER,module.params[USER],module)    
        validate_non_empty_type(PASSWORD,module.params[PASSWORD],module)

    if sub_task == sub_task_list[0]:
        validate_uuid_type(ID,module.params[sub_task][ID],module)
    
  
if __name__ == "__main__":
    main()