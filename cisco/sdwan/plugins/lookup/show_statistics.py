#!/usr/bin/python
from ansible.errors import AnsibleLookupError, AnsibleOptionsError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
from pydantic import ValidationError
from cisco_sdwan.tasks.implementation._show import TaskShow, ShowStatisticsArgs
from cisco_sdwan.tasks.common import TaskException
from cisco_sdwan.base.rest_api import RestAPIException
from cisco_sdwan.base.models_base import ModelException
from ansible_collections.cisco.sdwan.plugins.module_utils.common import is_mutually_exclusive
from ansible_collections.cisco.sdwan.plugins.module_utils.common_lookup import (run_task, get_plugin_inventory_args, validate_show_type_args,
                                                                                validate_show_mandatory_args, set_show_default_args)


DOCUMENTATION = """
lookup: show_statistics
version_added: "1.0"
short_description: Statistics commands. Faster, but data is 30 min or more old.Allows historical data queries.
description:
    - This show_devices lookup returns list of SD-WAN devices from vManage, contains multiple arguments with 
      connection and filter details to retrieve statistics device data.
      Following parameters must be configured in ansible inventor file
      - ansible_host
      - ansible_user
      - ansible_password
      - vmanage_port
      - tenant
      - timeout
options:
    regex:
        description: Regular expression matching device name, type or model to display
        required: false
        type: str
    not_regex:
        description: Regular expression matching device name, type or model NOT to display.
        required: false
        type: str
    reachable:
        description: Display only reachable devices
        required: false
        type: bool
        default: False
    site:
        description: Select devices with site ID.
        required: false
        type: str
    system_ip:
        description: Select device with system IP.
        required: false
        type: str
    cmd:
        description: >
                Group of, or specific command to execute. 
                Group options are all, app-route, interface, system. 
                Command options are app-route stats, interface info, system status.
        required: True
        type: list
    detail:
        description: Detailed output.
        required: false
        type: bool
        default: False
    days:
        description: Query statistics from days ago (default is now).
        required: false
        type: int
        default: 0
    hours:
        description: Query statistics from hours ago (default is now).
        required: false
        type: int
        default: 0
"""

EXAMPLES = """
    - name: Fetch all devices state data
      debug:
        msg: "{{ query('cisco.sdwan.show_statistics', cmd=['app-route','stats'])}}"
        
    - name: Fetch devices state data with filter arguments
      debug:
        msg: "{{ query('cisco.sdwan.show_statistics', cmd=['app-route','stats'], detail=True, site='100', regex='.*', reachable=true, system_ip='10.1.0.2', days=1, hours=2)}}"
"""

RETURN = """
    _raw:
        description: Returns list of dictionary of devices based on input filters
        type: list
"""

display = Display()

class LookupModule(LookupBase):
    
    def validate_statistics_type_args(self,**kwargs):
        validate_show_type_args(**kwargs)
        type_args = [
            ('days', int, 'an integer'),
            ('hours', int, 'an integer')
        ]
        for arg_name, arg_type, arg_hint in type_args:
            arg_val = kwargs.get(arg_name)
            if arg_val is not None and not isinstance(arg_val, arg_type):
                raise AnsibleOptionsError(f"Parameter {arg_name} must be {arg_hint}")
        
    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        mutual_exclusive_fields = ('regex','not_regex')
        if is_mutually_exclusive(mutual_exclusive_fields,**kwargs):
            raise AnsibleOptionsError(f"Parameters are mutually exclusive: {mutual_exclusive_fields}")
        validate_show_mandatory_args(**kwargs)
        self.validate_statistics_type_args(**kwargs)
        task_output = []
        try:
            task_args = ShowStatisticsArgs(**set_show_default_args(**kwargs))
            task_output = run_task(TaskShow, task_args, get_plugin_inventory_args(variables))
        except ValidationError as ex:
            raise AnsibleLookupError(f"Invalid show statistics parameter: {ex}") from None
        except (RestAPIException, ConnectionError, FileNotFoundError, ModelException, TaskException) as ex:
            raise AnsibleLookupError(f"Show statistics error: {ex}") from None
        return task_output