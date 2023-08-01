# Sastre-Ansible - Cisco-Sastre Automation Toolset Ansible Collection

The Sastre-Ansible collection exposes Sastre or Sastre-Pro commands to Ansible Playbooks as a set of tasks and lookup plugins. Allowing users to build-up on Sastre functionality to create larger automation workflows.

<!--start requires_ansible-->
### Ansible version compatibility

This collection has been tested against following Ansible versions: **==2.10.9**.

<!--end requires_ansible-->

### Modules
Name | Description
--- | ---
[cisco.sastre.attach_edge](cisco/sastre/docs/cisco.sastre.attach_edge_module.rst)|Attach templates to WAN Edges
[cisco.sastre.attach_vsmart](cisco/sastre/docs/cisco.sastre.attach_vsmart_module.rst)|Attach templates to Vsmarts
[cisco.sastre.attach_create](cisco/sastre/docs/cisco.sastre.attach_create_module.rst)|Attach create templates and config-groups to YAML file
[cisco.sastre.backup](cisco/sastre/docs/cisco.sastre.backup_module.rst)|Save SD-WAN vManage configuration items to local backup
[cisco.sastre.device_bootstrap](cisco/sastre/docs/cisco.sastre.device_bootstrap_module.rst)|Performs device bootstrap
[cisco.sastre.certificate_restore](cisco/sastre/docs/cisco.sastre.certificate_restore_module.rst)|Restore WAN edge certificate validity status to from a backup
[cisco.sastre.certificate_set](cisco/sastre/docs/cisco.sastre.certificate_set_module.rst)|Set WAN edge certificate validity status
[cisco.sastre.delete](cisco/sastre/docs/cisco.sastre.delete_module.rst)|Delete configuration items on SD-WAN vManage
[cisco.sastre.detach_edge](cisco/sastre/docs/cisco.sastre.detach_edge_module.rst)|Detach templates from WAN Edges
[cisco.sastre.detach_vsmart](cisco/sastre/docs/cisco.sastre.detach_vsmart_module.rst)|Detach templates from vSmarts
[cisco.sastre.encrypt](cisco/sastre/docs/cisco.sastre.encrypt_module.rst)|Encrypts password
[cisco.sastre.inventory](cisco/sastre/docs/cisco.sastre.inventory_module.rst)|Returns list of SD-WAN devices from vManage
[cisco.sastre.list_certificate](cisco/sastre/docs/cisco.sastre.list_certificate_module.rst)|List configuration items or device certificate information from vManage or a local backup. Display as table or export as csv file
[cisco.sastre.list_configuration](cisco/sastre/docs/cisco.sastre.list_configuration_module.rst)|List configuration items or device certificate information from vManage or a local backup. Display as table or export as csv file
[cisco.sastre.list_transform](cisco/sastre/docs/cisco.sastre.list_transform_module.rst)|List configuration items or device certificate information from vManage or a local backup. Display as table or export as csv file
[cisco.sastre.migrate](cisco/sastre/docs/cisco.sastre.migrate_module.rst)|Migrate configuration items from a vManage release to another
[cisco.sastre.report_create](cisco/sastre/docs/cisco.sastre.report_create_module.rst)|Generate a report file containing the output from all list and show-template commands
[cisco.sastre.report_diff](cisco/sastre/docs/cisco.sastre.report_diff_module.rst)|Generate a report file containing the output from all list and show-template commands
[cisco.sastre.restore](cisco/sastre/docs/cisco.sastre.restore_module.rst)|Restore configuration items from a local backup to SD-WAN vManage
[cisco.sastre.settings_enterprise_ca](cisco/sastre/docs/cisco.sastre.settings_enterprise_ca_module.rst)|Setting enterprise root certificate
[cisco.sastre.show_devices](cisco/sastre/docs/cisco.sastre.show_devices_module.rst)|Show Device List
[cisco.sastre.show_realtime](cisco/sastre/docs/cisco.sastre.show_realtime_module.rst)|Realtime commands. Slower, but up-to-date data. vManage collect data from devices in realtime
[cisco.sastre.show_state](cisco/sastre/docs/cisco.sastre.show_state_module.rst)|State commands. Faster and up-to-date synced state data
[cisco.sastre.show_statistics](cisco/sastre/docs/cisco.sastre.show_statistics_module.rst)|Statistics commands. Faster, but data is 30 min or more old.Allows historical data queries
[cisco.sastre.show_alarms](cisco/sastre/docs/cisco.sastre.show_alarms_module.rst)|Display vManage alarms
[cisco.sastre.show_events](cisco/sastre/docs/cisco.sastre.show_events_module.rst)|Display vManage events
[cisco.sastre.show_template_references](cisco/sastre/docs/cisco.sastre.show_template_references_module.rst)|Show template references about device templates on vManage or from a local backup. Display as table or export as csv/json file
[cisco.sastre.show_template_values](cisco/sastre/docs/cisco.sastre.show_template_values_module.rst)|Show template values about device templates on vManage or from a local backup. Display as table or export as csv/json file
[cisco.sastre.transform_copy](cisco/sastre/docs/cisco.sastre.transform_copy_module.rst)|Transform copy configuration items
[cisco.sastre.transform_password](cisco/sastre/docs/cisco.sastre.transform_password_module.rst)|Transform retrieve encrypted passwords
[cisco.sastre.transform_recipe](cisco/sastre/docs/cisco.sastre.transform_recipe_module.rst)|Transform using custom recipe
[cisco.sastre.transform_rename](cisco/sastre/docs/cisco.sastre.transform_rename_module.rst)|Transform rename configuration items
[cisco.sastre.transform_update](cisco/sastre/docs/cisco.sastre.transform_update_module.rst)|Transform using update recipe
[cisco.sastre.transform_updatepwd](cisco/sastre/docs/cisco.sastre.transform_updatepwd_module.rst)|Transform update password configuration items
<!--end collection content-->

