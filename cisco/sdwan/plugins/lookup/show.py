#!/usr/bin/python
import logging
from ansible.errors import AnsibleLookupError, AnsibleOptionsError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
from cisco_sdwan.tasks.implementation import TaskShow
from cisco_sdwan.tasks.utils import (
    OpType, RTCmdSemantics, StateCmdSemantics,
    StatsCmdSemantics
)
from cisco_sdwan.cmd import (
    REST_TIMEOUT
)


DOCUMENTATION = """
lookup: show
author: Satish Kumar Kamavaram (sakamava@cisco.com)
version_added: "1.0"
short_description: Run vManage real-time, state or statistics commands; collecting data from one or more devices.
description:
    - This lookup returns list of SD-WAN devices from vManage, contains multiple arguments with 
      connection and filter details to retrieve devices,realtime,state,statistics device data.
options:
    _terms:
        description: >
                Sub-task option for show task for collection of data. 
                Supported values are 'devices','realtime','state','statistics'
        required: True
        type: str
    cmds:
        description: >
                Group of, or specific command to execute. Applicable and mandatory for realtime,state,statistics sub-task options.
                For realtime , Group options are all, app-route, bfd, control, dpi, interface, omp, software, system, tunnel.
                Command options are app-route sla-class, app-route stats, bfd sessions, control connections, 
                control local-properties, dpi summary, interface info, omp adv-routes, 
                omp peers, omp summary, software info, system status, tunnel stats.
                For state , Group options are all, bfd, control, interface, omp, system. 
                Command options are bfd sessions, control connections, control local-properties, interface cedge,
                interface vedge, omp peers, system info.
                For statistics , Group options are all, app-route, interface, system. 
                Command options are app-route stats, interface info, system status.
        required: False
        type: list
    regex:
        description: Regular expression matching device name, type or model to display
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
    detail:
        description: Detailed output. Applicable to only realtime,state,statistics sub-task options
        required: false
        type: bool
        default: False
    days:
        description: Query statistics from days ago (default is now). Applicable to only statistics sub-task option
        required: false
        type: int
        default: 0
    hours:
        description: Query statistics from hours ago (default is now). Applicable to only statistics sub-task option
        required: false
        type: int
        default: 0
    verbose:
        description: Defines to control log level for the logs generated under "logs/sastre.log" when Ansible script is run.
                    Supported log levels are NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL
        required: false
        type: str
        default: "DEBUG"
    pid:
        description: CX project id or can also be defined via CX_PID environment variable. 
                      This is collected for AIDE reporting purposes only.
        required: false
        type: str
        default: '0'
"""

EXAMPLES = """
    - name: Fetch all devices
      debug:
        msg: "{{ query('cisco.sdwan.show', 'devices')}}"
        
    - name: Fetch devices with filter arguments
      debug:
        msg: "{{ query('cisco.sdwan.show', 'devices',site='100',regex='.*', reachable=true,system_ip='10.1.0.2' ,pid=1,verbose='INFO')}}"

    - name: Fetch all devices realtime data
      debug:
        msg: "{{ query('cisco.sdwan.show', 'realtime',cmds=['app-route','sla-class'])}}"
        
    - name: Fetch devices realtime data with filter arguments
      debug:
        msg: "{{ query('cisco.sdwan.show', 'realtime',cmds=['app-route','sla-class'],detail=true,site='100',regex='.*', reachable=true,system_ip='10.1.0.2',pid='1',verbose='INFO')}}"
        
    - name: Fetch all devices state data
      debug:
        msg: "{{ query('cisco.sdwan.show', 'state',cmds=['bfd','sessions'])}}"
        
    - name: Fetch devices state data with filter arguments
      debug:
        msg: "{{ query('cisco.sdwan.show', 'state',cmds=['bfd','sessions'],detail=true,site='100',regex='.*', reachable=true,system_ip='10.1.0.2',pid='1',verbose='INFO')}}"
        
    - name: Fetch all devices statistics data
      debug:
        msg: "{{ query('cisco.sdwan.show', 'statistics',cmds=['app-route','stats'])}}"
        
    - name: Fetch devices statistics data with filter arguments
      debug:
        msg: "{{ query('cisco.sdwan.show', 'statistics',cmds=['app-route','stats'],detail=true,site='100',regex='.*', reachable=true,system_ip='10.1.0.2',pid='1',verbose='INFO',days=1,hours=2)}}"
"""

RETURN = """
    _raw:
        description: Returns list of dictionary of devices based on input filters
        type: list
"""

display = Display()
sub_task_list = ['realtime', 'state', 'statistics', 'devices']


