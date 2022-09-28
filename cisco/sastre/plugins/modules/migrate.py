#! /usr/bin/env python3
DOCUMENTATION = """
module: migrate
short_description:  Migrate configuration items from a vManage release to another. 
                    Currently, only 18.4, 19.2 or 19.3 to 20.1 is supported. Minor revision numbers (e.g. 20.1.1) 
                    are not relevant for the template migration.
description: This migrate module migrates configuration items from vManage release
             to another from local specified directory or target vManage.
notes: 
- Tested against 20.4.1.1
options: 
  scope:
    description:
    - Select whether to evaluate all feature templates, or only feature templates attached to device templates.
    required: true
    type: list
    elements: str
    choices:
    - "all"
    - "attached"
  output:
    description: 
    - Directory to save migrated templates
    required: true
    type: str
  workdir:
    description: 
    - Migrate will read from the specified directory instead of target vManage. Either workdir or address/user/password is mandatory
    required: false
    type: str
  no_rollover:
    description:
    - By default, if the output directory already exists it is renamed using a 
      rolling naming scheme. This option disables this automatic rollover.
    required: false
    type: bool
    default: False
  name:
    description:
    - format used to name the migrated templates.
      Variable {name} is replaced with the original template name. Sections of the 
      original template name can be selected using the {name <regex>} format. Where 
      <regex> is a regular expression that must contain at least one capturing group. 
      Capturing groups identify sections of the original name to keep.
    required: false
    type: str
    default: migrated_{name}
  from:
    description: 
    - vManage version from source templates 
    required: false
    type: str
    default: 18.4
  to:
    description: 
    - target vManage version for template migration
    required: false
    type: str
    default: 20.1
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
- name: Migrate from local backup to local output
  cisco.sastre.migrate:
    scope: attached
    output: test_migrate
    workdir: backup_198.18.1.10_20210726
    name: migrated_1_{name}
    from: '18.4'
    to: '20.1'
    no_rollover: false
- name: Migrate from vManage to local output
  cisco.sastre.migrate:
    scope: attached
    output: test_migrate
    name: migrated_1_{name}
    from: '18.4'
    to: '20.1'
    no_rollover: false
    address: 198.18.1.10
    port: 8443
    user: admin
    password: admin
"""

RETURN = """
stdout:
  description: Status of migrate
  returned: always apart from low level errors
  type: str
  sample: 'Successfully saved migrated templates at test_migrate'
stdout_lines:
  description: The value of stdout split into a list
  returned: always apart from low level errors
  type: list
  sample: ['Successfully saved migrated templates at test_migrates']
"""
from ansible.module_utils.basic import AnsibleModule
from pydantic import ValidationError
from cisco_sdwan.tasks.common import TaskException
from cisco_sdwan.base.rest_api import RestAPIException
from cisco_sdwan.base.models_base import ModelException
from cisco_sdwan.tasks.implementation import TaskMigrate, MigrateArgs
from ansible_collections.cisco.sastre.plugins.module_utils.common import common_arg_spec, module_params, run_task


def main():
    argument_spec = common_arg_spec()
    argument_spec.update(
        scope=dict(type="str", required=True),
        output=dict(type="str", required=True),
        no_rollover=dict(type="bool"),
        name=dict(type="str"),
        from_version=dict(type="str", aliases=['from']),
        to_version=dict(type="str", aliases=['to']),
        workdir=dict(type="str")
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    try:
        task_args = MigrateArgs(
            **module_params('scope', 'output', 'no_rollover', 'name', 'from_version', 'to_version', 'workdir',
                            module_param_dict=module.params)
        )
        task_result = run_task(TaskMigrate, task_args, module.params)

        result = {
            "changed": False
        }
        module.exit_json(**result, **task_result)

    except ValidationError as ex:
        module.fail_json(msg=f"Invalid Migrate parameter: {ex}")
    except (RestAPIException, ConnectionError, FileNotFoundError, ModelException, TaskException) as ex:
        module.fail_json(msg=f"Migrate task error: {ex}")


if __name__ == "__main__":
    main()
