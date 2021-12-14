# Cisco SDWAN workflows automation

Cisco SDWAN Test Workflows will automate and test some of the Sastre-Ansible module tasks end to end. 

These workflows will leverage [CXTA framework](https://wwwin-github.cisco.com/AS-Community/CXTA) for building and running workflows


## CXTA version compatibility

These workflows are tested against following CXTA versions: **==21.9**.


## Running the workflows

* Launch [CXTA docker container](https://engci-maven.cisco.com/artifactory/list/cxta-docker/cxta/21.9/)
* Copy "workflows" folder inside docker container
* Run docker (ex : docker run -it dockerhub.cisco.com/cxta-docker/cxta:21.9 bash)
* Run cisco sdwan workflow 
  * cd to "workflows" folder
  * cxta sastre_workflows.robot  
* Check "report.html" for test report statistics
* Check "log.html" for test logs  

## Dependency

* Install [Sastre-Pro](https://wwwin-github.cisco.com/AIDE/Sastre-Pro) using pip
* Install [Sastre-Ansible](https://wwwin-github.cisco.com/AIDE/Sastre-Ansible) refer [ReadMe](https://wwwin-github.cisco.com/AIDE/Sastre-Ansible/blob/master/README.md) for build and installation