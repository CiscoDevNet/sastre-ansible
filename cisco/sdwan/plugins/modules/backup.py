#!/usr/bin/python

DOCUMENTATION = """
module: 
author: 
short_description: 
description:
notes:
"""
EXAMPLES = """

"""

RETURN = """

"""
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import env_fallback
import logging
from cisco_sdwan.tasks.common import (
    TaskArgs,
)
from cisco_sdwan.base.rest_api import (
    Rest,
    LoginFailedException,
)
from cisco_sdwan.base.models_base import (
    ModelException,
)
from cisco_sdwan.tasks.implementation._backup import (
    TaskBackup,
)
from cisco_sdwan.tasks.utils import (
    default_workdir, 
    regex_type,
)
from cisco_sdwan.tasks.utils import (
    TagOptions,
)
from  ansible_collections.cisco.sdwan.plugins.module_utils.common import (
    ADDRESS,PORT,USER,PASSWORD,WORKDIR,REGEX,TAGS,NO_ROLLOVER,VERBOSE,TIMEOUT,PID,
    DEFAULT_TAG,DEFAULT_LOG_LEVEL,
    logging_levels,
    setLogLevel,
    BASE_URL,
    updatevManageArgs,
    submit_usage_stats,
)


def main():
    """main entry point for module execution
    """
    tagList = list(TagOptions.tag_options)
    
    argument_spec = dict(
        workdir=dict(type="str"),
        no_rollover=dict(type="bool", default=False),
        regex=dict(type="str"),
        tags=dict(type="list", elements="str", default=[DEFAULT_TAG],choices=tagList),
        verbose=dict(type="str",default=DEFAULT_LOG_LEVEL,choices=logging_levels)
    )
    updatevManageArgs(argument_spec)
    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )
    
    setLogLevel(module.params[VERBOSE])
    log = logging.getLogger(__name__)
    log.debug("Task Backup started.")
    
    result = {"changed": False }
   
    vManage_ip=module.params[ADDRESS]
    workdir = module.params[WORKDIR]
    regex = module.params[REGEX]
    if workdir is None:
        workdir = default_workdir(vManage_ip)
    if regex is not None:
        regex = regex_type(regex)
    
    try:
        base_url = BASE_URL.format(address=vManage_ip, port=module.params[PORT])
        taskBackup = TaskBackup()
        backupArgs = {'workdir':workdir,'no_rollover':module.params[NO_ROLLOVER],'regex':regex,'tags':module.params[TAGS]}
        with Rest(base_url, module.params[USER], module.params[PASSWORD], timeout=module.params[TIMEOUT]) as api:
            taskArgs = TaskArgs(**backupArgs)
            taskBackup.runner(taskArgs, api)
        taskBackup.log_info('Task completed %s', taskBackup.outcome('successfully', 'with caveats: {tally}'))
    except (LoginFailedException, ConnectionError, FileNotFoundError, ModelException) as ex:
        log.critical(ex)
        module.fail_json(msg="Failed to take backup , check the logs for more detaills...")
        
    kwargs={'pid': module.params[PID], 'savings': taskBackup.savings}
    submit_usage_stats(**kwargs)
    log.debug("Task Backup completed successfully.")
    result.update(
        {"stdout": f"Successfully backed up files at {workdir}"}
    )
    module.exit_json(**result)

if __name__ == "__main__":
    main()