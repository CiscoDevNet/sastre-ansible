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
from cisco_sdwan.tasks.implementation._delete import (
    TaskDelete,
)
from cisco_sdwan.tasks.utils import (
    TagOptions
)
from ansible_collections.cisco.sdwan.plugins.module_utils.common import (
    ADDRESS,REGEX,VERBOSE,
    DRYRUN,TAG,DETACH,
    setLogLevel,updatevManageArgs,validateRegEx,processTask,
)


def main():
    """main entry point for module execution
    """
    tagList = list(TagOptions.tag_options)
    
    argument_spec = dict(
        regex=dict(type="str"),
        dryrun=dict(type="bool", default=False),
        detach=dict(type="bool", default=False),
        tag=dict(type="str", required=True, choices=tagList)
    )
    updatevManageArgs(argument_spec)
    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )
    setLogLevel(module.params[VERBOSE])
    log = logging.getLogger(__name__)
    log.debug("Task Delete started.")
        
    result = {"changed": False }
   
    vManage_ip=module.params[ADDRESS]
    regex = module.params[REGEX]
    validateRegEx(regex,module)
    dryrun = module.params[DRYRUN]
    tag = module.params[TAG]
    detach = module.params[DETACH]
    
    taskDelete = TaskDelete()
    deleteArgs = {'regex':regex,'dryrun':dryrun,'detach':detach,'tag':tag}
    try:
        processTask(taskDelete,module,**deleteArgs)
    except Exception as ex:
        module.fail_json(msg=f"Failed to delete , check the logs for more detaills... {ex}")
        
    log.debug("Task Delete completed successfully.")
    result["changed"] = False if dryrun else True
    result.update(
        {"stdout": "{} Delete completed successfully.vManage address {}".format("DRY-RUN mode: " if dryrun else "", vManage_ip) }
    )
    module.exit_json(**result)

if __name__ == "__main__":
    main()