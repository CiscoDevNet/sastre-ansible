#! /usr/bin/env python3
# -*- coding: utf-8 -*-

DOCUMENTATION = """
module: attach_create
short_description: Attach create templates and config-groups to YAML file
description: This attach create module connects to SD-WAN vManage using HTTP REST to 
             retrieve device templates, config-groups with devices attached or unattached
             and creates a YAML for use in attach_edge or attach_vsmart modules.
             This module contains multiple arguments with connection and filter details.
             When multiple filters are defined, the result is an AND of all filters. 
             The number of devices to include per attach request (to vManage) can be 
             defined with the batch param.
notes: 
- Tested against 20.4.1.1
options: 
  device_types:
    description:
    - Device types
    required: false
    type: str
    choices:
    - "vsmart"
    - "edge"
    - "all"
    default: "all"
  save_attach_file:
    description:
    - Save attach file as yaml file
      This generated yml file can be used in attach_edge or attach_vsmart modules.
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
- name: "Attach Create"
  cisco.sastre.attach_create:
    address: "198.18.1.10"
    port: 8443
    user: "admin"
    password:"admin"
    templates: ".*"
    config_groups: ".*"
    devices: ".*"
    reachable: True
    site: "1"
    system_ip: "12.12.12.12"
    save_attach_file: sample.yml       
- name: "Attach create vManage configuration with some vManage config arguments saved in environment variables"
  cisco.sastre.attach_create: 
    templates: ".*"
    config_groups: ".*"
    devices: ".*"
    reachable: True
    site: "1"
    system_ip: "12.12.12.12"
    save_attach_file: sample.yml
- name: "Attach create vManage configuration with all defaults"
  cisco.sastre.attach_create: 
    address: "198.18.1.10"
    user: admin
    password: admin
"""

RETURN = """
stdout:
  description: Status of attach create
  returned: always apart from low level errors
  type: str
  sample: 'Successfully completed attach create'
stdout_lines:
  description: The value of stdout split into a list
  returned: always apart from low level errors
  type: list
  sample: ['Successfully completed attach create']
"""

from ansible.module_utils.basic import AnsibleModule
from pydantic import ValidationError
from cisco_sdwan.tasks.common import TaskException
from cisco_sdwan.base.rest_api import RestAPIException
from cisco_sdwan.base.models_base import ModelException
from ansible_collections.cisco.sastre.plugins.module_utils.common import common_arg_spec, module_params, run_task


def main():
    argument_spec = common_arg_spec()
    argument_spec.update(
        device_types=dict(type="str"),
        save_attach_file=dict(type="str"),
        templates=dict(type="str"),
        config_groups=dict(type="str"),
        devices=dict(type="str"),
        reachable=dict(type="bool"),
        site=dict(type="str"),
        system_ip=dict(type="str"),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    try:
        from cisco_sdwan.tasks.implementation import TaskAttach, AttachCreateArgs
        task_args = AttachCreateArgs(
            **module_params('device_types', 'save_attach_file', 'templates', 'config_groups', 'devices', 'reachable', 'site', 'system_ip',
                             module_param_dict=module.params)
        )
        task_result = run_task(TaskAttach, task_args, module.params)

        result = {
            "changed": False
        }
        module.exit_json(**result, **task_result)

    except ImportError as ex:
        module.fail_json(msg=f"This module requires Sastre-Pro Python package: {ex}")
    except ValidationError as ex:
        module.fail_json(msg=f"Invalid attach create parameter: {ex}")
    except (RestAPIException, ConnectionError, FileNotFoundError, ModelException, TaskException) as ex:
        module.fail_json(msg=f"Attach create error: {ex}")


if __name__ == "__main__":
    main()
