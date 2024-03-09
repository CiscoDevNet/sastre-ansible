#! /usr/bin/env python3
# -*- coding: utf-8 -*-

DOCUMENTATION = """
module: device_bootstrap
short_description: Performs device bootstrap
description: Performs device bootstrap for a given uuid value
notes: 
- Tested against 20.10
options: 
  uuid:
    description: 
    - device uuid
    required: true
    type: str
  config_type:
    description: 
    - bootstrap configuration type to be used
    required: false
    type: str
    default: cloudinit
  include_default_root_certs:
    description:
    - By default, includes default root certificate. "True" includes the default root cert. "False"
      does not include the default root cert
    required: false
    type: bool
    default: True
  version:
    description:
    - version to be used
    required: false
    type: str
    default: v1
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
- name: Device bootstrap with only uuid
  cisco.sastre.device_bootstrap:
    uuid: "f21dbb35-30b3-47f4-93bb-d2b2fe092d35"
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
- name: Device bootstrap 
  cisco.sastre.device_bootstrap:
    uuid: "f21dbb35-30b3-47f4-93bb-d2b2fe092d35"
    config_type: "cloudinit"
    include_default_root_certs: true
    version: "v1"
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
"""

RETURN = """
stdout:
  description: Status of device bootstrap
  returned: always apart from low level errors
  type: str
"""
from ansible.module_utils.basic import AnsibleModule
from cisco_sdwan.tasks.common import TaskException
from cisco_sdwan.base.rest_api import RestAPIException, Rest
from cisco_sdwan.base.models_base import ModelException
from cisco_sdwan.base.models_vmanage import DeviceBootstrap
from ansible_collections.cisco.sastre.plugins.module_utils.common import common_arg_spec, module_params, sdwan_api_args


def main():
    argument_spec = common_arg_spec()
    argument_spec.update(
        uuid=dict(type="str", required=True),
        config_type=dict(type="str"),
        include_default_root_certs=dict(type="bool"),
        version=dict(type="str"),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    try:
        with Rest(**sdwan_api_args(module_param_dict=module.params)) as api:
            response = DeviceBootstrap.get(api, **module_params('uuid', 'config_type', 'include_default_root_certs',
                                                                'version', module_param_dict=module.params))

            if response is None:
                raise ValueError("Bootstrap request failed, verify that uuid provided is present on vManage and "
                                 "device is at proper state for bootstrap.")

            result = {
                "changed": True,
                "uuid": response.uuid,
                "otp": response.otp,
                "vbond": response.vbond,
                "organization": response.organization,
                "bootstrap_config": response.bootstrap_config
            }
            module.exit_json(**result)

    except (RestAPIException, ConnectionError, FileNotFoundError, ModelException, TaskException, ValueError) as ex:
        module.fail_json(msg=f"Device bootstrap error: {ex}")


if __name__ == "__main__":
    main()
