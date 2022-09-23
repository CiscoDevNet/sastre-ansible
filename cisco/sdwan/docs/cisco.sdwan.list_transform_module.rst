:source: list_transform.py

:orphan:

.. _list_transform_module:


list_transform - List configuration items or device certificate information from vManage or a local backup. Display as table or export as csv file.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


.. contents::
   :local:
   :depth: 2


Synopsis
--------
- The list task can be used to show items from a target vManage, or a backup directory. Matching criteria can contain item tag(s) and regular expression.When multiple filters are defined, the result is an AND of all filters.A log file is created under a "logs" directory. This "logs" directoryis relative to directory where Ansible runs.




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
                    <b>name_regex</b>
                    <br/><div style="font-size: small; color: red">str</div>                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>name-regex used to transform an existing item name. Variable {name} is replaced with the original template name. Sections of the original template name can be selected using the {name &lt;regex&gt;} format. Where  is a regular expression that must contain at least one capturing group. Capturing groups identify sections of the original name to keep. For transform option, this param is mandatory.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>not_regex</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Regular expression selecting items NOT to list, match on original item names.</div>
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
                                                                        <div>Regular expression selecting items to list, match on original item names.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>save_csv</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Export table as a csv file</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>save_json</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Export table as a json file</div>
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
                                                                        <div>Defines one or more tags for selecting groups of items. Multiple tags should be configured as list. Available tags are template_feature, policy_profile, policy_definition, all, policy_list, policy_vedge, policy_voice, policy_vsmart, template_device, policy_security, policy_customapp. Special tag &quot;all&quot; selects all items, including WAN edge certificates and device configurations.</div>
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
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>list will read from the specified directory instead of target vManage. Either workdir or vManage address/user/password is mandatory</div>
                                                                                </td>
            </tr>
                        </table>
    <br/>


Examples
--------

.. code-block:: yaml+jinja

    
    - name: List Configuration
      cisco.sdwan.list_transform:
        tags:
            - template_feature
            - policy_vedge
        regex: ".*"
        include: ".*"
        workdir: backup_198.18.1.10_20210720 
        name_regex: '{name}'
        save_csv: list_config_csv
        save_json: list_config_json
    - name: List Configuration
      cisco.sdwan.list_transform:
        tags:
            - template_feature
            - policy_vedge
        not_regex: ".*"
        include: ".*"
        exclude: ".*"
        save_csv: list_config_csv
        save_json: list_config_json
        name_regex: '{name}'
        address: 198.18.1.10
        port: 8443
        user: admin
        password: admin
        timeout: 300




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
                                            <div>Status of list</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">Task List: configuration completed successfully.vManage address 198.18.1.10</div>
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
