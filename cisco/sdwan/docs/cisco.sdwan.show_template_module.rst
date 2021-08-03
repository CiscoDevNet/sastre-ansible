:source: show_template.py

:orphan:

.. _cisco.sdwan.show_template_module:


cisco.sdwan.show_template - Show details about device templates on vManage or from a local backup. Display as table or export as csv file.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


.. contents::
   :local:
   :depth: 2


Synopsis
--------
- The Show template task can be used to show device templates from a target vManage, or a backup directory. Criteria can contain regular expression with matching device or feature template names depending on type of option specified. A log file is created under a "logs" directory. This "logs" directoryis relative to directory where Ansible runs.




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
                    <b>csv</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Export tables as csv files under the specified directory</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>id</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Device template id For values option, this param is applicable.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>name</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Device template name For values option, this param is applicable.</div>
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
                                                                        <div>For values option, regular expression matching device template names. For references option, regular expression matching feature template names to include.</div>
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
                    <b>with_refs</b>
                    <br/><div style="font-size: small; color: red">bool</div>                                                        </td>
                                <td>
                                                                                                                                                                                                                    <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Include only feature-templates with device-template references For references option, this param is applicable.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>workdir</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>show-template will read from the specified directory instead of target vManage. Either workdir or vManage address/user/password is mandatory</div>
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

    
    - name: Show Template values from local backup directory
      cisco.sdwan.show_template:
        values: 
            regex: ".*"
            workdir: backup_198.18.1.10_20210720
            csv: show_temp
            name: DC-vEdges
            id: 704bbc2f-aa9a-4068-84a2-fc31602ed553
        verbose: DEBUG
        pid: "2"
    - name: Show Template values from vManage
      cisco.sdwan.show_template:
        values: 
            regex: ".*"
            csv: show_temp
            name: DC-vEdges
            id: 704bbc2f-aa9a-4068-84a2-fc31602ed553
        address: 198.18.1.10
        port: 8443
        user: admin
        password: admin
        verbose: DEBUG
        pid: "2"
        timeout: 300
    - name: Show Template references from local backup directory
      cisco.sdwan.show_template:
        references: 
            regex: ".*"
            csv: show_temp
            workdir: backup_198.18.1.10_20210720
            with_refs: True
        verbose: DEBUG
        pid: "2"
    - name: Show Template references from vManage
      cisco.sdwan.show_template:
        references: 
            regex: ".*"
            csv: show_temp
            with_refs: True
        address: 198.18.1.10
        port: 8443
        user: admin
        password: admin
        verbose: DEBUG
        pid: "2"
        timeout: 300





Status
------




Author
~~~~~~

- Satish Kumar Kamavaram (sakamava@cisco.com)


.. hint::
    If you notice any issues in this documentation you can `edit this document <https://github.com/ansible/ansible/edit/devel/lib/ansible/modules/show_template.py?description=%3C!---%20Your%20description%20here%20--%3E%0A%0A%2Blabel:%20docsite_pr>`_ to improve it.
