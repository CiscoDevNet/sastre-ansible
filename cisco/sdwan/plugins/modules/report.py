#!/usr/bin/python
DOCUMENTATION = """
module: cisco.sdwan.report
author: Satish Kumar Kamavaram (sakamava@cisco.com)
short_description: Generate a report file containing the output from all list and show-template commands.
description: This report module generates report from local backup directory
             or from vManage and saves to local file.
             A log file is created under a "logs" directory. This "logs" directory
             is relative to directory where Ansible runs.
notes: 
- Tested against 20.4.1.1
options: 
  workdir:
    description: 
    - Report will read from the specified directory instead of target vManage. Either workdir or address/user/password is mandatory
    required: false
    type: str
  file:
    description: 
    - report filename (default: report_{current_date}.txt)
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
- name: Report from vManage
  cisco.sdwan.report:
    file: todays_report.txt
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
    verbose: DEBUG
    pid: "2"
    timeout: 300
- name: Report from local folder
  cisco.sdwan.report:
    workdir: backup_198.18.1.10_20210726
    file: todays_report.txt
    verbose: DEBUG
    pid: "2"
"""

RETURN = """
stdout:
  description: Status of report
  returned: always apart from low level errors
  type: str
  sample: 'Successfully Report saved as report_20210802.txt'
stdout_lines:
  description: The value of stdout split into a list
  returned: always apart from low level errors
  type: list
  sample: ['Successfully Report saved as report_20210802.txt']
"""
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import env_fallback
import logging
from datetime import date
from cisco_sdwan.tasks.implementation._report import (
    TaskReport
)
from  ansible_collections.cisco.sdwan.plugins.module_utils.common import (
    ADDRESS,WORKDIR,VERBOSE,FILE,USER,PASSWORD,
    set_log_level,update_vManage_args,validate_filename,process_task,
    validate_existing_file_type,validate_non_empty_type
)


def main():
    """main entry point for module execution
    """
    argument_spec = dict(
        workdir=dict(type="str"),
        file=dict(type="str", default=f'report_{date.today():%Y%m%d}.txt')
    )
    update_vManage_args(argument_spec,False)
    
    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )
    
    set_log_level(module.params[VERBOSE])
    log = logging.getLogger(__name__)
    log.debug("Task Report started.")
    
    result = {"changed": False }
   
    workdir = module.params[WORKDIR]
    file = module.params[FILE]
    report_validations(workdir,file,module)
    
    task_report = TaskReport()
    reportArgs = {'workdir':workdir,'file':file,}
    try:
        process_task(task_report,module,**reportArgs)
    except Exception as ex:
        module.fail_json(msg=f"Failed to create report, check the logs for more details... {ex}")
  
    log.debug("Task Report completed successfully.")
    result.update(
        {"stdout": f"Successfully Report saved as {file}"}
    )
    module.exit_json(**result)

def report_validations(workdir,file,module):
    validate_filename(FILE,file,module)
    validate_existing_file_type(WORKDIR,workdir,module)

    if workdir is None:
        validate_non_empty_type(ADDRESS,module.params[ADDRESS],module)
        validate_non_empty_type(USER,module.params[USER],module)    
        validate_non_empty_type(PASSWORD,module.params[PASSWORD],module)  

if __name__ == "__main__":
    main()