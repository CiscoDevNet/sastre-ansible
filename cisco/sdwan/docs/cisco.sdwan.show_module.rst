:source: show.py

:orphan:

.. _cisco.sdwan.show_module:


cisco.sdwan.show - Run vManage real-time, state or statistics commands; collecting data from one or more devices.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


.. contents::
   :local:
   :depth: 2


Synopsis
--------
- This show module connects to SD-WAN vManage using HTTP REST to retrieve different data.This module contains multiple arguments with connection and filter details to retrieve devices,realtime,state, statistics data.The retrieved data will be displayed to console in table format or can be exported as csv files under the specified directory defined in csv param.When multiple filters are defined, the result is an AND of all filters. A log file is created under a "logs" directory. This "logs" directoryis relative to directory where Ansible runs.




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
                    <b>cmds</b>
                    <br/><div style="font-size: small; color: red">list</div>                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>group of, or specific command to execute. Applicable to only realtime,state,statistics options For realtime , Group options are all, app-route, bfd, control, dpi, interface, omp, software, system, tunnel. Command options are app-route sla-class, app-route stats, bfd sessions, control connections, control local-properties, dpi summary, interface info, omp adv-routes, omp peers, omp summary, software info, system status, tunnel stats. For state , Group options are all, bfd, control, interface, omp, system. Command options are bfd sessions, control connections, control local-properties, interface cedge, interface vedge, omp peers, system info. For statistics , Group options are all, app-route, interface, system. Command options are app-route stats, interface info, system status.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>csv</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Export results as csv files under the specified directory</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>days</b>
                    <br/><div style="font-size: small; color: red">int</div>                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">0</div>
                                    </td>
                                                                <td>
                                                                        <div>Query statistics from &lt;days&gt; ago (default is now). Applicable to only statistics option</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>detail</b>
                    <br/><div style="font-size: small; color: red">bool</div>                                                        </td>
                                <td>
                                                                                                                                                                                                                    <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Detailed output. Applicable to only realtime,state,statistics options</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>hours</b>
                    <br/><div style="font-size: small; color: red">int</div>                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">0</div>
                                    </td>
                                                                <td>
                                                                        <div>Query statistics from &lt;hours&gt; ago (default is now). Applicable to only statistics option</div>
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
                    <b>reachable</b>
                    <br/><div style="font-size: small; color: red">bool</div>                                                        </td>
                                <td>
                                                                                                                                                                                                                    <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Display only reachable devices</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>regex</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Regular expression matching device name, type or model to display</div>
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
                        </table>
    <br/>


Notes
-----

.. note::
    - Tested against 20.4.1.1


Examples
--------

.. code-block:: yaml+jinja

    
    - name: Show Devices data
      cisco.sdwan.show:
        devices:
            regex: ".*"
            reachable: true
            site: "100"
            system_ip: 10.1.0.2
            csv: test
        address: 198.18.1.10
        port: 8443
        user: admin
        password: admin
        timeout: 300
        pid: "2"
        verbose: DEBUG
    - name: Show RealTime data
      cisco.sdwan.show:
        realtime:
            regex: ".*"
            cmds:
                - all
            detail: true
            reachable: true
            site: "100"
            system_ip: 11.0.2.1
            csv: test123
        address: 198.18.1.10
        port: 8443
        user: admin
        password: admin
        timeout: 300
        pid: "2"
        verbose: DEBUG 
    - name: Show State data
      cisco.sdwan.show:
        state:
            regex: ".*"
            cmds:
                - all
            detail: true
            reachable: true
            site: "100"
            system_ip: 11.0.2.1
            csv: test123
        address: 198.18.1.10
        port: 8443
        user: admin
        password: admin
        timeout: 300
        pid: "2"
        verbose: DEBUG 
    - name: Show Statistics data
      cisco.sdwan.show:
        statistics:
            regex: ".*"
            cmds:
                - all
            detail: true
            reachable: true
            site: "100"
            system_ip: 11.0.2.1
            csv: test123
            days: 0
            hours: 0
        address: 198.18.1.10
        port: 8443
        user: admin
        password: admin
        timeout: 300
        pid: "2"
        verbose: DEBUG 





Status
------




Author
~~~~~~

- Satish Kumar Kamavaram (sakamava@cisco.com)


.. hint::
    If you notice any issues in this documentation you can `edit this document <https://github.com/ansible/ansible/edit/devel/lib/ansible/modules/show.py?description=%3C!---%20Your%20description%20here%20--%3E%0A%0A%2Blabel:%20docsite_pr>`_ to improve it.
