:source: backup.py

:orphan:

.. _backup_module:


backup - Save SD-WAN vManage configuration items to local backup
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


.. contents::
   :local:
   :depth: 2


Synopsis
--------
- This backup module connects to SD-WAN vManage using HTTP REST and returned HTTP responses are stored to default or configured argument local backup folder. This module contains multiple arguments with connection and filter details to backup all or specific configurtion data.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                        <th width="100%">Comments</th>
        </tr>
                    <tr>
                                                                <td colspan="1">
                    <b>address</b>
                    <br/><div style="font-size: small; color: red">str</div>                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>vManage IP address or can also be defined via VMANAGE_IP environment variable</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>no_rollover</b>
                    <br/><div style="font-size: small; color: red">bool</div>                                                        </td>
                                <td>
                                                                                                                                                                                                                    <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>By default, if workdir already exists (before a new backup is saved) the old workdir is renamed using a rolling naming scheme. &quot;True&quot; disables the automatic rollover. &quot;False&quot; enables the automatic rollover</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>not_regex</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Regular expression matching item names NOT to backup, within selected tags</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>password</b>
                    <br/><div style="font-size: small; color: red">str</div>                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>password or can also be defined via VMANAGE_PASSWORD environment variable.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>port</b>
                    <br/><div style="font-size: small; color: red">int</div>                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">8443</div>
                                    </td>
                                                                <td>
                                                                        <div>vManage port number or can also be defined via VMANAGE_PORT environment variable</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>regex</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Regular expression matching item names to be backed up, within selected tags</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>save_running</b>
                    <br/><div style="font-size: small; color: red">bool</div>                                                        </td>
                                <td>
                                                                                                                                                                                                                    <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Include the running config from each node to the backup. This is useful for reference or documentation purposes. It is not needed by the restore task.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>tags</b>
                    <br/><div style="font-size: small; color: red">list</div>                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>template_feature</li>
                                                                                                                                                                                                <li>policy_profile</li>
                                                                                                                                                                                                <li>policy_definition</li>
                                                                                                                                                                                                <li>all</li>
                                                                                                                                                                                                <li>policy_list</li>
                                                                                                                                                                                                <li>policy_vedge</li>
                                                                                                                                                                                                <li>policy_voice</li>
                                                                                                                                                                                                <li>policy_vsmart</li>
                                                                                                                                                                                                <li>template_device</li>
                                                                                                                                                                                                <li>policy_security</li>
                                                                                                                                                                                                <li>policy_customapp</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Defines one or more tags for selecting items to be backed up. Multiple tags should be configured as list. Available tags are template_feature, policy_profile, policy_definition, all, policy_list, policy_vedge, policy_voice, policy_vsmart, template_device, policy_security, policy_customapp. Special tag &quot;all&quot; selects all items, including WAN edge certificates and device configurations.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>tenant</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>tenant name, when using provider accounts in multi-tenant deployments.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>timeout</b>
                    <br/><div style="font-size: small; color: red">int</div>                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">300</div>
                                    </td>
                                                                <td>
                                                                        <div>vManage REST API timeout in seconds</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>user</b>
                    <br/><div style="font-size: small; color: red">str</div>                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>username or can also be defined via VMANAGE_USER environment variable.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>workdir</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">backup_&lt;address&gt;_&lt;yyyymmdd&gt;</div>
                                    </td>
                                                                <td>
                                                                        <div>Defines the location (in the local machine) where vManage data files are located. By default, it follows the format &quot;backup_&lt;address&gt;_&lt;yyyymmdd&gt;&quot;. The workdir argument can be used to specify a different location. workdir is under a &#x27;data&#x27; directory. This &#x27;data&#x27; directory is relative to the directory where Ansible script is run.</div>
                                                                                </td>
            </tr>
                        </table>
    <br/>


Notes
-----

.. note::
    - Tested against 20.4.1.1


Examples
--------

.. code-block:: yaml+jinja

    
    - name: "Backup vManage configuration"
      cisco.sdwan.backup: 
        address: "198.18.1.10"
        port: 8443
        user: admin
        password: admin
        timeout: 300
        workdir: /home/user/backups
        no_rollover: false
        save_running: true
        regex: ".*"
        tags: 
          - template_device
          - template_feature
    - name: "Backup all vManage configuration"
      cisco.sdwan.backup: 
        address: "198.18.1.10"
        port: 8443
        user: admin
        password: admin
        timeout: 300
        verbose: INFO
        workdir: /home/user/backups
        no_rollover: false
        save_running: true
        regex: ".*"
        tags: "all"
    - name: "Backup vManage configuration with some vManage config arguments saved in environment variables"
      cisco.sdwan.backup: 
        timeout: 300
        workdir: /home/user/backups
        no_rollover: false
        save_running: true
        regex: ".*"
        tags: "all"
    - name: "Backup vManage configuration with all defaults"
      cisco.sdwan.backup: 
        address: "198.18.1.10"
        user: admin
        password: admin
        tags: "all"





Status
------




Author
~~~~~~

- UNKNOWN


.. hint::
    If you notice any issues in this documentation you can `edit this document <https://github.com/ansible/ansible/edit/devel/lib/ansible/modules/backup.py?description=%3C!---%20Your%20description%20here%20--%3E%0A%0A%2Blabel:%20docsite_pr>`_ to improve it.
