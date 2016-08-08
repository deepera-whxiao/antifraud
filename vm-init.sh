#!/bin/bash


if [ -z "$1" ]; then
  echo "ERROR: VM name not specified."
  exit 1
fi
NAME=$1


echo "INFO: Initializing VM $NAME..."

VM_HOME=/home/vagrant

if [ -e "$VM_HOME/local" ]; then
  echo "WARNING: VM $NAME already initialized. Skip."
  exit 0
fi

if [ -e "/vagrant/vm-local-$NAME.tar.gz" ]; then
  cd $VM_HOME && tar zxf /vagrant/vm-local-$NAME.tar.gz
  if ! grep "local/etc/bashrc" $VM_HOME/.bashrc >/dev/null 2>&1; then
    cat >>$VM_HOME/.bashrc <<-EOM
if [ -f \$HOME/local/etc/bashrc ]; then
        . \$HOME/local/etc/bashrc
fi 
EOM
  fi
  echo "INFO: VM $NAME initialized."
else
  echo "WARNING: vm-local-$NAME.tar.gz does not exist. Skip."
fi
