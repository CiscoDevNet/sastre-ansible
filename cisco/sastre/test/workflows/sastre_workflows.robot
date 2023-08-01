*** Settings ***
Library     CXTA
Resource    cxta.robot

Library     OperatingSystem
Library     Collections
Library     lib/sastre_ansible.py

Test Setup  Run Keyword  sdwan setup

*** Variables ***
${playbook_base_dir}                                 ${CURDIR}/playbooks

${WorkFlow_01_Folder}                                WorkFlow_01
${WorkFlow_02_Folder}                                WorkFlow_02
${WorkFlow_03_Folder}                                WorkFlow_03
${WorkFlow_04_Folder}                                WorkFlow_04
${WorkFlow_05_Folder}                                WorkFlow_05

${backup_path}                                       ${WorkFlow_01_Folder}/backup
${list_config_csv_before}                            ${WorkFlow_01_Folder}/list_config_before.csv
${list_config_csv_after}                             ${WorkFlow_01_Folder}/list_config_after.csv
${show_template_csv_before}                          ${WorkFlow_01_Folder}/show_template_values_csv_before
${show_template_csv_after}                           ${WorkFlow_01_Folder}/show_template_values_csv_after

${show_template_csv_after_attachment}                show_template_values_csv_after_attachment
${show_template_csv_with_no_attachment}              show_template_values_csv_with_no_attachment
${show_template_csv}                                 show_template_values_csv
${show_template_attach_detach_compare_fail_msg}      show template values detach/attach file mismatch

${template_yml_file_path}                            attach_template_create.yml
${template_yml_file_path_with_no_attachments}        attach_template_create_no_attachments.yml
${template_yml_file_path_after}                      attach_template_create_after_attachment.yml


*** Keywords ***
sdwan setup
    [Arguments]    ${restore_backup_path}=backup
    execute delete task
    execute restore task  restore_backup_path=${restore_backup_path}

execute backup task
    [Arguments]    ${backup_path}=backup
    ${backup_task_output} =  Run  ANSIBLE_STDOUT_CALLBACK=json ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook ${playbook_base_dir}/backup.yml --extra-vars "backup_path=${backup_path}"
    Log  ${backup_task_output}
    ${backup_passed}  Is Playbook Success  backup  ${backup_task_output}

execute delete task
    ${delete_task_output} =  Run  ANSIBLE_STDOUT_CALLBACK=json ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook ${playbook_base_dir}/delete.yml
    Log  ${delete_task_output}
    ${delete_passed}  Is Playbook Success  delete  ${delete_task_output}

execute restore task
    [Arguments]    ${restore_backup_path}=backup
    ${restore_task_output} =  Run  ANSIBLE_STDOUT_CALLBACK=json ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook ${playbook_base_dir}/restore.yml --extra-vars "backup_path=${restore_backup_path}"
    Log  ${restore_task_output}
    ${restore_passed}  Is Playbook Success  restore  ${restore_task_output}

execute show template values task
    [Arguments]    ${show_template_csv_path}=show_template_csv
    ${show_temp_values_task_output} =  Run  ANSIBLE_STDOUT_CALLBACK=json ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook ${playbook_base_dir}/show-template_values.yml --extra-vars "show_template_csv=${show_template_csv_path}"
    Log  ${show_temp_values_task_output}
    ${show_temp_values_passed}  Is Playbook Success  show_template_values  ${show_temp_values_task_output}

execute list configuration task
    [Arguments]    ${list_config_csv_file_path}=list_config.csv
    ${list_config_task_output} =  Run  ANSIBLE_STDOUT_CALLBACK=json ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook ${playbook_base_dir}/list_configuration.yml --extra-vars "list_config_csv=${list_config_csv_file_path}"
    Log  ${list_config_task_output}
    ${list_config_passed}  Is Playbook Success  list_configuration  ${list_config_task_output}

execute detach edge task
    ${detach_edge_task_output} =  Run  ANSIBLE_STDOUT_CALLBACK=json ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook ${playbook_base_dir}/detach_edge.yml
    Log  ${detach_edge_task_output}
    ${detach_edge_passed}  Is Playbook Success  detach_edge  ${detach_edge_task_output}

execute attach edge task
    ${attach_edge_task_output} =  Run  ANSIBLE_STDOUT_CALLBACK=json ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook ${playbook_base_dir}/attach_edge.yml
    Log  ${attach_edge_task_output}
    ${attach_edge_passed}  Is Playbook Success  attach_edge  ${attach_edge_task_output}

execute detach vsmart task
    ${detach_vsmart_task_output} =  Run  ANSIBLE_STDOUT_CALLBACK=json ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook ${playbook_base_dir}/detach_vsmart.yml
    Log  ${detach_vsmart_task_output}
    ${detach_vsmart_passed}  Is Playbook Success  detach_vsmart  ${detach_vsmart_task_output}

