#!/usr/bin/python

DOCUMENTATION = """
module: cisco.sdwan.attach
author: Satish Kumar Kamavaram (sakamava@cisco.com)
short_description: Attach WAN Edges/vSmarts to templates. Allows further customization on top of the functionality available via "restore --attach".
description: This attach module connects to SD-WAN vManage using HTTP REST to 
             updated configuration data stored in local default backup or configured argument
             local backup folder. This module contains multiple arguments with 
             connection and filter details to attach WAN Edges/vSmarts to templates.
             When multiple filters are defined, the result is an AND of all filters. 
             Dry-run can be used to validate the expected outcome.The number of devices to include 
             per attach request (to vManage) can be defined with the batch param.
             A log file is created under a "logs" directory. This "logs" directory
             is relative to directory where Ansible runs.
notes: 
- Tested against 20.4.1.1
options: 
  device_type:
    description:
    - Select type of devices to attach templates. Available types are edge,vsmart
    required: true
    type: str
    choices:
    - "edge"
    - "vsmart"
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
  templates:
    description:
    - Regular expression selecting templates to attach. Match on template name.
    required: false
    type: str
  devices:
    description:
    - Regular expression selecting devices to attach. Match on device name.
    required: false
    type: str
  reachable:
    description:
    - Select reachable devices only.
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
  dryrun:
    description:
    - dry-run mode. Attach operations are listed but not is pushed to vManage.
    required: false
    type: bool
    default: False
  batch:
    description:
    - Maximum number of devices to include per vManage attach request.
    required: false
    type: int
    default: 200
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
- name: "Attach vManage configuration"
  cisco.sdwan.attach:
    address: "198.18.1.10"
    port: 8443
    user: "admin"
    password:"admin"
    timeout: 300
    pid: "2"
    verbose: "DEBUG"
    device_type: "edge"
    workdir: "/home/user/backups"
    templates: ".*"
    devices: ".*"
    reachable: True
    site: "1"
    system_ip: "12.12.12.12"
    dryrun: False
    batch: 99       
- name: "Attach vManage configuration with some vManage config arguments saved in environment variables"
  cisco.sdwan.attach: 
    timeout: 300
    verbose: INFO
    workdir: /home/user/backups
    device_type: "edge"
    workdir: "/home/user/backups"
    templates: ".*"
    devices: ".*"
    reachable: True
    site: "1"
    system_ip: "12.12.12.12"
    dryrun: True
    batch: 99    
- name: "Attach vManage configuration with all defaults"
  cisco.sdwan.attach: 
    address: "198.18.1.10"
    user: admin
    password: admin
    device_type: "edge"
"""

RETURN = """
stdout:
  description: Status of attach
  returned: always apart from low level errors
  type: str
  sample: 'Successfully attached files from local backup_198.18.1.10_20210707 folder to vManage address 198.18.1.10'
stdout_lines:
  description: The value of stdout split into a list
  returned: always apart from low level errors
  type: list
  sample: ['Successfully attached files from local backup_198.18.1.10_20210707 folder to vManage address 198.18.1.10']
"""

from ansible.module_utils.basic import AnsibleModule
import logging
from cisco_sdwan.tasks.implementation._attach_detach import (
    DEFAULT_BATCH_SIZE,TaskAttach,
)
from cisco_sdwan.tasks.utils import (
    existing_file_type,
)
from cisco_sdwan.base.models_vmanage import (
  DeviceTemplateIndex,
)
from  ansible_collections.cisco.sdwan.plugins.module_utils.common import (
    ADDRESS,WORKDIR,VERBOSE,TEMPLATES,DEVICES,SITE,
    SYSTEM_IP,DRYRUN,BATCH,REACHABLE,DEVICE_TYPE,
    set_log_level,update_vManage_args,process_task,get_workdir,
    attach_detach_device_types,attach_detach_validations,
)

def main():
    """main entry point for module execution
    """
    argument_spec = dict(
        device_type=dict(type="str", required=True, choices=attach_detach_device_types),
        workdir=dict(type="str"),
        templates=dict(type="str"),
        devices=dict(type="str"),
        reachable=dict(type="bool", default=False),
        site=dict(type="str"),
        system_ip=dict(type="str"),
        dryrun=dict(type="bool", default=False),
        batch=dict(type=int, default=DEFAULT_BATCH_SIZE),
    )
    update_vManage_args(argument_spec)
    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )
    
    set_log_level(module.params[VERBOSE])
    log = logging.getLogger(__name__)
    log.debug("Task Attach started.")
    
    result = {"changed": False }
   
    vManage_ip=module.params[ADDRESS]
    workdir = get_workdir(module.params[WORKDIR],vManage_ip)
    
    try:
        existing_file_type(workdir)
    except Exception as ex:
        log.critical(ex)
        module.fail_json(msg=f"Work directory {workdir} not found.")
    
    attach_detach_validations(module)
    dryrun = module.params[DRYRUN]
    default_args = getDefaults(module.params[DEVICE_TYPE])
    
    task_attach = TaskAttach()
    attach_args = {'workdir':workdir,'templates':module.params[TEMPLATES],'devices':module.params[DEVICES],'reachable':module.params[REACHABLE],'site':module.params[SITE],'system_ip':module.params[SYSTEM_IP],'dryrun':dryrun,'batch':module.params[BATCH]}
    attach_args.update(default_args)
    try:
        process_task(task_attach,module,**attach_args)
    except Exception as ex:
        module.fail_json(msg=f"Failed to attach , check the logs for more detaills... {ex}")
  
    log.debug("Task Attach completed successfully.")
    result["changed"] = False if dryrun else True
    result.update(
        {"stdout": "{}Successfully attached files from local {} folder to vManage address {}".format("DRY-RUN mode: " if dryrun else "",workdir,vManage_ip) }
    )
    module.exit_json(**result)

def getDefaults(device_type):
      if device_type == attach_detach_device_types[0]:
            return {'template_filter': DeviceTemplateIndex.is_not_vsmart,'device_set':TaskAttach.edge_set,'set_title':'WAN Edges'}
      elif device_type == attach_detach_device_types[1]:
            return {'template_filter': DeviceTemplateIndex.is_vsmart,'device_set':TaskAttach.vsmart_set,'set_title':'vSmarts'}
      
if __name__ == "__main__":
    main()