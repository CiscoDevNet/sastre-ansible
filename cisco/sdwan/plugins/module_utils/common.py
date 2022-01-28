import logging
from logging.handlers import QueueHandler
from queue import SimpleQueue, Empty
from ansible.module_utils.basic import env_fallback
from cisco_sdwan.tasks.common import TaskException, Table
from cisco_sdwan.base.rest_api import Rest
from cisco_sdwan.cmd import VMANAGE_PORT, REST_TIMEOUT, BASE_URL


class MemoryLogHandler(QueueHandler):
    def __init__(self):
        super().__init__(SimpleQueue())

    def message_iter(self):
        try:
            while True:
                record = self.queue.get_nowait()
                yield record.getMessage()
        except Empty:
            pass


log_handler = MemoryLogHandler()
logging.basicConfig(level=logging.INFO, handlers=[log_handler], format="[%(levelname)s] %(message)s")


def common_arg_spec():
    return dict(
        address=dict(type="str", fallback=(env_fallback, ['VMANAGE_IP'])),
        user=dict(type="str", fallback=(env_fallback, ['VMANAGE_USER'])),
        password=dict(type="str", no_log=True, fallback=(env_fallback, ['VMANAGE_PASSWORD'])),
        tenant=dict(type="str"),
        pid=dict(type="str", default="0", fallback=(env_fallback, ['CX_PID'])),
        port=dict(type="int", default=VMANAGE_PORT, fallback=(env_fallback, ['VMANAGE_PORT'])),
        timeout=dict(type="int", default=REST_TIMEOUT),
    )


def module_params(*param_names, module_param_dict):
    return {
        name: module_param_dict.get(name) for name in param_names if module_param_dict.get(name) is not None
    }


def sdwan_api_args(module_param_dict):
    missing_required = [
        required_param for required_param in ['address', 'user', 'password']
        if not module_param_dict[required_param]
    ]
    if missing_required:
        raise TaskException(f"Missing parameters: {', '.join(missing_required)}")

    api_args = {
        'base_url': BASE_URL.format(address=module_param_dict['address'], port=module_param_dict['port']),
        'username': module_param_dict['user'],
        'password': module_param_dict['password'],
        'timeout': module_param_dict['timeout']
    }
    if module_param_dict['tenant'] is not None:
        api_args['tenant'] = module_param_dict['tenant']

    return api_args


def run_task(task_cls, task_args, module_param_dict):
    task = task_cls()
    if task.is_api_required(task_args):
        with Rest(**sdwan_api_args(module_param_dict=module_param_dict)) as api:
            task_output = task.runner(task_args, api)
    else:
        task_output = task.runner(task_args)

    result = {}
    if task_output:
        result["stdout"] = "\n\n".join(str(entry) for entry in task_output)
        for entry in task_output:
            if isinstance(entry, Table):
                result.setdefault("tables", []).append(entry.dict())

    if task.is_dryrun:
        result['stdout'] = result.get("stdout", "") + str(task.dryrun_report)

    result["trace"] = list(log_handler.message_iter())
    result["msg"] = f"Task completed {task.outcome('successfully', 'with caveats: {tally}')}"

    # Fail ansible task if critical or error messages are found
    if task.log_count.critical or task.log_count.error:
        raise TaskException(f'{result["msg"]}: {", ".join(result["trace"])}')

    return result
