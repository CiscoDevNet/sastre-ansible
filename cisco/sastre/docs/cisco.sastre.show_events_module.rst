:source: show_events.py

:orphan:

.. _show_events_module:


show_events -- Display vManage events.
++++++++++++++++++++++++++++++++++++++


.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This show events module connects to SD-WAN vManage using HTTP REST to retrieve and display vManage events.This module contains multiple arguments with connection and filter details to retrieve data. The retrieved data will be displayed to console in table format or can be exported as csv/json files. When multiple filters are defined, the result is an AND of all filters.




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
                    <b>days</b>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">0</div>
                                    </td>
                                                                <td>
                                                                        <div>Retrieve records since &lt;days&gt; ago (default is now)</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>detail</b>
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
                                                                        <div>Detailed output (i.e. more columns)</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>exclude</b>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Exclude table rows matching the regular expression</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>hours</b>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">1</div>
                                    </td>
                                                                <td>
                                                                        <div>Retrieve records since &lt;hours&gt; ago (default is now)</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>include</b>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Include table rows matching the regular expression, exclude all other rows</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>max</b>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">100</div>
                                    </td>
                                                                <td>
                                                                        <div>Maximum number of records to retrieve (default is now)</div>
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
                    <b>save_csv</b>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Export results as CSV files under the specified directory</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>save_json</b>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Export results as JSON-formatted file</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>simple</b>
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
                                                                        <div>Simple output (i.e. less columns)</div>
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
                        </table>
    <br/>


Notes
-----

.. note::
   - Tested against 20.4.1.1



Examples
--------

.. code-block:: yaml+jinja

    
    - name: Show events data
      cisco.sastre.show_events:
        include: ".*"
        max: 1
        days: 1
        hours: 1
        detail: true
        save_csv: show_events_csv
        save_json: show_events_json
        address: 198.18.1.10
        port: 8443
        user: admin
        password: admin
    - name: Show events data
      cisco.sastre.show_events:
        address: 198.18.1.10
        port: 8443
        user: admin
        password: admin