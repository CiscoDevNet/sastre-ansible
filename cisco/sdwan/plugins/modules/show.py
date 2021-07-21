#!/usr/bin/python

DOCUMENTATION = """
module: cisco.sdwan.show
author: Satish Kumar Kamavaram (sakamava@cisco.com)
short_description: Run vManage real-time, state or statistics commands; collecting data from one or more devices.
description: This show module connects to SD-WAN vManage using HTTP REST to 
             retrieve different data.This module contains multiple arguments with 
             connection and filter details to retrieve devices,realtime,state,
             statistics data.The retrieved data will be displayed to console in table
             format or can be exported as csv files under the specified directory defined
             in csv param.When multiple filters are defined, the result is an AND of all filters.
             A log file is created under a "logs" directory. This "logs" directoryis relative 
             to directory where Ansible runs.
notes: 
- Tested against 20.4.1.1
options: 
  regex:
    description:
    - Regular expression matching device name, type or model to display
    required: false
    type: str
  reachable:
    description:
    - Display only reachable devices
    required: false
    type: bool
    default: False
  site:
    description:
    - Select devices with site ID.
    required: false
    type: str
  system_ip:
    description:
    - Select device with system IP.
    required: false
    type: str
  csv:
    description:
    - Export results as csv files under the specified directory
    required: false
    type: str
  detail:
    description:
    - Detailed output. Applicable to only realtime,state,statistics options
    required: false
    type: bool
    default: False
  cmds:
    description:
    - group of, or specific command to execute. Applicable to only realtime,state,statistics options
      For realtime , Group options are all, app-route, bfd, control, dpi, interface, omp, software, system, tunnel.
                     Command options are app-route sla-class, app-route stats, bfd sessions, control connections, 
                                      control local-properties, dpi summary, interface info, omp adv-routes, 
                                      omp peers, omp summary, software info, system status, tunnel stats.
      For state , Group options are all, bfd, control, interface, omp, system. 
                  Command options are bfd sessions, control connections, control local-properties, interface cedge,
                                   interface vedge, omp peers, system info.
      For statistics , Group options are all, app-route, interface, system. 
                       Command options are app-route stats, interface info, system status.
    required: true
    type: list
  days:
    description: 
    - Query statistics from <days> ago (default is now). Applicable to only statistics option
    required: false
    type: int
    default: 0
  hours:
    description: 
    - Query statistics from <hours> ago (default is now). Applicable to only statistics option
    required: false
    type: int
    default: 0
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
- name: Show Devices data
  cisco.sdwan.show:
    devices:
        regex: ".*"
        reachable: true
        site: "100"
        system_ip: 10.1.0.2
        csv: test
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
    timeout: 300
    pid: "2"
    verbose: DEBUG
- name: Show RealTime data
  cisco.sdwan.show:
    realtime:
        regex: ".*"
        cmds:
            - all
        detail: true
        reachable: true
        site: "100"
        system_ip: 11.0.2.1
        csv: test123
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
    timeout: 300
    pid: "2"
    verbose: DEBUG 
- name: Show State data
  cisco.sdwan.show:
    state:
        regex: ".*"
        cmds:
            - all
        detail: true
        reachable: true
        site: "100"
        system_ip: 11.0.2.1
        csv: test123
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
    timeout: 300
    pid: "2"
    verbose: DEBUG 
- name: Show Statistics data
  cisco.sdwan.show:
    statistics:
        regex: ".*"
        cmds:
            - all
        detail: true
        reachable: true
        site: "100"
        system_ip: 11.0.2.1
        csv: test123
        days: 0
        hours: 0
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
  description: Status of show
  returned: always apart from low level errors
  type: str
  sample: 'Task Show: state completed successfully.vManage address 198.18.1.10'
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
from cisco_sdwan.tasks.implementation._show import (
    TaskShow,
)
from cisco_sdwan.tasks.utils import (
    OpType,RTCmdSemantics,StateCmdSemantics,
    StatsCmdSemantics
)
from ansible_collections.cisco.sdwan.plugins.module_utils.common import (
    ADDRESS,REGEX,VERBOSE,REACHABLE,SITE,SYSTEM_IP,CSV,CMDS,DETAIL,DAYS,HOURS,
    set_log_level,update_vManage_args,process_task,validate_time,
    validate_filename,validate_regex,validate_site,validate_ipv4,
)

sub_task_list = ['devices','realtime','state','statistics']  

def main():
    """main entry point for module execution
    """
    show_base_args = dict(
                regex=dict(type="str", default=None),
                reachable=dict(type="bool", default=False),
                site=dict(type="str",required=False),
                system_ip=dict(type="str",required=False),
                csv=dict(type="str",required=False)
        )

    argument_spec = dict(
        devices=dict(type="dict",aliases=["dev"],
            options = show_base_args),
        realtime=dict(type="dict",aliases=["rt"],
            options = update_realtime_option_args(show_base_args)),
        state=dict(type="dict",aliases=["st"],
            options = update_state_option_args(show_base_args)),
        statistics=dict(type="dict",aliases=["stats"],
            options = update_statistics_option_args(show_base_args))
    )

    update_vManage_args(argument_spec)
    
    module = AnsibleModule(
        argument_spec=argument_spec, mutually_exclusive=[sub_task_list], required_one_of=[sub_task_list], supports_check_mode=True
    )
    set_log_level(module.params[VERBOSE])
    log = logging.getLogger(__name__)
        
    result = {"changed": False }
   
    vManage_ip=module.params[ADDRESS]    
    show_args = None
    sub_task_name = None
           
    if module.params[sub_task_list[0]]:
        sub_task_name = sub_task_list[0] 
        show_common_args = get_show_common_args(module,sub_task_list[0])
        show_args = get_show_devices_args(sub_task_name,show_common_args)
    
    if module.params[sub_task_list[1]]:
        sub_task_name = sub_task_list[1] 
        show_common_args = get_show_common_args(module,sub_task_list[1])
        show_args = get_show_realtime_args(module,sub_task_name,show_common_args)
    
    if module.params[sub_task_list[2]]:
        sub_task_name = sub_task_list[2] 
        show_common_args = get_show_common_args(module,sub_task_list[2])
        show_args = get_show_state_args(module,sub_task_name,show_common_args)
    
    if module.params[sub_task_list[3]]:
        sub_task_name = sub_task_list[3] 
        show_common_args = get_show_common_args(module,sub_task_list[3])
        show_args = get_show_statistics_args(module,sub_task_name,show_common_args)
            
    show_validations(sub_task_name,module)          
   
    log.debug(f"Task Show: {sub_task_name} started.")
    task_output = []
    show_args.update({'task_output':task_output})
    task_show = TaskShow()
    try:
        process_task(task_show,module,**show_args)
    except Exception as ex:
        module.fail_json(msg=f"Task Show: {sub_task_name} failed , check the logs for more detaills... {ex}")
        
    log.debug(f"Task Show: {sub_task_name} completed successfully.")
    if task_output and isinstance(task_output, list) and len(task_output):
        result.update({"stdout": ''.join(task_output)})  
    else:
        result.update(
            {"stdout": "Task Show: {} completed successfully.vManage address {}".format(sub_task_name,vManage_ip) }
        )    
    module.exit_json(**result)


def get_show_common_args(module, sub_task):
    show_common_args = {
                        'regex':module.params[sub_task][REGEX],
                        'reachable':module.params[sub_task][REACHABLE],
                        'site':module.params[sub_task][SITE],
                        'system_ip':module.params[sub_task][SYSTEM_IP],
                        'csv':module.params[sub_task][CSV]
                    }
    return show_common_args


def get_show_devices_args(sub_task,show_common_args):
    devices_args = {
                        'subtask_info':sub_task,
                        'subtask_handler':TaskShow.devices
                    }             
    show_common_args.update(devices_args)  
    return show_common_args 

def get_show_realtime_args(module, sub_task, show_common_args):
    realtime_args = {
                        'subtask_info':sub_task,
                        'subtask_handler':TaskShow.realtime,
                        'cmds':module.params[sub_task][CMDS],
                        'detail':module.params[sub_task][DETAIL]
                    }
    show_common_args.update(realtime_args)
    return show_common_args    

def get_show_state_args(module, sub_task, show_common_args):
    state_args = {
                    'subtask_info':sub_task,
                    'subtask_handler':TaskShow.bulk_state,
                    'cmds':module.params[sub_task][CMDS],
                    'detail':module.params[sub_task][DETAIL]
                }
    show_common_args.update(state_args)
    return show_common_args        

def get_show_statistics_args(module, sub_task, show_common_args):
    statistics_args = {
                        'subtask_info':sub_task,
                        'subtask_handler':TaskShow.bulk_stats,
                        'days':module.params[sub_task][DAYS],
                        'hours':module.params[sub_task][HOURS],
                        'cmds':module.params[sub_task][CMDS],
                        'detail':module.params[sub_task][DETAIL]
                    }
    show_common_args.update(statistics_args)
    return show_common_args    

def update_realtime_option_args(show_base_args):
    return update_common_args(show_base_args)         

def update_state_option_args(show_base_args):
   return update_common_args(show_base_args)   

def update_statistics_option_args(show_base_args):
    common_args = update_common_args(show_base_args)  
    temp_show_base_args = copy.copy(common_args)
    temp_show_base_args.update(dict(
                days=dict(type="int",default=0),
                hours=dict(type="int",default=0)
            ))
    return temp_show_base_args 

def update_common_args(show_base_args):
    temp_show_base_args = copy.copy(show_base_args)
    temp_show_base_args.update(dict(
                cmds=dict(type="list", elements="str",required=True),
                detail=dict(type="bool",default=False)
            ))
    return temp_show_base_args

def validate_show_cmds(cmds_arg,values,op_type,module):
    if values is not None:
        try:  
          if op_type == OpType.RT:
            cmd_obj = RTCmdSemantics(values,cmds_arg)
            cmd_obj.__call__(object,cmd_obj,values)
          elif op_type == OpType.STATE:
            cmd_obj = StateCmdSemantics(values,cmds_arg)
            cmd_obj.__call__(object,cmd_obj,values)
          elif op_type == OpType.STATS:
            cmd_obj = StatsCmdSemantics(values,cmds_arg)
            cmd_obj.__call__(object,cmd_obj,values)   
        except Exception as ex:
          logging.getLogger(__name__).critical(ex)
          module.fail_json(msg=f'{cmds_arg}: Invalid value(s): {values}:{ex}')  
          
def show_validations(sub_task,module):
    regex = module.params[sub_task][REGEX]
    validate_regex(REGEX,regex,module)
    site= module.params[sub_task][SITE]
    validate_site(SITE,site,module)
    system_ip= module.params[sub_task][SYSTEM_IP]
    validate_ipv4(SYSTEM_IP,system_ip,module)
    csv= module.params[sub_task][CSV]
    validate_filename(CSV,csv,module)
    
    op_type = None
    if sub_task == sub_task_list[1]:
        op_type = OpType.RT
    elif sub_task == sub_task_list[2]:    
        op_type = OpType.STATE
    elif sub_task == sub_task_list[3]:
        op_type = OpType.STATS
        days= module.params[sub_task][DAYS]
        validate_time(DAYS,days,module)
        hours= module.params[sub_task][HOURS]
        validate_time(HOURS,hours,module)

    if sub_task != sub_task_list[0]:
        validate_show_cmds(CMDS,module.params[sub_task][CMDS],op_type,module)  

if __name__ == "__main__":
    main()