class LookupModule(LookupBase):

    def parse_optional_args(self, **kwargs):
        optional_args = [
            ('regex', str, 'a string', None),
            ('not_regex', str, 'a string', None),
            ('reachable', bool, 'a boolean', False),
            ('site', str, 'a string', None),
            ('system_ip', str, 'a string', None),
            ('csv', str, 'a string', None),
            ('detail', bool, 'a boolean', False),
            ('cmds', list, 'a list of string', []),
            ('days', int, 'an integer', 0),
            ('hours', int, 'an integer', 0),
            ('verbose', str, 'a string', DEFAULT_LOG_LEVEL)
        ]
        for arg_name, arg_type, arg_hint, arg_default in optional_args:
            arg_val = kwargs.get(arg_name)
            if arg_val is None:
                arg_val = arg_default
            elif not isinstance(arg_val, arg_type):
                raise AnsibleOptionsError(f"Parameter {arg_name} must be {arg_hint}")

            setattr(self, arg_name, arg_val)

    def get_show_devices_args(self, sub_task, show_common_args):
        devices_args = {
            'subtask_info': sub_task,
            'subtask_handler': TaskShow.devices
        }
        show_common_args.update(devices_args)
        return show_common_args

    def get_show_realtime_args(self, sub_task, show_common_args):
        realtime_args = {
            'subtask_info': sub_task,
            'subtask_handler': TaskShow.realtime,
            'cmds': self.cmds,
            'detail': self.detail
        }
        show_common_args.update(realtime_args)
        return show_common_args

    def get_show_state_args(self, sub_task, show_common_args):
        state_args = {
            'subtask_info': sub_task,
            'subtask_handler': TaskShow.bulk_state,
            'cmds': self.cmds,
            'detail': self.detail
        }
        show_common_args.update(state_args)
        return show_common_args

    def get_show_statistics_args(self, sub_task, show_common_args):
        statistics_args = {
            'subtask_info': sub_task,
            'subtask_handler': TaskShow.bulk_stats,
            'days': self.days,
            'hours': self.hours,
            'cmds': self.cmds,
            'detail': self.detail
        }
        show_common_args.update(statistics_args)
        return show_common_args

    def validate_show_cmds(self, cmds_arg, values, op_type):
        if values is not None:
            try:
                if op_type == OpType.RT:
                    cmd_obj = RTCmdSemantics(values, cmds_arg)
                    cmd_obj.__call__(object, cmd_obj, values)
                elif op_type == OpType.STATE:
                    cmd_obj = StateCmdSemantics(values, cmds_arg)
                    cmd_obj.__call__(object, cmd_obj, values)
                elif op_type == OpType.STATS:
                    cmd_obj = StatsCmdSemantics(values, cmds_arg)
                    cmd_obj.__call__(object, cmd_obj, values)
            except Exception as ex:
                logging.getLogger(__name__).critical(ex)
                raise Exception(f'{cmds_arg}: Invalid value(s): {values}:{ex}')

    def show_validations(self, sub_task):
        validate_regex(REGEX, self.regex)
        validate_site(SITE, self.site)
        validate_ipv4(SYSTEM_IP, self.system_ip)
        validate_filename(CSV, self.csv)

        op_type = None
        if sub_task == sub_task_list[0]:
            op_type = OpType.RT
        elif sub_task == sub_task_list[1]:
            op_type = OpType.STATE
        elif sub_task == sub_task_list[2]:
            op_type = OpType.STATS
            validate_time(DAYS, self.days)
            validate_time(HOURS, self.hours)

        if sub_task != sub_task_list[3]:
            self.validate_show_cmds(CMDS, self.cmds, op_type)

    def get_env_args(self, variables):
        env_args = {
            ADDRESS: variables.get('ansible_host'),
            PORT: (8443 if variables.get('vmanage_port') is None else variables.get('vmanage_port')),
            USER: variables.get('ansible_user'),
            PASSWORD: variables.get('ansible_password'),
            PID: (DEFAULT_PID if variables.get('pid') is None else variables.get('pid')),
            TIMEOUT: (REST_TIMEOUT if variables.get('timeout') is None else variables.get('timeout'))
        }
        return env_args

    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        self.parse_optional_args(**kwargs)
        set_log_level(self.verbose)
        output_list = []
        task_output = []
        show_common_args = {
            'regex': self.regex,
            'not_regex': self.not_regex,
            'reachable': self.reachable,
            'site': self.site,
            'system_ip': self.system_ip,
            'csv': self.csv,
            'task_output': task_output
        }
        task_show = TaskShow()
        for term in terms:
            if term not in sub_task_list:
                raise AnsibleOptionsError(f"Task: {term} must be one of {sub_task_list}")
            try:
                if term == sub_task_list[0]:
                    show_args = self.get_show_realtime_args(term, show_common_args)
                elif term == sub_task_list[1]:
                    show_args = self.get_show_state_args(term, show_common_args)
                elif term == sub_task_list[2]:
                    show_args = self.get_show_statistics_args(term, show_common_args)
                elif term == sub_task_list[3]:
                    show_args = self.get_show_devices_args(term, show_common_args)

                self.show_validations(term)
                process_task(task_show, self.get_env_args(variables), **show_args)
                if task_output and isinstance(task_output, list) and len(task_output):
                    output = ''.join(task_output)
                    output = output.split('\n')
                    output_list.append(output)
                else:
                    display.display("Task Show: {} completed successfully. csv files @ {}".format(term, self.csv))

            except Exception as ex:
                raise AnsibleLookupError(ex) from None

                # return task_output
        return output_list
