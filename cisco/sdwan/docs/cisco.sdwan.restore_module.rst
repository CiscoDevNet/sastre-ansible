:source: restore.py

:orphan:

.. _cisco.sdwan.restore_module:


cisco.sdwan.restore - Restore configuration items from a local backup to SD-WAN vManage.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


.. contents::
   :local:
   :depth: 2


Synopsis
--------
- This restore module connects to SD-WAN vManage using HTTP REST to updated configuration data stored in local default backup or configured argument local backup folder. This module contains multiple arguments with connection and filter details to restore all or specific configurtion data. A log file is created under a "logs" directory. This "logs" directory is relative to directory where Ansible runs.




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
                    <b>attach</b>
                    <br/><div style="font-size: small; color: red">bool</div>                                                        </td>
                                <td>
                                                                                                                                                                                                                    <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Attach devices to templates and activate vSmart policy after restoring items</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>dryrun</b>
                    <br/><div style="font-size: small; color: red">bool</div>                                                        </td>
                                <td>
                                                                                                                                                                                                                    <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>dry-run mode. Items to be restored are listed but not pushed to vManage.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>force</b>
                    <br/><div style="font-size: small; color: red">bool</div>                                                        </td>
                                <td>
                                                                                                                                                                                                                    <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Target vManage items with the same name as the corresponding item in workdir are updated with the contents from workdir. Without this option, those items are skipped and not overwritten.</div>
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
                    <b>pid</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">0</div>
                                    </td>
                                                                <td>
                                                                        <div>CX project id or can also be defined via CX_PID environment variable. This is collected for AIDE reporting purposes only.</div>
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
                                                                        <div>Regular expression matching item names to be restored, within selected tags</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>tag</b>
                    <br/><div style="font-size: small; color: red">str</div>                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
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
                                                                        <div>Tag for selecting items to be restored. Items that are dependencies of the specified tag are automatically included. Available tags are template_feature, policy_profile, policy_definition, all, policy_list, policy_vedge, policy_voice, policy_vsmart, template_device, policy_security, policy_customapp. Special tag &quot;all&quot; selects all items.</div>
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
                    <b>verbose</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>NOTSET</li>
                                                                                                                                                                                                <li><div style="color: blue"><b>DEBUG</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>INFO</li>
                                                                                                                                                                                                <li>WARNING</li>
                                                                                                                                                                                                <li>ERROR</li>
                                                                                                                                                                                                <li>CRITICAL</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Defines to control log level for the logs generated under &quot;logs/sastre.log&quot; when Ansible script is run. Supported log levels are NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL</div>
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

    
    - name: Restore vManage configuration
      cisco.sdwan.restore:
        address: "198.18.1.10"
        port: 8443
        user: "admin"
        password: "admin"
        timeout: 300
        pid: "2"
        verbose: "INFO"
        workdir: "/home/user/backups"
        regex: ".*"
        dryrun: False
        attach: False
        force: False
        tag: "template_device"
    - name: Restore all vManage configuration
      cisco.sdwan.restore:
        address: "198.18.1.10"
        port: 8443
        user: "admin"
        password: "admin"
        timeout: 300
        pid: "2"
        verbose: "INFO"
        workdir: "/home/user/backups"
        regex: ".*"
        dryrun: False
        attach: False
        force: False
        tag: "all"
    - name: Restore vManage configuration with some vManage config arguments saved in environment variables
      cisco.sdwan.restore:
        timeout: 300
        verbose: "INFO"
        workdir: "/home/user/backups"
        regex: ".*"
        dryrun: False
        attach: False
        force: False
        tag: "all"
    - name: Restore vManage configuration with all defaults
      cisco.sdwan.restore:
        address: "198.18.1.10"
        user: "admin"
        password: "admin"
        tag: "all"





Status
------




Author
~~~~~~

- Satish Kumar Kamavaram (sakamava@cisco.com)


.. hint::
    If you notice any issues in this documentation you can `edit this document <https://github.com/ansible/ansible/edit/devel/lib/ansible/modules/restore.py?description=%3C!---%20Your%20description%20here%20--%3E%0A%0A%2Blabel:%20docsite_pr>`_ to improve it.
