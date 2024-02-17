:source: transform_recipe.py

:orphan:

.. _transform_recipe_module:


transform_recipe -- Transform using custom recipe
+++++++++++++++++++++++++++++++++++++++++++++++++


.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The transform recipe task can be used for custom recipe. A regular expression can be used to select item names to transform.




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
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>                    </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>vManage IP address or can also be defined via VMANAGE_IP environment variable</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>from_file</b>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>load custom report specification from YAML file</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>from_json</b>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>load custom report specification from JSON-formatted string</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>no_rollover</b>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                                                                    <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>By default, if output directory already exists it is renamed using a rolling naming scheme. &quot;True&quot; disables the automatic rollover. &quot;False&quot; enables the automatic rollover</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>output</b>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>                    </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Directory to save transform result</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>password</b>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>                    </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>password or can also be defined via VMANAGE_PASSWORD environment variable.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>port</b>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">8443</div>
                                    </td>
                                                                <td>
                                                                        <div>vManage port number or can also be defined via VMANAGE_PORT environment variable</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>tenant</b>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>tenant name, when using provider accounts in multi-tenant deployments.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>timeout</b>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                                            </div>
                                    </td>
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
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>                    </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>username or can also be defined via VMANAGE_USER environment variable.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>workdir</b>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>transform will read from the specified directory instead of target vManage</div>
                                                                                </td>
            </tr>
                        </table>
    <br/>


Notes
-----

.. note::
   - Tested against 20.10



Examples
--------

.. code-block:: yaml+jinja

    
    - name: Transform recipe
      cisco.sastre.transform_recipe:
        output: transform_recipe
        workdir: /home/user/backup
        no_rollover: false
        from_file: recipe.yml
        address: 198.18.1.10
        port: 8443
        user: admin
        password: admin
    - name: Transform recipe
      cisco.sastre.transform_recipe:
        output: transform_recipe
        from_json: recipe.json
        address: 198.18.1.10
        port: 8443
        user: admin
        password: admin