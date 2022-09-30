pip install --upgrade git+https://github.com/CiscoDevNet/sastre.git
cd cisco/sastre/
value=`cat galaxy.yml`
echo $value | grep -o "version: [0-9]*\.[0-9]*\.[0-9]*" | sed "s/version: //g" > version.txt
version=`cat version.txt`
ansible-galaxy collection build --force
ansible-galaxy collection install cisco-sastre-$version.tar.gz --force
export VMANAGE_IP=$VMANAGE_IP
export VMANAGE_PORT=$VMANAGE_PORT
export VMANAGE_USER=$VMANAGE_USER
export VMANAGE_PASSWORD=$VMANAGE_PASSWORD
cd ../../
mkdir temp
cd temp
git clone https://wwwin-github.cisco.com/AIDE/Sastre-Ansible.git
cd Sastre-Ansible
git checkout test-data
cp -r data ../../cisco/sastre/test/workflows/playbooks/
cd ../../
cxta cisco/sastre/test/workflows/sastre_workflows.robot