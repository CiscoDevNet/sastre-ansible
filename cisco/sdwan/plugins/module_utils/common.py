import logging
import logging.config
import logging.handlers
from pathlib import Path
import json
from ansible.module_utils.basic import env_fallback
from cisco_sdwan.__version__ import __version__ as version
from cisco_sdwan.base.models_base import (
    SASTRE_ROOT_DIR,
)
from cisco_sdwan.tasks.utils import (
    regex_type,TagOptions,default_workdir,
)
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
from cisco_sdwan.cmd import (
    submit_aide_stats,LOGGING_CONFIG,
    VMANAGE_PORT,REST_TIMEOUT,BASE_URL,AIDE_TIMEOUT

)

# Ansible YML argument keys
ADDRESS = "address"
PORT = "port"
USER = "user"
PASSWORD = "password"
WORKDIR = "workdir"
REGEX = "regex"
TAGS = "tags"
NO_ROLLOVER = "no_rollover"
VERBOSE = "verbose"
TIMEOUT = "timeout"
PID= "pid"
DRYRUN="dryrun"
TAG="tag"
ATTACH="attach"
DETACH="detach"
FORCE="force"
# Default tag value
DEFAULT_LOG_LEVEL="DEBUG"
DEFAULT_PID = "0"

logging_levels = [
    'NOTSET',
    'DEBUG',
    'INFO',
    'WARNING',
    'ERROR',
    'CRITICAL',
]

 # Logging setup
logging_config = json.loads(LOGGING_CONFIG)
console_handler = logging_config.get('handlers', {}).get('console')

file_handler = logging_config.get('handlers', {}).get('file')
if file_handler is not None:
    file_handler['filename'] = str(Path(SASTRE_ROOT_DIR, file_handler['filename']))
    Path(file_handler['filename']).parent.mkdir(parents=True, exist_ok=True)

tag_list = list(TagOptions.tag_options)

def get_workdir(workdir,vManage_ip):
    if workdir is None:
        return default_workdir(vManage_ip)
    return workdir
        
def set_log_level(log_level):
    console_handler['level'] = log_level
    file_handler['level'] = log_level
    logging.config.dictConfig(logging_config)

def update_vManage_args(args_spec):
    args = dict(
        address=dict(type="str", required=True,fallback=(env_fallback, ['VMANAGE_IP'])),
        port=dict(type="int", default=VMANAGE_PORT,fallback=(env_fallback, ['VMANAGE_PORT'])),
        user=dict(type="str", required=True,fallback=(env_fallback, ['VMANAGE_USER'])),
        password=dict(type="str", required=True,no_log=True,fallback=(env_fallback, ['VMANAGE_PASSWORD'])),
        timeout=dict(type="int", default=REST_TIMEOUT),
        pid=dict(type="str",default=DEFAULT_PID,fallback=(env_fallback, ['CX_PID'])),
        verbose=dict(type="str",default=DEFAULT_LOG_LEVEL,choices=logging_levels),
    )
    args_spec.update(args)
    
def submit_usage_stats(**kwargs):
    # Submit usage statistics to AIDE (https://wwwin-github.cisco.com/AIDE/aide-python-tools)
    import threading
    aide_thread = threading.Thread(
        target=submit_aide_stats, kwargs={'pid': kwargs['pid'], 'estimated_savings': kwargs['savings']}, daemon=True
    )
    aide_thread.start()
    aide_thread.join(timeout=AIDE_TIMEOUT)
    if aide_thread.is_alive():
        logging.getLogger(__name__).warning('AIDE statistics collection timeout')
    
def validate_regex(regex,module):
    if regex is not None:
        try:  
          regex = regex_type(regex)
        except Exception as ex:
          logging.getLogger(__name__).critical(ex)
          module.fail_json(msg=f'{regex} is not a valid regular expression.') 
          
def process_task(task,module,**taskArgs):
    try:
        base_url = BASE_URL.format(address=module.params[ADDRESS], port=module.params[PORT])
        with Rest(base_url, module.params[USER], module.params[PASSWORD], timeout=module.params[TIMEOUT]) as api:
            taskArgs = TaskArgs(**taskArgs)
            task.runner(taskArgs, api)
        task.log_info('Task completed %s', task.outcome('successfully', 'with caveats: {tally}'))
    except (LoginFailedException, ConnectionError, FileNotFoundError, ModelException) as ex:
        task.log_critical(ex)
    kwargs={'pid': module.params[PID], 'savings': task.savings}
    submit_usage_stats(**kwargs)