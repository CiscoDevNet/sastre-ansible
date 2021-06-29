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
    regex_type
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

# vManage REST API defaults
VMANAGE_PORT = '8443'
REST_TIMEOUT = 300
BASE_URL = 'https://{address}:{port}'

# Maximum amount of time allowed for AIDE statistics collection
AIDE_TIMEOUT = 3

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
DEFAULT_TAG = "all"
DEFAULT_LOG_LEVEL="DEBUG"
DEFAULT_PID = "0"


# Default logging configuration - JSON formatted
# Reason for setting level at chardet.charsetprober is to prevent unwanted debug messages from requests module
LOGGING_CONFIG = '''
{
    "version": 1,
    "formatters": {
        "simple": {
            "format": "%(levelname)s: %(message)s"
        },
        "detailed": {
            "format": "%(asctime)s: %(name)s: %(levelname)s: %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/sastre.log",
            "backupCount": 3,
            "maxBytes": 204800,
            "level": "DEBUG",
            "formatter": "detailed"
        }
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "DEBUG"
    },
    "loggers": {
        "chardet.charsetprober": {
            "level": "INFO"
        },
        "aide.statistics": {
            "level": "WARN"
        }
    }
}
'''

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

def setLogLevel(logLevel):
    console_handler['level'] = logLevel
    file_handler['level'] = logLevel
    logging.config.dictConfig(logging_config)

def updatevManageArgs(argsSpec):
    args = dict(
        address=dict(type="str", required=True,fallback=(env_fallback, ['VMANAGE_IP'])),
        port=dict(type="int", default=VMANAGE_PORT,fallback=(env_fallback, ['VMANAGE_PORT'])),
        user=dict(type="str", required=True,fallback=(env_fallback, ['VMANAGE_USER'])),
        password=dict(type="str", required=True,no_log=True,fallback=(env_fallback, ['VMANAGE_PASSWORD'])),
        timeout=dict(type="int", default=REST_TIMEOUT),
        pid=dict(type="str",default=DEFAULT_PID,fallback=(env_fallback, ['CX_PID'])),
        verbose=dict(type="str",default=DEFAULT_LOG_LEVEL,choices=logging_levels),
    )
    argsSpec.update(args)
    
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
    
def submit_aide_stats(pid, estimated_savings):
    try:
        from aide import submit_statistics
        submit_statistics(
            tool_id='46810',
            pid=pid,
            metadata={
                "potential_savings": estimated_savings,
                "report_savings": True,
                "sastre_version": version
            }
        )
    except ModuleNotFoundError:
        logging.getLogger(__name__).debug('AIDE package not installed')
    except Exception as ex:
        logging.getLogger(__name__).debug(f'Exception found while submitting AIDE statistics: {ex}')
        
def validateRegEx(regex,module):
    if regex is not None:
        try:  
          regex = regex_type(regex)
        except Exception as ex:
          logging.getLogger(__name__).critical(ex)
          module.fail_json(msg=f'{regex} is not a valid regular expression.') 
          
def processTask(task,module,**taskArgs):
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