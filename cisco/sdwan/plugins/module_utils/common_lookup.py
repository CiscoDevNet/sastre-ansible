from ansible.errors import AnsibleOptionsError
from cisco_sdwan.cmd import REST_TIMEOUT
from .common import execute_task

def get_plugin_inventory_args(variables):
    return dict(
        address = variables.get('ansible_host'),
        port = (8443 if variables.get('vmanage_port') is None else variables.get('vmanage_port')),
        user = variables.get('ansible_user'),
        password = variables.get('ansible_password'),
        tenant = variables.get('tenant'),
        timeout = (REST_TIMEOUT if variables.get('timeout') is None else variables.get('timeout'))
    )

def run_task(task_cls, task_args, module_param_dict):
    task = task_cls()
    task_output = execute_task(task, task_args, module_param_dict)

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
        ('save_csv','None'),
        ('save_json','None')
    ]
    for arg_name, arg_default in default_args:
        kwargs.pop(arg_name, arg_default)
    return kwargs           