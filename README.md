# Cisco SDWAN Collection

The Ansible Cisco SDWAN collection includes all the Sastre Pro operations to assist with managing configuration elements from Cisco SD-WAN deployments.

This collection has been tested against Cisco SDWAN vManage version 20.4.1.1.

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **==2.10.9**.

<!--end requires_ansible-->

### Modules
Name | Description
--- | ---
[cisco.sdwan.attach_edge](https://wwwin-github.cisco.com/AIDE/Sastre-Ansible/blob/master/cisco/sdwan/docs/cisco.sdwan.attach_edge_module.rst)|Attach templates to WAN Edges
[cisco.sdwan.attach_vsmart](https://wwwin-github.cisco.com/AIDE/Sastre-Ansible/blob/master/cisco/sdwan/docs/cisco.sdwan.attach_vsmart_module.rst)|Attach templates to Vsmarts
[cisco.sdwan.backup](https://wwwin-github.cisco.com/AIDE/Sastre-Ansible/blob/master/cisco/sdwan/docs/cisco.sdwan.backup_module.rst)|Save SD-WAN vManage configuration items to local backup
[cisco.sdwan.certificate_restore](https://wwwin-github.cisco.com/AIDE/Sastre-Ansible/blob/master/cisco/sdwan/docs/cisco.sdwan.certificate_restore_module.rst)|Restore WAN edge certificate validity status to from a backup
[cisco.sdwan.certificate_set](https://wwwin-github.cisco.com/AIDE/Sastre-Ansible/blob/master/cisco/sdwan/docs/cisco.sdwan.certificate_set_module.rst)|Set WAN edge certificate validity status
[cisco.sdwan.delete](https://wwwin-github.cisco.com/AIDE/Sastre-Ansible/blob/master/cisco/sdwan/docs/cisco.sdwan.delete_module.rst)|Delete configuration items on SD-WAN vManage
[cisco.sdwan.detach_edge](https://wwwin-github.cisco.com/AIDE/Sastre-Ansible/blob/master/cisco/sdwan/docs/cisco.sdwan.detach_edge_module.rst)|Detach templates from WAN Edges
[cisco.sdwan.detach_vsmart](https://wwwin-github.cisco.com/AIDE/Sastre-Ansible/blob/master/cisco/sdwan/docs/cisco.sdwan.detach_vsmart_module.rst)|Detach templates from vSmarts
[cisco.sdwan.list_certificate](https://wwwin-github.cisco.com/AIDE/Sastre-Ansible/blob/master/cisco/sdwan/docs/cisco.sdwan.list_certificate_module.rst)|List configuration items or device certificate information from vManage or a local backup. Display as table or export as csv file
[cisco.sdwan.list_configuration](https://wwwin-github.cisco.com/AIDE/Sastre-Ansible/blob/master/cisco/sdwan/docs/cisco.sdwan.list_configuration_module.rst)|List configuration items or device certificate information from vManage or a local backup. Display as table or export as csv file
[cisco.sdwan.list_transform](https://wwwin-github.cisco.com/AIDE/Sastre-Ansible/blob/master/cisco/sdwan/docs/cisco.sdwan.list_transform_module.rst)|List configuration items or device certificate information from vManage or a local backup. Display as table or export as csv file
[cisco.sdwan.migrate](https://wwwin-github.cisco.com/AIDE/Sastre-Ansible/blob/master/cisco/sdwan/docs/cisco.sdwan.migrate_module.rst)|Migrate configuration items from a vManage release to another
[cisco.sdwan.report_create](https://wwwin-github.cisco.com/AIDE/Sastre-Ansible/blob/master/cisco/sdwan/docs/cisco.sdwan.report_create_module.rst)|Generate a report file containing the output from all list and show-template commands
[cisco.sdwan.report_diff](https://wwwin-github.cisco.com/AIDE/Sastre-Ansible/blob/master/cisco/sdwan/docs/cisco.sdwan.report_diff_module.rst)|Generate a report file containing the output from all list and show-template commands
[cisco.sdwan.restore](https://wwwin-github.cisco.com/AIDE/Sastre-Ansible/blob/master/cisco/sdwan/docs/cisco.sdwan.restore_module.rst)|Restore configuration items from a local backup to SD-WAN vManage
[cisco.sdwan.show_devices](https://wwwin-github.cisco.com/AIDE/Sastre-Ansible/blob/master/cisco/sdwan/docs/cisco.sdwan.show_devices_module.rst)|Show Device List
[cisco.sdwan.show_realtime](https://wwwin-github.cisco.com/AIDE/Sastre-Ansible/blob/master/cisco/sdwan/docs/cisco.sdwan.show_realtime_module.rst)|Realtime commands. Slower, but up-to-date data. vManage collect data from devices in realtime
[cisco.sdwan.show_state](https://wwwin-github.cisco.com/AIDE/Sastre-Ansible/blob/master/cisco/sdwan/docs/cisco.sdwan.show_state_module.rst)|State commands. Faster and up-to-date synced state data
[cisco.sdwan.show_statistics](https://wwwin-github.cisco.com/AIDE/Sastre-Ansible/blob/master/cisco/sdwan/docs/cisco.sdwan.show_statistics_plugin.rst)|Statistics commands. Faster, but data is 30 min or more old.Allows historical data queries
[cisco.sdwan.show_template_references](https://wwwin-github.cisco.com/AIDE/Sastre-Ansible/blob/master/cisco/sdwan/docs/cisco.sdwan.show_template_references_module.rst)|Show template references about device templates on vManage or from a local backup. Display as table or export as csv/json file
[cisco.sdwan.show_template_values](https://wwwin-github.cisco.com/AIDE/Sastre-Ansible/blob/master/cisco/sdwan/docs/cisco.sdwan.show_template_values_module.rst)|Show template values about device templates on vManage or from a local backup. Display as table or export as csv/json file
<!--end collection content-->

### Lookup Plugins
Name | Description
--- | ---
[cisco.sdwan.devices](https://wwwin-github.cisco.com/AIDE/Sastre-Ansible/blob/master/cisco/sdwan/docs/cisco.sdwan.devices_lookup_plugin.rst)|Fetches list of SD-WAN devices from vManage
[cisco.sdwan.show_devices](https://wwwin-github.cisco.com/AIDE/Sastre-Ansible/blob/master/cisco/sdwan/docs/cisco.sdwan.show_devices_lookup_plugin.rst)|Show Device List
[cisco.sdwan.show_realtime](https://wwwin-github.cisco.com/AIDE/Sastre-Ansible/blob/master/cisco/sdwan/docs/cisco.sdwan.show_realtime_lookup_plugin.rst)|Realtime commands. Slower, but up-to-date data. vManage collect data from devices in realtime
[cisco.sdwan.show_state](https://wwwin-github.cisco.com/AIDE/Sastre-Ansible/blob/master/cisco/sdwan/docs/cisco.sdwan.show_state_lookup_plugin.rst)|State commands. Faster and up-to-date synced state data
[cisco.sdwan.show_statistics](https://wwwin-github.cisco.com/AIDE/Sastre-Ansible/blob/master/cisco/sdwan/docs/cisco.sdwan.show_statistics_plugin.rst)|Statistics commands. Faster, but data is 30 min or more old.Allows historical data queries

## Building the collection

From the top directory:

    % ls
    CHANGELOG.md			LICENSE				cisco				requirements.txt
    Jenkinsfile			README.md
    % ansible-galaxy collection build cisco/sdwan


## Installing this collection

You can install the Cisco SDWAN collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install cisco.sdwan

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: cisco.sdwan
```

## Dependency

Install [Sastre-Pro](https://wwwin-github.cisco.com/AIDE/Sastre-Pro) using pip 


### Using modules from the Cisco SDWAN collection in your playbooks

You can call modules by their Fully Qualified Collection Namespace (FQCN), such as `cisco.sdwan.backup`.
The following example task saves vManage configuration to local backup:

```yaml
---
- name: "Backup vManage configuration"
  cisco.sdwan.backup: 
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