### Lookup Plugins
Name | Description
--- | ---
[cisco.sastre.devices](cisco/sastre/docs/cisco.sastre.devices_lookup_plugin.rst)|Fetches list of SD-WAN devices from vManage
[cisco.sastre.realtime](cisco/sastre/docs/cisco.sastre.realtime_lookup_plugin.rst)|Realtime commands. Slower, but up-to-date data. vManage collect data from devices in realtime
[cisco.sastre.state](cisco/sastre/docs/cisco.sastre.state_lookup_plugin.rst)|State commands. Faster and up-to-date synced state data
[cisco.sastre.statistics](cisco/sastre/docs/cisco.sastre.statistics_lookup_plugin.rst)|Statistics commands. Faster, but data is 30 min or more old.Allows historical data queries


## Installation

### Building the collection

Go to the top-level directory of this repo and run the collection build command:
```
% ls
CHANGELOG.md		README.md			requirements.txt
Jenkinsfile			cisco				LICENSE

% ansible-galaxy collection build cisco/sastre
Created collection for cisco.sastre at cisco-sastre-1.0.14.tar.gz
```

- Note that it creates a tar.gz artifact, which can then be used to install to the ansible environment

### Installing the collection

You can install the Sastre-Ansible collection with the Ansible Galaxy CLI:
```
% ansible-galaxy collection install -f cisco-sastre-1.0.14.tar.gz
Process install dependency map
Starting collection install process
Installing 'cisco.sastre:1.0.14' to '~/.ansible/collections/ansible_collections/cisco/sastre'
```

### Dependencies

In addition to Ansible itself, [Sastre](https://github.com/CiscoDevNet/sastre) or [Sastre-Pro](https://wwwin-github.cisco.com/AIDE/Sastre-Pro) need to be installed in the Python environment being used by Ansible.

Please refer to the corresponding README files for Sastre/Sastre-Pro install instructions.

## Using Sastre-Ansible in your playbooks

You can call modules by their Fully Qualified Collection Namespace (FQCN), such as `cisco.sastre.backup`.
The following example task saves vManage configuration to local backup:

```yaml
---
- name: "Backup vManage configuration"
  cisco.sastre.backup: 
    address: "198.18.1.10"
    port: 8443
    user: admin
    password: admin
    tenant: customer 
    timeout: 300
    verbose: INFO
    workdir: /home/user/backups
    no_rollover: false
    save_running: true
    regex: ".*"
    tags: "all"
```