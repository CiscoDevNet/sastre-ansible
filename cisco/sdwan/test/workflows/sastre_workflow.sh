pip install --upgrade git+https://wwwin-github.cisco.com/AIDE/Sastre-Pro.git
cd cisco/sdwan/
value=`cat galaxy.yml`
echo $value | grep -o "version: [0-9]*\.[0-9]*\.[0-9]*" | sed "s/version: //g" > version.txt
version=`cat version.txt`
ansible-galaxy collection build --force
ansible-galaxy collection install cisco-sdwan-$version.tar.gz --force
export VMANAGE_PASSWORD=$VMANAGE_PASSWORD
export VMANAGE_IP=$VMANAGE_IP
export VMANAGE_PORT=$VMANAGE_PORT
export VMANAGE_USER=$VMANAGE_USER
export VMANAGE_PASSWORD=$VMANAGE_PASSWORD
cd ../../
mkdir temp
cd temp
git clone https://wwwin-github.cisco.com/sakamava/Sastre-Ansible.git
cd Sastre-Ansible
git checkout test-data
cp -r data ../../cisco/sdwan/test/workflows/playbooks/
cd ../../
cxta cisco/sdwan/test/workflows/sastre_workflows.robot