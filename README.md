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
[cisco.sdwan.backup](https://github.com/ansible-collections/cisco.sdwan/blob/main/docs/cisco.ios.backup.rst)|Save SD-WAN vManage configuration items to local backup
[cisco.sdwan.restore](https://github.com/ansible-collections/cisco.sdwan/blob/main/docs/cisco.ios.restore.rst)|Restore configuration items from a local backup to SD-WAN vManage.
[cisco.sdwan.delete](https://github.com/ansible-collections/cisco.sdwan/blob/main/docs/cisco.ios.delete.rst)|Delete configuration items on SD-WAN vManage.

<!--end collection content-->
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
    no_rollover: false
    password: admin
    pid: "2"
    port: 8443
    regex: .*
    tags: all
    timeout: 300
    user: admin
    verbose: INFO
    workdir: /home/user/backups

```