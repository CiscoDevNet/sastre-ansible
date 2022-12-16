#! /usr/bin/env python3
from cisco_sdwan.base.rest_api import Rest
from typing import NamedTuple, List, Optional
from cisco_sdwan.base.models_vmanage import Device
from cisco_sdwan.tasks.common import regex_search
from cisco_sdwan.tasks.models import TaskArgs
from cisco_sdwan.tasks.validators import validate_regex, validate_site_id, validate_ipv4
from pydantic import validator
from .common import sdwan_api_args

iter_fields = ('uuid', 'host-name', 'deviceId', 'site-id', 'reachability', 'device-type', 'device-model', 'version')


class DeviceInfo(NamedTuple):
    uuid: str
    name: str
    system_ip: str
    site_id: str
    state: str
    model: str
    version: str
    device_type: str


def device_info_iter(api, cedge_models, task_args):
    def device_type(device_class, device_model):
        if device_class == 'vedge':
            return 'cedge' if device_model in cedge_models else 'vedge'
        return device_class

    def match_name(device_name):
        if task_args.regex_list is not None:
            return any(regex_search(regex_entry, device_name) for regex_entry in task_args.regex_list)

        regex = task_args.regex or task_args.not_regex
        return regex is None or regex_search(regex, device_name, inverse=task_args.regex is None)

    for uuid, name, system_ip, site_id, state, d_class, model, version in Device.get_raise(api).iter(*iter_fields):
        d_type = device_type(d_class, model)
        if (match_name(name) and (not task_args.reachable or state == 'reachable') and
                (task_args.site is None or site_id == task_args.site) and
                (task_args.system_ip is None or system_ip == task_args.system_ip) and
                (task_args.device_type is None or d_type == task_args.device_type)):
            yield DeviceInfo(uuid, name, system_ip, site_id, state, model, version, d_type)

        continue


def get_matched_devices(module_param_dict, task_args):
    with Rest(**sdwan_api_args(module_param_dict=module_param_dict)) as api:
        cedge_set = {
            elem['name'] for elem in api.get('device/models')['data']
            if elem['deviceClass'] in {'cisco-router', 'eio-lte', 'vbranch'}
        }
        return [elem._asdict() for elem in device_info_iter(api, cedge_set, task_args)]


class InventoryArgs(TaskArgs):
    regex_list: Optional[List[str]] = None
    regex: Optional[str] = None
    not_regex: Optional[str] = None
    reachable: bool = False
    site: Optional[str] = None
    system_ip: Optional[str] = None
    device_type: Optional[str] = None

    # Validators
    _validate_regex_list = validator('regex_list', allow_reuse=True, each_item=True)(validate_regex)
    _validate_regex = validator('regex', 'not_regex', allow_reuse=True)(validate_regex)
    _validate_site_id = validator('site', allow_reuse=True)(validate_site_id)
    _validate_ipv4 = validator('system_ip', allow_reuse=True)(validate_ipv4)
