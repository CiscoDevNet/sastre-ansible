:source: attach_vsmart.py

:orphan:

.. _attach_vsmart_module:


attach_vsmart - Attach templates to Vsmarts
+++++++++++++++++++++++++++++++++++++++++++


.. contents::
   :local:
   :depth: 2


Synopsis
--------
- This attach module connects to SD-WAN vManage using HTTP REST to updated configuration data stored in local default backup or configured argument local backup folder. This module contains multiple arguments with connection and filter details to attach Vsmarts to templates. When multiple filters are defined, the result is an AND of all filters. Dry-run can be used to validate the expected outcome.The number of devices to include per attach request (to vManage) can be defined with the batch param.




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
                    <b>activate</b>
                    <br/><div style="font-size: small; color: red">bool</div>                                                        </td>
                                <td>
                                                                                                                                                                                                                    <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Activate centralized policy after vSmart template attach/deploy.</div>
                                                                                </td>
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
                    <b>batch</b>
                    <br/><div style="font-size: small; color: red">int</div>                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">200</div>
                                    </td>
                                                                <td>
                                                                        <div>Maximum number of devices to include per vManage attach request.</div>
                                                                                </td>
            </tr>
            <tr>
                                                                <td colspan="1">
                    <b>config_groups</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Regular expression selecting config-groups to deploy. Match on config-group name.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>devices</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Regular expression selecting devices to attach. Match on device name.</div>
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
                                                                        <div>dry-run mode. Attach operations are listed but not is pushed to vManage.</div>
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
                    <b>reachable</b>
                    <br/><div style="font-size: small; color: red">bool</div>                                                        </td>
                                <td>
                                                                                                                                                                                                                    <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Select reachable devices only.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>site</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Select devices with site ID.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>system_ip</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Select device with system IP.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>templates</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Regular expression selecting templates to attach. Match on template name.</div>
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


Examples
--------

.. code-block:: yaml+jinja

    
    - name: "Attach vManage configuration"
      cisco.sdwan.attach_vsmart:
        address: "198.18.1.10"
        port: 8443
        user: "admin"
        password:"admin"
        timeout: 300
        workdir: "backup_test_1"
        templates: ".*"
        config_groups: ".*"
        devices: ".*"
        reachable: True
        activate: True
        site: "1"
        system_ip: "12.12.12.12"
        dryrun: False
        batch: 99       
    - name: "Attach vManage configuration with some vManage config arguments saved in environment variables"
      cisco.sdwan.attach_vsmart:
        workdir: "backup_test_2"
        templates: ".*"
        config_groups: ".*"
        devices: ".*"
        reachable: True
        activate: True
        site: "1"
        system_ip: "12.12.12.12"
        dryrun: True
        batch: 99    
    - name: "Attach vManage configuration with all defaults"
      cisco.sdwan.attach_vsmart: 
        address: "198.18.1.10"
        user: admin
        password: admin
