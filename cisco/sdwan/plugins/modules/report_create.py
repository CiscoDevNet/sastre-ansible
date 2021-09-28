#!/usr/bin/python
DOCUMENTATION = """
module: report_create
author: Satish Kumar Kamavaram (sakamava@cisco.com)
short_description: Generate a report file containing the output from all list and show-template commands.
description: This report module generates report from local backup directory
             or from vManage and saves to local file.
             A log file is created under a logs directory. This logs directory
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
    - report filename (default filename - report_{current_date}.txt)
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
    verbose: "DEBUG"
    pid: "2"
    timeout: 300
- name: Report from local folder
  cisco.sdwan.report:
    workdir: backup_198.18.1.10_20210726
    file: todays_report.txt
    verbose: "DEBUG"
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
import logging
from datetime import date
from pydantic import ValidationError
from ansible.module_utils.basic import AnsibleModule
from cisco_sdwan.tasks.implementation import TaskReport, ReportCreateArgs
from cisco_sdwan.tasks.common import TaskException
from cisco_sdwan.base.rest_api import Rest, RestAPIException
from cisco_sdwan.base.models_base import ModelException
from cisco.sdwan.plugins.module_utils.common import api_args, VERBOSE, set_log_level, common_arg_spec


def main():
    argument_spec = dict(
        workdir=dict(type="str"),
        file=dict(type="str", default=f'report_{date.today():%Y%m%d}.txt'),
        spec_file=dict(type="str"),
        spec_json=dict(type="str")
    )
    module = AnsibleModule(
        argument_spec={**common_arg_spec(), **argument_spec},
        mutually_exclusive=[('spec_file', 'spec_json')],
        supports_check_mode=True
    )

    set_log_level(module.params[VERBOSE])
    log = logging.getLogger(__name__)
    log.debug("Task Report started.")

    try:
        task_args = ReportCreateArgs(
            workdir=module.params['workdir'],
            file=module.params['file'],
            spec_file=module.params['spec_file'],
            spec_json=module.params['spec_json']
        )
        task = TaskReport()
        if task.is_api_required(task_args):
            with Rest(**api_args(module_params=module.params)) as api:
                task_output = task.runner(task_args, api)
        else:
            task_output = task.runner(task_args)

        result = {
            "changed": False,
            "stdout": "\n\n".join(str(entry) for entry in task_output) if task_output else "",
            "outcome": f"Task completed {task.outcome('successfully', 'with caveats: {tally}')}"
        }
        module.exit_json(**result)

    except ValidationError as ex:
        module.fail_json(msg=f"Invalid report create parameter: {ex}")
    except (RestAPIException, ConnectionError, FileNotFoundError, ModelException, TaskException) as ex:
        module.fail_json(msg=f"Report create error: {ex}")


if __name__ == "__main__":
    main()
