#!/usr/bin/python

DOCUMENTATION = """
module: detach_vsmart
short_description: Detach templates from vSmarts.
description: This detach module connects to SD-WAN vManage using HTTP REST to 
             updated configuration data stored in local default backup or configured argument
             local backup folder. This module contains multiple arguments with 
             connection and filter details to detach vSmarts from templates.
             When multiple filters are defined, the result is an AND of all filters. 
             Dry-run can be used to validate the expected outcome.The number of devices to include 
             per detach request (to vManage) can be defined with the batch option.
notes: 
- Tested against 20.4.1.1
options: 
  templates:
    description:
    - Regular expression selecting templates to detach. Match on template name.
    required: false
    type: str
  devices:
    description:
    - Regular expression selecting devices to detach. Match on device name.
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
    - dry-run mode. Attach operations are listed but nothing is pushed to vManage.
    required: false
    type: bool
    default: False
  batch:
    description:
    - Maximum number of devices to include per vManage detach request.
    required: false
    type: int
    default: 200
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
- name: "Detach vManage configuration"
  cisco.sdwan.detach_vsmart:
    address: "198.18.1.10"
    port: 8443
    user: "admin"
    password:"admin"
    timeout: 300
    templates: ".*"
    devices: ".*"
    reachable: True
    site: "1"
    system_ip: "12.12.12.12"
    dryrun: False
    batch: 99       
- name: "Detach vManage configuration with some vManage config arguments saved in environment variables"
  cisco.sdwan.detach_vsmart: 
    timeout: 300
    templates: ".*"
    devices: ".*"
    reachable: True
    site: "1"
    system_ip: "12.12.12.12"
    dryrun: True
    batch: 99    
- name: "Detach vManage configuration with all defaults"
  cisco.sdwan.detach_vsmart: 
    address: "198.18.1.10"
    user: admin
    password: admin
"""

RETURN = """
stdout:
  description: Status of detach vsmarts
  returned: always apart from low level errors
  type: str
  sample: 'Successfully detached templates from vsmarts'
stdout_lines:
  description: The value of stdout split into a list
  returned: always apart from low level errors
  type: list
  sample: ['Successfully detached templates from vsmarts']
"""

from ansible.module_utils.basic import AnsibleModule
from pydantic import ValidationError
from cisco_sdwan.tasks.implementation._attach_detach import TaskDetach, DetachVsmartArgs
from cisco_sdwan.tasks.common import TaskException
from cisco_sdwan.base.rest_api import RestAPIException
from cisco_sdwan.base.models_base import ModelException
from  ansible_collections.cisco.sdwan.plugins.module_utils.common import common_arg_spec, module_params, run_task

def main():
    """main entry point for module execution
    """
    argument_spec = common_arg_spec()
    argument_spec.update(
        templates=dict(type="str"),
        devices=dict(type="str"),
        reachable=dict(type="bool"),
        site=dict(type="str"),
        system_ip=dict(type="str"),
        dryrun=dict(type="bool"),
        batch=dict(type=int),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    try:
        task_args = DetachVsmartArgs(
            **module_params('templates', 'devices', 'reachable', 'site', 'system_ip', 'dryrun', 'batch', 
                            module_param_dict=module.params)
        )
        task_result = run_task(TaskDetach, task_args, module.params)

        result = {
            "changed": False
        }
        module.exit_json(**result, **task_result)

    except ValidationError as ex:
        module.fail_json(msg=f"Invalid detach vsmart parameter: {ex}")
    except (RestAPIException, ConnectionError, FileNotFoundError, ModelException, TaskException) as ex:
        module.fail_json(msg=f"Detach vsmart error: {ex}")

if __name__ == "__main__":
    main()