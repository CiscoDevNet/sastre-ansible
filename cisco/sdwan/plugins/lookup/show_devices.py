#! /usr/bin/env python3
from ansible.errors import AnsibleLookupError, AnsibleOptionsError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
from pydantic import ValidationError
from cisco_sdwan.tasks.implementation._show import TaskShow, ShowDevicesArgs
from cisco_sdwan.tasks.common import TaskException
from cisco_sdwan.base.rest_api import RestAPIException
from cisco_sdwan.base.models_base import ModelException
from ansible_collections.cisco.sdwan.plugins.module_utils.common import is_mutually_exclusive
from ansible_collections.cisco.sdwan.plugins.module_utils.common_lookup import (run_task, get_plugin_inventory_args,
                                                                                validate_show_type_args,
                                                                                set_show_default_args)

DOCUMENTATION = """
lookup: show_devices
version_added: "1.0"
short_description: Show Device List
description:
    - This show_devices lookup returns list of SD-WAN devices from vManage, contains multiple arguments with 
      connection and filter details to retrieve devices data.
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
"""

EXAMPLES = """
    - name: Fetch all devices
      debug:
        msg: "{{ query('cisco.sdwan.show_devices')}}"
        
    - name: Fetch devices with filter arguments
      debug:
        msg: "{{ query('cisco.sdwan.show_devices', site='100',regex='.*', reachable=true,system_ip='10.1.0.2')}}"
"""

RETURN = """
    _raw:
        description: Returns list of dictionary of devices based on input filters
        type: list
"""

display = Display()


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        mutual_exclusive_fields = ('regex', 'not_regex')
        if is_mutually_exclusive(mutual_exclusive_fields, **kwargs):
            raise AnsibleOptionsError(f"Parameters are mutually exclusive: {mutual_exclusive_fields}")
        validate_show_type_args(**kwargs)
        task_output = []
        try:
            task_args = ShowDevicesArgs(**set_show_default_args(**kwargs))
            task_output = run_task(TaskShow, task_args, get_plugin_inventory_args(variables))
        except ValidationError as ex:
            raise AnsibleLookupError(f"Invalid show devices parameter: {ex}") from None
        except (RestAPIException, ConnectionError, FileNotFoundError, ModelException, TaskException) as ex:
            raise AnsibleLookupError(f"Show devices error: {ex}") from None
        return task_output