execute attach vsmart task
    ${attach_vsmart_task_output} =  Run  ANSIBLE_STDOUT_CALLBACK=json ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook ${playbook_base_dir}/attach_vsmart.yml
    Log  ${attach_vsmart_task_output}
    ${attach_vsmart_passed}  Is Playbook Success  attach_vsmart  ${attach_vsmart_task_output}

execute attach vsmart var task
    [Arguments]    ${template_yml_file_path}=attach_template.yml
    ${attach_vsmart_var_task_output} =  Run  ANSIBLE_STDOUT_CALLBACK=json ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook ${playbook_base_dir}/attach_vsmart_var_file.yml --extra-vars "attach_file=${template_yml_file_path}"
    Log  ${attach_vsmart_var_task_output}
    ${attach_vsmart_var_passed}  Is Playbook Success  attach_vsmart_var  ${attach_vsmart_var_task_output}

execute attach edge var task
    [Arguments]    ${template_yml_file_path}=attach_template.yml
    ${attach_edge_var_task_output} =  Run  ANSIBLE_STDOUT_CALLBACK=json ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook ${playbook_base_dir}/attach_edge_var_file.yml --extra-vars "attach_file=${template_yml_file_path}"
    Log  ${attach_edge_var_task_output}
    ${attach_edge_var_passed}  Is Playbook Success  attach_edge_var  ${attach_edge_var_task_output}

execute attach create task
    [Arguments]    ${template_yml_file_path}=attach_template.yml
    ${attach_create_task_output} =  Run  ANSIBLE_STDOUT_CALLBACK=json ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook ${playbook_base_dir}/attach_create.yml --extra-vars "attach_file=${template_yml_file_path}"
    Log  ${attach_create_task_output}
    ${attach_create_passed}  Is Playbook Success  attach_create  ${attach_create_task_output}

cleanup directory
    [Arguments]    ${directory}
    Remove Directory  ${directory}  recursive=True
    Create Directory  ${directory}

*** Test Cases ***
Workflow_01: Backup_Delete_Restore
    [Documentation]  Executing list_config, show_template_values, backup, delete, restore, list_config, show_template_values  Tasks
    [Tags]  backup_delete_restore

    cleanup directory  directory=${playbook_base_dir}/${WorkFlow_01_Folder}
    execute list configuration task  list_config_csv_file_path=${list_config_csv_before}
    execute show template values task  show_template_csv_path=${show_template_csv_before}
    execute backup task  backup_path=${backup_path}
    sdwan setup  restore_backup_path=${backup_path}
    execute list configuration task  list_config_csv_file_path=${list_config_csv_after}
    execute show template values task  show_template_csv_path=${show_template_csv_after}
    csv folders should be equal  ${playbook_base_dir}/${show_template_csv_before}  ${playbook_base_dir}/${show_template_csv_after}
    csv files should be equal  ${playbook_base_dir}/${list_config_csv_before}  ${playbook_base_dir}/${list_config_csv_after}  0

Workflow_02: Detach_Edge_Attach_Edge
    [Documentation]  Executing show_template_values, detach_edge, show_template_values, attach_edge, show_template_values tasks
    [Tags]  detach_attach

    cleanup directory  directory=${playbook_base_dir}/${WorkFlow_02_Folder}
    execute show template values task  show_template_csv_path=${WorkFlow_02_Folder}/${show_template_csv}
    execute detach edge task
    execute show template values task  show_template_csv_path=${WorkFlow_02_Folder}/${show_template_csv_with_no_attachment}
    compare show template values attach detach  ${playbook_base_dir}/${WorkFlow_02_Folder}/${show_template_csv}  ${playbook_base_dir}/${WorkFlow_02_Folder}/${show_template_csv_with_no_attachment}  true  msg=${show_template_attach_detach_compare_fail_msg}
    execute attach edge task
    execute show template values task  show_template_csv_path=${WorkFlow_02_Folder}/${show_template_csv_after_attachment}
    csv folders should be equal  ${playbook_base_dir}/${WorkFlow_02_Folder}/${show_template_csv}  ${playbook_base_dir}/${WorkFlow_02_Folder}/${show_template_csv_after_attachment}

Workflow_03: Detach_Vsmart_Attach_Vsmart
    [Documentation]  Executing show_template_values, detach_vsmart, show_template_values, attach_vsmart, show_template_values tasks
    [Tags]  detach_attach

    cleanup directory  directory=${playbook_base_dir}/${WorkFlow_03_Folder}
    execute show template values task  show_template_csv_path=${WorkFlow_03_Folder}/${show_template_csv}
    execute detach vsmart task
    execute show template values task  show_template_csv_path=${WorkFlow_03_Folder}/${show_template_csv_with_no_attachment}
    compare show template values attach detach  ${playbook_base_dir}/${WorkFlow_03_Folder}/${show_template_csv}  ${playbook_base_dir}/${WorkFlow_03_Folder}/${show_template_csv_with_no_attachment}  false  msg=${show_template_attach_detach_compare_fail_msg}
    execute attach vsmart task
    execute show template values task  show_template_csv_path=${WorkFlow_03_Folder}/${show_template_csv_after_attachment}
    csv folders should be equal  ${playbook_base_dir}/${WorkFlow_03_Folder}/${show_template_csv}  ${playbook_base_dir}/${WorkFlow_03_Folder}/${show_template_csv_after_attachment}

