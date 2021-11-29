from ansible.errors import AnsibleOptionsError
from cisco_sdwan.base.rest_api import Rest
from cisco_sdwan.cmd import REST_TIMEOUT, VMANAGE_PORT
from .common import sdwan_api_args


def get_plugin_inventory_args(variables):
    return dict(
        address=variables.get('ansible_host'),
        user=variables.get('ansible_user'),
        password=variables.get('ansible_password'),
        tenant=variables.get('tenant'),
        port=variables.get('vmanage_port') or VMANAGE_PORT,
        timeout=variables.get('timeout') or REST_TIMEOUT
    )


def run_task(task_cls, task_args, module_param_dict):
    task = task_cls()
    if task.is_api_required(task_args):
        with Rest(**sdwan_api_args(module_param_dict=module_param_dict)) as api:
            task_output = task.runner(task_args, api)
    else:
        task_output = task.runner(task_args)

    result = []
    if task_output:
        result = [table.dict() for table in task_output]

    return result


def validate_show_mandatory_args(**kwargs):
    mandatory_args = [
        ('cmd', list, 'a list')
    ]
    for arg_name, arg_type, arg_hint in mandatory_args:
        arg_val = kwargs.get(arg_name)
        if arg_val is None:
            raise AnsibleOptionsError(f"Parameter {arg_name} is mandatory")
        elif not isinstance(arg_val, arg_type):
            raise AnsibleOptionsError(f"Parameter {arg_name} must be {arg_hint}")


def validate_show_type_args(**kwargs):
    type_args = [
        ('regex', str, 'a string'),
        ('not_regex', str, 'a string'),
        ('reachable', bool, 'a boolean'),
        ('site', str, 'a string'),
        ('system_ip', str, 'a string'),
        ('detail', bool, 'a boolean'),
    ]
    for arg_name, arg_type, arg_hint in type_args:
        arg_val = kwargs.get(arg_name)
        if arg_val is not None and not isinstance(arg_val, arg_type):
            raise AnsibleOptionsError(f"Parameter {arg_name} must be {arg_hint}")


def set_show_default_args(**kwargs):
    default_args = [
        ('save_csv', 'None'),
        ('save_json', 'None')
    ]
    for arg_name, arg_default in default_args:
        kwargs.pop(arg_name, arg_default)
    return kwargs


def is_mutually_exclusive(mutual_exclusive_fields, **kwargs):
    if mutual_exclusive_fields is not None and len(mutual_exclusive_fields) > 1:
        is_mutually_exlusive: bool = False
        for arg in mutual_exclusive_fields:
            if kwargs.get(arg) is None:
                continue
            elif is_mutually_exlusive:
                return is_mutually_exlusive
            is_mutually_exlusive = True
