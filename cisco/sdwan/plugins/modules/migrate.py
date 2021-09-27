#!/usr/bin/python
DOCUMENTATION = """
module: migrate
author: Satish Kumar Kamavaram (sakamava@cisco.com)
short_description:  Migrate configuration items from a vManage release to another. 
                    Currently, only 18.4, 19.2 or 19.3 to 20.1 is supported. Minor revision numbers (e.g. 20.1.1) 
                    are not relevant for the template migration.
description: This migrate module migrates configuration items from vManage release
             to another from local specified directory or target vManage.
             A log file is created under a "logs" directory. This "logs" directory
             is relative to directory where Ansible runs.
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
    - migrate will read from the specified directory instead of target vManage. Either workdir or address/user/password is mandatory
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
- name: Migrate from local backup to local output
  cisco.sdwan.migrate:
    scope: attached
    output: test_migrate
    workdir: backup_198.18.1.10_20210726
    name: migrated_1_{name}
    from: '18.4'
    to: '20.1'
    no_rollover: false
    port: 8443
    verbose: INFO
    pid: "2"
- name: Migrate from vManage to local output
  cisco.sdwan.migrate:
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
    verbose: INFO
    pid: "2"
    timeout: 300
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
from ansible.module_utils.basic import env_fallback
import logging
from datetime import date
from cisco_sdwan.tasks.implementation._migrate import (
    TaskMigrate
)
from  ansible_collections.cisco.sdwan.plugins.module_utils.common import (
    ADDRESS,WORKDIR,VERBOSE,SCOPE,OUTPUT,NO_ROLLOVER,NAME,FROM_VERSION,TO,
    USER,PASSWORD,
    set_log_level,update_vManage_args,validate_filename,process_task,
    validate_existing_file_type,validate_non_empty_type, 
    validate_ext_template_type,validate_version_type,get_env_args
)


def main():
    """main entry point for module execution
    """
    argument_spec = dict(
        scope=dict(type="str", required=True, choices=['all','attached']),
        output=dict(type="str",required=True),
        no_rollover=dict(type="bool",default=False),
        name=dict(type="str",default='migrated_{name}'),
        from_version=dict(type="str",default='18.4',aliases=['from']),
        to=dict(type="str",default='20.1'),
        workdir=dict(type="str")
    )

    update_vManage_args(argument_spec,False)

    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )
    
    set_log_level(module.params[VERBOSE])
    log = logging.getLogger(__name__)
    log.debug("Task Migrate started.")
    
    result = {"changed": False }
   
    output = module.params[OUTPUT]
    migrate_validations(module)
    
    task_migrate = TaskMigrate()
    migrateArgs = get_migrate_args(module)

    try:
        process_task(task_migrate,get_env_args(module),**migrateArgs)
    except Exception as ex:
        module.fail_json(msg=f"Failed to migrate, check the logs for more details... {ex}")
  
    log.debug("Task Migrate completed successfully.")
    result.update(
        {"stdout": f"Successfully saved migrated templates at {output}"}
    )
    module.exit_json(**result)

def get_migrate_args(module):
    args= {
            'scope':module.params[SCOPE],
            'output':module.params[OUTPUT],
            'no_rollover':module.params[NO_ROLLOVER],
            'name':module.params[NAME],
            'from_version':module.params[FROM_VERSION],
            'to_version':module.params[TO],
            'workdir':module.params[WORKDIR]
        }
    return args

def migrate_validations(module):
    validate_filename(OUTPUT,module.params[OUTPUT],module)
    validate_ext_template_type(NAME,module.params[NAME],module)
    validate_version_type('from',module.params[FROM_VERSION],module)
    validate_version_type(TO,module.params[TO],module)
    workdir = module.params[WORKDIR]
    validate_existing_file_type(WORKDIR,workdir,module)

    if workdir is None:
        validate_non_empty_type(ADDRESS,module.params[ADDRESS],module)
        validate_non_empty_type(USER,module.params[USER],module)    
        validate_non_empty_type(PASSWORD,module.params[PASSWORD],module)        

if __name__ == "__main__":
    main()