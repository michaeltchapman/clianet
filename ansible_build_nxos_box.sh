#!/bin/bash

# First parameter is name of image to build, eg nxos, veos etc.
# Second parameter is optional name of ansible debug log, and will
# turn on -vvvv + logging for the playbook

ROLE_REPO="https://github.com/rcarrillocruz/build-networking-image.git"
#ROLE_REPO="https://github.com/michaeltchapman/build-networking-image.git"

if [ ! -f images/$1.yml ]; then
  echo "Could not find ansible playbook images/$1.yml"
fi
if ! which virtualenv; then
  sudo pip install virtualenv
fi

# Re-use existing venv
if [ ! -d image_build ]; then
  virtualenv image_build
fi

pushd image_build
rm *.box
source bin/activate
pip install git+https://github.com/ansible/ansible.git@devel
pip install pexpect

### hacky python SElinux virtualenv workaround ###

# python selinux library is not in pip, and --use-site-packages is bad 
PYMAJMINVERS=$(python --version | cut -d ' ' -f 2 | cut -d '.' -f 1-2)
PYSTR="python$PYMAJMINVERS"
cp /usr/lib64/$PYSTR/site-packages/_selinux*  ./lib64/$PYSTR/site-packages
cp -r /usr/lib64/$PYSTR/site-packages/selinux ./lib64/$PYSTR/site-packages

##################################################

if [ ! -d build-networking-image ]; then
  git clone $ROLE_REPO
fi

if [ "$2" != "" ]; then
  DBGCMD1="ANSIBLE_LOG_PATH=$2 ANSIBLE_DEBUG=True"
  DBGCMD2="-vvvv"
fi

cp ../images/$1.yml .

ANSIBLE_HOST_KEY_CHECKING=False ANSIBLE_PERSISTENT_CONNECT_TIMEOUT=100 ANSIBLE_PERSISTENT_CONNECT_RETRY_TIMEOUT=60 ANSIBLE_PERSISTENT_COMMAND_TIMEOUT=100 $DBGCMD1 ansible-playbook $1.yml $DBGCMD2

popd
deactivate

# Copy build image out

# Convert image to box

# Leave artifacts only if we're debugging
#if [ "$2" == "" ]; then
#  rm -r image_build
#fi
