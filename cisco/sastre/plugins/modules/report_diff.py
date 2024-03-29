#! /usr/bin/env python3
# -*- coding: utf-8 -*-

DOCUMENTATION = """
module: report_diff
short_description: Generate a report file containing the output from all list and show-template commands.
description: This report module generates report from local backup directory
             or from vManage and saves to local file.
             A log file is created under a logs directory. This logs directory
             is relative to directory where Ansible runs.
notes: 
- Tested against 20.10
options: 
  report_a:
    description: 
    - report a filename (from)
    required: true
    type: str
  report_b:
    description: 
    - report b filename (to)
    required: true
    type: str
  spec_file:
    description: 
    - load custom report specification from YAML file
    required: false
    type: str
  spec_json:
    description: 
    - load custom report specification from JSON-formatted string
    required: false
    type: str
  save_html:
    description: 
    - save report diff as html file
    required: false
    type: str
  save_txt:
    description: 
    - save report diff as text file
    required: false
    type: str
  address:
    description:
    - vManage IP address or can also be defined via VMANAGE_IP environment variable
    required: True
    type: str
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
  tenant:
    description: 
    - tenant name, when using provider accounts in multi-tenant deployments.
    required: false
    type: str
  pid:
    description: 
    - CX project id or can also be defined via CX_PID environment variable. 
      This is collected for AIDE reporting purposes only.
    type: str
    required: true
  port:
    description: 
    - vManage port number or can also be defined via VMANAGE_PORT environment variable
    required: false
    type: int
    default: 8443
  timeout:
    description: 
    - vManage REST API timeout in seconds
    required: false
    type: int
    default: 300
"""

EXAMPLES = """
- name: Report from vManage
  cisco.sastre.report_diff:
    report_a: todays_report.txt
    report_b: todays_report.txt
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
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
from pydantic import ValidationError
from ansible.module_utils.basic import AnsibleModule
from cisco_sdwan.tasks.common import TaskException
from cisco_sdwan.base.rest_api import RestAPIException
from cisco_sdwan.base.models_base import ModelException
from cisco_sdwan.tasks.implementation import TaskReport, ReportDiffArgs
from ansible_collections.cisco.sastre.plugins.module_utils.common import common_arg_spec, module_params, run_task


def main():
    argument_spec = common_arg_spec()
    argument_spec.update(
        report_a=dict(type="str", required=True),
        report_b=dict(type="str", required=True),
        spec_file=dict(type="str"),
        spec_json=dict(type="json"),
        save_html=dict(type="str"),
        save_txt=dict(type="str")
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=[('spec_file', 'spec_json')],
        supports_check_mode=True
    )

    try:
        task_args = ReportDiffArgs(
            **module_params('report_a', 'report_b', 'spec_file', 'spec_json', 'save_html', 'save_txt',
                            module_param_dict=module.params)
        )
        task_result = run_task(TaskReport, task_args, module.params)

        result = {
            "changed": False
        }
        module.exit_json(**result, **task_result)

    except ValidationError as ex:
        module.fail_json(msg=f"Invalid report diff parameter: {ex}")
    except (RestAPIException, ConnectionError, FileNotFoundError, ModelException, TaskException) as ex:
        module.fail_json(msg=f"Report diff error: {ex}")


if __name__ == "__main__":
    main()
