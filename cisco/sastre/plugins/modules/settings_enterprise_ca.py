#! /usr/bin/env python3
# -*- coding: utf-8 -*-

DOCUMENTATION = """
module: settings_enterprise_ca
short_description: Setting enterprise root certificate
description: Setting enterprise root certificate
notes: 
- Tested against 20.10
options: 
  root_cert:
    description: 
    - Enterprise root certificate
    required: true
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
- name: Setting enterprise root certificate
  cisco.sastre.settings_enterprise_ca:
    root_cert: "{{ lookup('file', 'myCA.pem') }}"
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
"""

RETURN = """
stdout:
  description: Status of enterprise root certificate setting
  returned: always apart from low level errors
  type: str
"""
from ansible.module_utils.basic import AnsibleModule
from cisco_sdwan.tasks.common import TaskException
from cisco_sdwan.base.rest_api import RestAPIException, Rest
from cisco_sdwan.base.models_base import ModelException
from cisco_sdwan.base.models_vmanage import SettingsCertificate
from ansible_collections.cisco.sastre.plugins.module_utils.common import common_arg_spec, module_params, sdwan_api_args


def main():
    argument_spec = common_arg_spec()
    argument_spec.update(
        root_cert=dict(type="str", required=True),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    try:
        with Rest(**sdwan_api_args(module_param_dict=module.params)) as api:
            SettingsCertificate.set_signing_enterprise(api, module.params['root_cert'])

            result = {
                "changed": True,
            }
            module.exit_json(**result)

    except (RestAPIException, ConnectionError, FileNotFoundError, ModelException, TaskException) as ex:
        module.fail_json(msg=f"Device bootstrap error: {ex}")


if __name__ == "__main__":
    main()
