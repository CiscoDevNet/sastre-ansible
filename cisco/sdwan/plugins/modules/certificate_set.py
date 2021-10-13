#!/usr/bin/python

DOCUMENTATION = """
module: certificate
short_description: Set Certificate status
description: The certificate set task can be used to set of desired value to target vManage. 
             Matching or not matching criteria can contain regular expression value.
notes: 
- Tested against 20.4.1.1
options: 
  regex:
    description:
    - Regular expression selecting devices to modify certificate status. Matches on
      the hostname or chassis/uuid. Use "^-$" to match devices without a hostname.'
    required: false
    type: str
  not_regex:
    description:
    - Regular expression selecting devices NOT to modify certificate status. Matches on
      the hostname or chassis/uuid.'
    required: false
    type: str
  dryrun:
    description:
    - dry-run mode. List modifications that would be performed without pushing changes to vManage.
    required: false
    type: bool
    default: False
  status:
    description:
    - WAN edge certificate status
    required: true
    type: str
    choices:
    - "invalid"
    - "staging"
    - "valid"
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
  tenant:
    description: 
    - tenant name, when using provider accounts in multi-tenant deployments.
    required: false
    type: str
  timeout:
    description: 
    - vManage REST API timeout in seconds
    required: false
    type: int
    default: 300
"""

EXAMPLES = """
- name: Certificate Set
  cisco.sdwan.certificate_set:
    status: valid
    regex: ".*"
    dryrun: True
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
    timeout: 300
- name: Certificate Set
  cisco.sdwan.certificate_set:
    status: valid
    not_regex: ".*"
    dryrun: True
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
    timeout: 300
"""

RETURN = """
stdout:
  description: Status of Certificate
  returned: always apart from low level errors
  type: str
  sample: 'Task Certificate: set completed successfully.vManage address 198.18.1.10'
stdout_lines:
  description: The value of stdout split into a list
  returned: always apart from low level errors
  type: list
  sample: ['Task Certificate: set completed successfully.vManage address 198.18.1.10']
"""
from ansible.module_utils.basic import AnsibleModule
from cisco_sdwan.tasks.implementation._certificate import (
    TaskCertificate,CertificateSetArgs
)
import logging
from pydantic import ValidationError
from cisco_sdwan.tasks.common import TaskException
from cisco_sdwan.base.rest_api import RestAPIException
from cisco_sdwan.base.models_base import ModelException
from ansible_collections.cisco.sdwan.plugins.module_utils.common import (
    common_arg_spec,module_params, run_task
)

def main():
    """main entry point for module execution
    """
    argument_spec = common_arg_spec()
    argument_spec.update(
        regex=dict(type="str"),
        not_regex=dict(type="str"),
        dryrun=dict(type="bool"),
        status=dict(type="str", required=True)
    )
    
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=[('regex', 'not_regex')],
        supports_check_mode=True
    )
    
    try:
        task_args = CertificateSetArgs(
            **module_params('regex','not_regex','dryrun', 'status',module_param_dict=module.params)
        )
        task_result = run_task(TaskCertificate, task_args, module.params)

        result = {
            "changed": False
        }
        module.exit_json(**result, **task_result)
    except ValidationError as ex:
        module.fail_json(msg=f"Invalid Certificate set parameter: {ex}")
    except (RestAPIException, ConnectionError, FileNotFoundError, ModelException, TaskException) as ex:
        module.fail_json(msg=f"Certificate set task error: {ex}")

if __name__ == "__main__":
    main()