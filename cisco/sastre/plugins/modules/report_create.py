#! /usr/bin/env python3
# -*- coding: utf-8 -*-

DOCUMENTATION = """
module: report_create
short_description: Generate a report file containing the output from all list and show-template commands.
description: This report module generates report from local backup directory
             or from vManage and saves to local file.
             A log file is created under a logs directory. This logs directory
             is relative to directory where Ansible runs.
notes: 
- Tested against 20.4.1.1
options: 
  file:
    description: 
    - report filename (default filename - report_{current_date}.txt)
    required: false
    type: str
  workdir:
    description: 
    - report from the specified directory instead of target vManage
    required: false
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
  diff:
    description: 
    - generate diff between the specified previous report and the current report
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
  cisco.sastre.report_create:
    file: todays_report.txt
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
- name: Report from local folder
  cisco.sastre.report_create:
    workdir: backup_198.18.1.10_20210726
    file: todays_report.txt
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
from ansible_collections.cisco.sastre.plugins.module_utils.common import common_arg_spec, module_params, run_task


def main():
    argument_spec = common_arg_spec()
    argument_spec.update(
        workdir=dict(type="str"),
        file=dict(type="str"),
        spec_file=dict(type="str"),
        spec_json=dict(type="json"),
        diff=dict(type="str")
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=[('spec_file', 'spec_json')],
        supports_check_mode=True
    )

    try:
        from cisco_sdwan.tasks.implementation import TaskReport, ReportCreateArgs
        task_args = ReportCreateArgs(
            **module_params('workdir', 'file', 'spec_file', 'spec_json', 'diff', module_param_dict=module.params)
        )
        task_result = run_task(TaskReport, task_args, module.params)

        # changed flag is True when 'diff' option is provided and diff comparison indicates differences between reports
        result = {
            "changed": module.params['diff'] is not None and len(task_result.get('stdout', '').splitlines()) > 4
        }
        module.exit_json(**result, **task_result)

    except ImportError:
        module.fail_json(msg="This module requires Sastre-Pro Python package")
    except ValidationError as ex:
        module.fail_json(msg=f"Invalid report create parameter: {ex}")
    except (RestAPIException, ConnectionError, FileNotFoundError, ModelException, TaskException) as ex:
        module.fail_json(msg=f"Report create error: {ex}")


if __name__ == "__main__":
    main()
