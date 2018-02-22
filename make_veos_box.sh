#!/bin/bash

# Consume the veos vmdk image and the aboot iso from the arista download
# page and create a vagrant-libvirt box that can be configured with Ansible

if ! rpm -q expect; then
  sudo yum install -y expect
fi

sudo rm -rf /tmp/makeveos
mkdir -p /tmp/makeveos

echo "Copying images to /tmp/makeveos"

cp vEOS-lab*.vmdk /tmp/makeveos
cp Aboot-veos* /tmp/makeveos
cp images/veos.xml /tmp/makeveos
cp images/veos.json /tmp/makeveos

cd /tmp/makeveos

VEOS_NAME=$(ls | grep vEOS-lab | cut -d '.' -f 1-3)
ABOOT_NAME=$(ls | grep Aboot-veos)
VEOS_VERSION=$(ls | grep vEOS-lab | cut -d '-' -f 3 | cut -d '.' -f 1-3)

if [ "$VEOS_NAME" == "" ]; then
  echo "No vEOS image found, exiting"
fi
if [ "$ABOOT_NAME" == "" ]; then
  echo "No aboot iso found, exiting"
fi

sed -i "s/VERSION/$VERSION/" veos.json

echo "Grabbing box creation script"

curl -O https://raw.githubusercontent.com/vagrant-libvirt/vagrant-libvirt/master/tools/create_box.sh

echo "Converting vmdk to qcow2"

qemu-img convert -f vmdk -O qcow2 $VEOS_NAME.vmdk veos-box.qcow2

echo "Copying qcow and iso to /var/lib/libvirt/images"

sudo cp -f veos-box.qcow2 /var/lib/libvirt/images
sudo mv -f Aboot-veos* /var/lib/libvirt/images

echo "Defining libvirt domain"

if sudo virsh list --all | grep veos-box; then
  sudo virsh destroy veos-box
fi
sudo virsh undefine veos-box
sudo virsh define veos.xml

echo "Starting domain"

sudo virsh start veos-box

echo "Waiting 90 seconds for box to initialise"
sleep 90

echo "Configuring domain, will pause for a bit after login"

expect -c"
    set timeout 10
    spawn virsh console veos-box
    expect {
    \"Escape character\" {send \"\r\r\" ; exp_continue} 
    \"Escape character\" {send \"\r\r\" ; exp_continue} 
    \"login:\" {send \"admin\r\"; exp_continue}
    }
    expect "localhost\>"
    send \"en\r\r\"
    expect "localhost\#"
    send \"conf t\r\r\"
    expect "localhost\(config\)\#"
    send \"aaa authorization exec default local\r\r\"
    expect "localhost\(config\)\#"
    send \"user vagrant privilege 15 secret vagrant\r\r\"
    expect "localhost\(config\)\#"
    send \"user vagrant shell /bin/sh\r\r\"
    expect "localhost\(config\)\#"
    send \"user vagrant sshkey ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA6NF8iallvQVp22WDkTkyrtvp9eWW6A8YVr+kz4TjGYe7gHzIw+niNltGEFHzD8+v1I2YJ6oXevct1YeS0o9HZyN1Q9qgCgzUFtdOKLv6IedplqoPkcmF0aYet2PkEDo3MlTBckFXPITAMzF8dJSIFo9D8HfdOV0IAdx4O7PtixWKn5y2hMNG0zQPyUecp4pzC6kivAIhyfHilFR61RGL+GPXQ2MWZWFYbAGjyiYJnAmCP3NOTd0jMZEnDkbUvxhMmBYSdETk1rRgm+R4LOzFUGaHqHDLKLX+FIPKcF96hrucXzcWyLbIbEgE98OHlnVYCzRdK8jlqm8tehUc9c9WhQ== vagrant insecure public key\r\r\"
    expect "localhost\(config\)\#"
    send \"!\r\r\"
    expect "localhost\(config\)\#"
    send \"int management1\r\r\"
    expect "localhost\(config-if-Ma1\)\#"
    send \"ip address dhcp\r\r\"
    expect "localhost\(config-if-Ma1\)\#"
    send \"no shutdown\r\r\"
    expect "localhost\(config-if-Ma1\)\#"
    send \"!\r\r\"
    expect "localhost\(config-if-Ma1\)\#"
    send \"end\r\r\"
    expect "localhost\#"
    send \"wr mem\r\r\"
    expect "localhost\#"
    send \"!\r\r\"
    expect "localhost\#"
    send \"exit\r\r\"
"

sudo virsh destroy veos-box
sudo virsh undefine veos-box

sudo bash create_box.sh /var/lib/libvirt/images/veos-box.qcow2

vagrant box add veos.json --name veos
