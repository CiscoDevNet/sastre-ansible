import logging
import logging.config
import logging.handlers
from pathlib import Path
import json
from ansible.utils.display import Display
from functools import partial
from ansible.module_utils.basic import env_fallback
from cisco_sdwan.__version__ import __version__ as version
from cisco_sdwan.base.models_base import (
    SASTRE_ROOT_DIR,
)
from cisco_sdwan.tasks.utils import (
    regex_type,TagOptions,default_workdir,site_id_type,ipv4_type,int_type,
    filename_type,ext_template_type,non_empty_type,existing_file_type,
    version_type,uuid_type,
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
PID = "pid"
DRYRUN = "dryrun"
TAG = "tag"
ATTACH = "attach"
DETACH = "detach"
FORCE = "force"
TEMPLATES = "templates"
DEVICES = "devices"
SITE = "site"
SYSTEM_IP = "system_ip"
BATCH = "batch"
DEVICE_TYPE = "device_type"
REACHABLE = "reachable"
CMDS="cmds"
DETAIL="detail"
DAYS="days"
HOURS="hours"
CSV="csv"
NAME_REGEX="name_regex"
STATUS="status"
FILE="file"
SCOPE="scope"
OUTPUT="output"
NAME="name"
FROM_VERSION="from_version"
TO="to"
ID="id"
WITH_REFS="with_refs"
# Default tag value
DEFAULT_LOG_LEVEL="DEBUG"
DEFAULT_PID = "0"

attach_detach_device_types = ['edge','vsmart']

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
display = Display()

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

def update_vManage_args(args_spec,mandatory=True):
    args = dict(
        address=dict(type="str", required=mandatory,fallback=(env_fallback, ['VMANAGE_IP'])),
        port=dict(type="int", default=VMANAGE_PORT,fallback=(env_fallback, ['VMANAGE_PORT'])),
        user=dict(type="str", required=mandatory,fallback=(env_fallback, ['VMANAGE_USER'])),
        password=dict(type="str", required=mandatory,no_log=True,fallback=(env_fallback, ['VMANAGE_PASSWORD'])),
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

def get_env_args(module):
    env_args = {
                ADDRESS: module.params[ADDRESS],
                PORT: module.params[PORT],
                USER: module.params[USER],
                PASSWORD: module.params[PASSWORD],
                TIMEOUT: module.params[TIMEOUT],
                PID: module.params[PID]
            }      
    return env_args        

def process_task(task,env_args,**task_args):
    task_args = TaskArgs(**task_args)
    is_api_required = task.is_api_required(task_args)
    task_output = None
    
    try:
        task_output = task_args.task_output
    except AttributeError as exc:       
        task.log_debug(exc)
    
    try:
        if is_api_required:
            base_url = BASE_URL.format(address=env_args[ADDRESS], port=env_args[PORT])
            with Rest(base_url, env_args[USER], env_args[PASSWORD], timeout=env_args[TIMEOUT]) as api:
                task.runner(task_args, api, task_output)
        else:
            task.runner(task_args,task_output=task_output)
        task.log_info('Task completed %s', task.outcome('successfully', 'with caveats: {tally}'))
    except (LoginFailedException, ConnectionError, FileNotFoundError, ModelException) as ex:
        task.log_critical(ex)
        raise Exception(ex) from None
    finally:    
        kwargs={'pid': env_args[PID], 'savings': task.savings}
        submit_usage_stats(**kwargs)

def validate_regex(regex_arg,regex,module=None):
    if regex is not None:
        try:  
          regex_type(regex)
        except Exception as ex:
          ex_msg=f'{regex_arg}: {regex} is not a valid regular expression.'  
          logging.getLogger(__name__).critical(ex)
          raise Exception(ex_msg) if module is None else module.fail_json(msg=ex_msg)
        
def validate_site(site_arg,site,module=None):
    if site is not None:
        try:  
          site_id_type(site)
        except Exception as ex:
          ex_msg=f'{site_arg}: {site} is not a valid site-id.'  
          logging.getLogger(__name__).critical(ex)
          raise Exception(ex_msg) if module is None else module.fail_json(msg=ex_msg)
          
def validate_ipv4(ipv4_arg,ipv4_str,module=None):
    if ipv4_str is not None:
        try:  
          ipv4_type(ipv4_str)
        except Exception as ex:
          ex_msg=f'{ipv4_arg}: {ipv4_str} is not a valid IPv4 address.'
          logging.getLogger(__name__).critical(ex)
          raise Exception(ex_msg) if module is None else module.fail_json(msg=ex_msg)
          
def validate_batch(batch_arg,batch,module=None):
    if batch is not None:
        try:  
          partial_batch = partial(int_type, 1, 9999)
          partial_batch(batch)
        except Exception as ex:
          ex_msg=f'{batch_arg}: Invalid value: {batch}. Must be an integer between 1 and 9999 inclusive.'
          logging.getLogger(__name__).critical(ex)
          raise Exception(ex_msg) if module is None else module.fail_json(msg=ex_msg)
    
def validate_filename(filename_arg,filename,module=None):
    if filename is not None:
        try:
            filename_type(filename)
        except Exception as ex:
            ex_msg = f'{filename_arg}: Invalid name {filename}. Only alphanumeric characters, "-", "_", and "." are allowed.'
            logging.getLogger(__name__).critical(ex)
            raise Exception(ex_msg) if module is None else module.fail_json(msg=ex_msg)

def validate_time(time_arg,time,module=None):
    if time is not None:
        try:  
          time_func = partial(int_type, 0, 9999)
          time_func(time)
        except Exception as ex:
          ex_msg = f'{time_arg}: Invalid value: {time}. Must be an integer between 0 and 9999 inclusive.'  
          logging.getLogger(__name__).critical(ex)
          raise Exception(ex_msg) if module is None else module.fail_json(msg=ex_msg) 

def validate_non_empty_type(src_str_arg,src_str,module=None):
        try:
            non_empty_type(src_str)
        except Exception as ex:
            ex_msg=f'{src_str_arg}:Value cannot be empty.'
            logging.getLogger(__name__).critical(ex)
            raise Exception(ex_msg) if module is None else module.fail_json(msg=ex_msg) 
     
def validate_ext_template_type(name_regex_arg,template_str,module=None):
    if template_str is not None:
        try:
            ext_template_type(template_str)
        except Exception as ex:
            ex_msg = f'{name_regex_arg}:{ex}'
            logging.getLogger(__name__).critical(ex)
            raise Exception(ex_msg) if module is None else module.fail_json(msg=ex_msg)          

def validate_existing_file_type(workdir_arg,workdir,module=None):
    if workdir is not None:
        try:
            existing_file_type(workdir)
        except Exception as ex:
            ex_msg = f'{workdir_arg}:Work directory "{workdir}" not found.'
            logging.getLogger(__name__).critical(ex)
            raise Exception(ex_msg) if module is None else module.fail_json(msg=ex_msg)

def validate_version_type(version_arg,version,module=None):
        try:
            version_type(version)
        except Exception as ex:
            ex_msg = f'{version_arg}:{version}" is not a valid version identifier.'
            logging.getLogger(__name__).critical(ex)
            raise Exception(ex_msg) if module is None else module.fail_json(msg=ex_msg)

def validate_uuid_type(uuid_arg,uuid,module=None):
    if uuid is not None:
        try:
            uuid_type(uuid)
        except Exception as ex:
            ex_msg = f'{uuid_arg}:{uuid} is not a valid item ID.'
            logging.getLogger(__name__).critical(ex)
            raise Exception(ex_msg) if module is None else module.fail_json(msg=ex_msg)
            
def attach_detach_validations(module):
    validate_regex(TEMPLATES,module.params[TEMPLATES],module)
    validate_regex(DEVICES,module.params[DEVICES],module)
    validate_site(SITE,module.params[SITE],module)
    validate_ipv4(SYSTEM_IP,module.params[SYSTEM_IP],module)
    validate_batch(BATCH,module.params[BATCH],module)