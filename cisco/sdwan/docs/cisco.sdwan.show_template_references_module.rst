:source: show_template_references.py

:orphan:

.. _show_template_references_module:


show_template_references - Show template references about device templates on vManage or from a local backup. Display as table or export as csv/json file.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


.. contents::
   :local:
   :depth: 2


Synopsis
--------
- The Show template task can be used to show device templates from a target vManage or a backup directory.
- Criteria can contain regular expression with matching or not matching device or feature template names.




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
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>vManage IP address or can also be defined via VMANAGE_IP environment variable. Either workdir or address/user/password parameter is mandatory</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>exclude</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Exclude table rows matching the regular expression</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>include</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Include table rows matching the regular expression, exclude all other rows</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>password</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>password or can also be defined via VMANAGE_PASSWORD environment variable. Either workdir or address/user/password parameter is mandatory</div>
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
                    <b>save_csv</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Export tables as csv files under the specified directory</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>save_json</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Save teamplate references as json file</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>templates</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Regular expression matching feature template names to include</div>
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
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>username or can also be defined via VMANAGE_USER environment variable. Either workdir or address/user/password parameter is mandatory</div>
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
                                                                        <div>Include only feature-templates with device-template references</div>
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


Examples
--------

.. code-block:: yaml+jinja

    
    - name: Show Template references from local backup directory
      cisco.sdwan.show_template_references:
        save_csv: show_temp_csv
        save_json: show_temp_json
        workdir: backup_198.18.1.10_20210720
        with_refs: True
    - name: Show Template references from vManage
      cisco.sdwan.show_template_references:
        save_csv: show_temp_csv
        with_refs: True
        address: 198.18.1.10
        port: 8443
        user: admin
        password: admin



Return Values
-------------
Common return values are documented :ref:`here <common_return_values>`, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
                    <tr>
                                <td colspan="1">
                    <b>stdout</b>
                    <br/><div style="font-size: small; color: red">str</div>
                                    </td>
                <td>always apart from low level errors</td>
                <td>
                                            <div>Status of Show Template references</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">Show Template references data in string format</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>stdout_lines</b>
                    <br/><div style="font-size: small; color: red">list</div>
                                    </td>
                <td>always apart from low level errors</td>
                <td>
                                            <div>The value of stdout split into a list</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">show table view data</div>
                                    </td>
            </tr>
                        </table>
    <br/><br/>