Workflow_04: Attach_Create_Detach_Edge_Attach_Edge
    [Documentation]  Executing attach_create, show_template_values, detach_edge, attach_create, show_template_values, attach_edge, show_template_values, attach_create tasks
    [Tags]  detach_attach

    cleanup directory  directory=${playbook_base_dir}/${WorkFlow_04_Folder}
    execute attach create task  template_yml_file_path=${WorkFlow_04_Folder}/${template_yml_file_path}
    execute show template values task  show_template_csv_path=${WorkFlow_04_Folder}/${show_template_csv}
    execute detach edge task
    execute attach create task  template_yml_file_path=${WorkFlow_04_Folder}/${template_yml_file_path_with_no_attachments}
    execute show template values task  show_template_csv_path=${WorkFlow_04_Folder}/${show_template_csv_with_no_attachment}
    compare yml files  ${playbook_base_dir}/${WorkFlow_04_Folder}/${template_yml_file_path}  ${playbook_base_dir}/${WorkFlow_04_Folder}/${template_yml_file_path_with_no_attachments}  false
    compare show template values attach detach  ${playbook_base_dir}/${WorkFlow_04_Folder}/${show_template_csv}  ${playbook_base_dir}/${WorkFlow_04_Folder}/${show_template_csv_with_no_attachment}  true  msg=${show_template_attach_detach_compare_fail_msg}
    execute attach edge var task  template_yml_file_path=${WorkFlow_04_Folder}/${template_yml_file_path}
    execute show template values task  show_template_csv_path=${WorkFlow_04_Folder}/${show_template_csv_after_attachment}
    csv folders should be equal  ${playbook_base_dir}/${WorkFlow_04_Folder}/${show_template_csv}  ${playbook_base_dir}/${WorkFlow_04_Folder}/${show_template_csv_after_attachment}
    execute attach create task  template_yml_file_path=${WorkFlow_04_Folder}/${template_yml_file_path_after}
    compare yml files  ${playbook_base_dir}/${WorkFlow_04_Folder}/${template_yml_file_path}  ${playbook_base_dir}/${WorkFlow_04_Folder}/${template_yml_file_path_after}  true

Workflow_05: Attach_Create_Detach_Vsmart_Attach_Vsmart
    [Documentation]  Executing attach_create, show_template_values, detach_vsmart, show_template_values, attach_vsmart, show_template_values, attach_create tasks
    [Tags]  detach_attach
    
    cleanup directory  directory=${playbook_base_dir}/${WorkFlow_05_Folder}
    execute attach create task  template_yml_file_path=${WorkFlow_05_Folder}/${template_yml_file_path}
    execute show template values task  show_template_csv_path=${WorkFlow_05_Folder}/${show_template_csv}
    execute detach vsmart task
    execute attach create task  template_yml_file_path=${WorkFlow_05_Folder}/${template_yml_file_path_with_no_attachments}
    execute show template values task  show_template_csv_path=${WorkFlow_05_Folder}/${show_template_csv_with_no_attachment}
    compare yml files  ${playbook_base_dir}/${WorkFlow_05_Folder}/${template_yml_file_path}  ${playbook_base_dir}/${WorkFlow_05_Folder}/${template_yml_file_path_with_no_attachments}  false
    compare show template values attach detach  ${playbook_base_dir}/${WorkFlow_05_Folder}/${show_template_csv}  ${playbook_base_dir}/${WorkFlow_05_Folder}/${show_template_csv_with_no_attachment}  false  msg=${show_template_attach_detach_compare_fail_msg}
    execute attach vsmart var task  template_yml_file_path=${WorkFlow_05_Folder}/${template_yml_file_path}
    execute show template values task  show_template_csv_path=${WorkFlow_05_Folder}/${show_template_csv_after_attachment}
    csv folders should be equal  ${playbook_base_dir}/${WorkFlow_05_Folder}/${show_template_csv}  ${playbook_base_dir}/${WorkFlow_05_Folder}/${show_template_csv_after_attachment}
    execute attach create task  template_yml_file_path=${WorkFlow_05_Folder}/${template_yml_file_path_after}
    compare yml files  ${playbook_base_dir}/${WorkFlow_05_Folder}/${template_yml_file_path}  ${playbook_base_dir}/${WorkFlow_05_Folder}/${template_yml_file_path_after}  true