#! /usr/bin/env python3
from ansible.errors import AnsibleLookupError, AnsibleOptionsError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
from pydantic import ValidationError
from cisco_sdwan.tasks.implementation import TaskShow, ShowStateArgs
from cisco_sdwan.tasks.common import TaskException
from cisco_sdwan.base.rest_api import RestAPIException
from cisco_sdwan.base.models_base import ModelException
from ansible_collections.cisco.sdwan.plugins.module_utils.common_lookup import (run_task, get_lookup_args,
                                                                                validate_show_type_args,
                                                                                validate_show_mandatory_args,
                                                                                set_show_default_args,
                                                                                is_mutually_exclusive)

DOCUMENTATION = """
lookup: state
version_added: "1.0"
short_description: State commands. Faster and up-to-date synced state data.
description:
    - This show_devices lookup returns list of SD-WAN devices from vManage, contains multiple arguments with 
      connection and filter details to retrieve state device data.
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
                Group options are all, bfd, control, interface, omp, system. 
                Command options are bfd sessions, control connections, control local-properties, interface cedge,
                interface vedge, omp peers, system info.
        required: True
        type: list
    detail:
        description: Detailed output.
        required: false
        type: bool
        default: False
"""

EXAMPLES = """
    - name: Fetch all devices state data
      debug:
        msg: "{{ query('cisco.sdwan.state', cmd=['bfd','sessions'])}}"
        
    - name: Fetch devices state data with filter arguments
      debug:
        msg: "{{ query('cisco.sdwan.state', cmd=['bfd','sessions'], detail=True, site='100', regex='.*', reachable=true, system_ip='10.1.0.2')}}"
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
        validate_show_mandatory_args(**kwargs)
        validate_show_type_args(**kwargs)

        try:
            task_args = ShowStateArgs(**set_show_default_args(**kwargs))
            task_output = run_task(TaskShow, task_args, get_lookup_args(variables))
        except ValidationError as ex:
            raise AnsibleLookupError(f"Invalid show state parameter: {ex}") from None
        except (RestAPIException, ConnectionError, FileNotFoundError, ModelException, TaskException) as ex:
            raise AnsibleLookupError(f"Show state error: {ex}") from None

        return task_output
