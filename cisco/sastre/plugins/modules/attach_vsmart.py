#! /usr/bin/env python3
# -*- coding: utf-8 -*-

DOCUMENTATION = """
module: attach_vsmart
short_description: Attach templates to Vsmarts
description: This attach module connects to SD-WAN vManage using HTTP REST to 
             updated configuration data stored in local default backup or configured argument
             local backup folder or attach yml file. This module contains multiple arguments with 
             connection and filter details to attach Vsmarts to templates.
             When multiple filters are defined, the result is an AND of all filters. 
             Dry-run can be used to validate the expected outcome.The number of devices to include 
             per attach request (to vManage) can be defined with the batch param.
notes: 
- Tested against 20.10
options: 
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
  attach_file:
    description:
    - load vsmart device templates attach and vsmart policy activate from attach YAML file
    required: false
    type: str
  templates:
    description:
    - Regular expression selecting templates to attach. Match on template name.
    required: false
    type: str
  config_groups:
    description:
    - Regular expression selecting config-groups to deploy. Match on config-group name.
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
  activate:
    description:
    - Activate centralized policy after vSmart template attach/deploy.
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
- name: "Attach vManage configuration"
  cisco.sastre.attach_vsmart:
    address: "198.18.1.10"
    port: 8443
    user: "admin"
    password:"admin"
    workdir: "backup_test_1"
    templates: ".*"
    config_groups: ".*"
    devices: ".*"
    reachable: True
    activate: True
    site: "1"
    system_ip: "12.12.12.12"
    dryrun: False
    batch: 99       
- name: "Attach vManage configuration with some vManage config arguments saved in environment variables"
  cisco.sastre.attach_vsmart: 
    workdir: "backup_test_2"
    templates: ".*"
    config_groups: ".*"
    devices: ".*"
    reachable: True
    activate: True
    site: "1"
    system_ip: "12.12.12.12"
    dryrun: True
    batch: 99    
- name: "Attach vsmart device templates and vsmart policy activate from attach yml file"
  cisco.sastre.attach_vsmart: 
    attach_file: "/path/to/attach.yml"
    batch: 99 
- name: "Attach vManage configuration with all defaults"
  cisco.sastre.attach_vsmart: 
    address: "198.18.1.10"
    user: admin
    password: admin
"""

RETURN = """
stdout:
  description: Status of attach vsmart
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
from pydantic import ValidationError
from cisco_sdwan.tasks.common import TaskException
from cisco_sdwan.tasks.utils import default_workdir
from cisco_sdwan.base.rest_api import RestAPIException
from cisco_sdwan.base.models_base import ModelException
from cisco_sdwan.tasks.implementation import TaskAttach, AttachVsmartArgs
from ansible_collections.cisco.sastre.plugins.module_utils.common import common_arg_spec, module_params, run_task


def main():
    argument_spec = common_arg_spec()
    argument_spec.update(
        workdir=dict(type="str"),
        attach_file=dict(type="str"),
        templates=dict(type="str"),
        config_groups=dict(type="str"),
        devices=dict(type="str"),
        reachable=dict(type="bool"),
        activate=dict(type="bool"),
        site=dict(type="str"),
        system_ip=dict(type="str"),
        dryrun=dict(type="bool"),
        batch=dict(type=int),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=[('workdir', 'attach_file')],
        supports_check_mode=True
    )

    try:
        if not module.params['attach_file']:
            module.params['workdir'] = module.params['workdir'] or default_workdir(module.params['address'])
        task_args = AttachVsmartArgs(
            **module_params('workdir', 'attach_file', 'templates', 'config_groups', 'devices', 'reachable', 'activate', 'site', 'system_ip',
                            'dryrun', 'batch', module_param_dict=module.params)
        )
        task_result = run_task(TaskAttach, task_args, module.params)

        result = {
            "changed": False
        }
        module.exit_json(**result, **task_result)

    except ValidationError as ex:
        module.fail_json(msg=f"Invalid attach vsmart parameter: {ex}")
    except (RestAPIException, ConnectionError, FileNotFoundError, ModelException, TaskException) as ex:
        module.fail_json(msg=f"Attach vsmart error: {ex}")


if __name__ == "__main__":
    main()
