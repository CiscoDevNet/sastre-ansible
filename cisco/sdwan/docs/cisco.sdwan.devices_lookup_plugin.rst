:source: devices.py

:orphan:

.. _devices_module:


devices - Fetches list of SD-WAN devices from vManage
+++++++++++++++++++++++++++++++++++++++++++++++++++++


.. contents::
   :local:
   :depth: 2


Synopsis
--------
- This lookup returns list of SD-WAN devices from vManage with multiple filter options.
- When more than one filter condition is defined match is an 'and' of all conditions.
- When no filter is defined all devices are returned.




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
                    <b>_terms</b>
                    <br/><div style="font-size: small; color: red">list</div>                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>base url to connect to SD-WAN vmanage</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>device_type</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Match on device type to include.  Supported values are &#x27;vmanage&#x27;, &#x27;vsmart&#x27;, &#x27;vbond&#x27;, &#x27;vedge&#x27;, &#x27;cedge&#x27;</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>not_regex</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Regular expression matching on the device name to not include.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>reachable</b>
                    <br/><div style="font-size: small; color: red">bool</div>                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>When set to true, only include devices in reachable state.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>regex</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Regular expression matching on the device name to include.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>site</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Include devices matching this site id.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>system_ip</b>
                    <br/><div style="font-size: small; color: red">str</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Include devices matching this system ip.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>timeout_secs</b>
                    <br/><div style="font-size: small; color: red">int</div>                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>REST API timeout value in seconds</div>
                                                                                </td>
            </tr>
                        </table>
    <br/>



Examples
--------

.. code-block:: yaml+jinja

    
        - name: Fetch devices for vedge device type
          ansible.builtin.set_fact:
            device_list: "{{ query('cisco.sdwan.devices', 'https://198.18.1.10:8443', device_type='vedge') }}"
        - name: Fetch all devices
          ansible.builtin.set_fact:
            device_list: "{{ query('cisco.sdwan.devices', 'https://198.18.1.10:8443') }}"





Status
------




Author
~~~~~~

- UNKNOWN


.. hint::
    If you notice any issues in this documentation you can `edit this document <https://github.com/ansible/ansible/edit/devel/lib/ansible/modules/devices.py?description=%3C!---%20Your%20description%20here%20--%3E%0A%0A%2Blabel:%20docsite_pr>`_ to improve it.
