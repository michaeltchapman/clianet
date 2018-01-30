#!/bin/bash

# This script will build the ansible inventory based on the current
# running vagrant machines

if [ -f tmp.inventory ]; then
  rm tmp.inventory
fi
VAGRANTOUT=$(vagrant status | grep running | cut -f 1 -d ' ')

for vswitch in $VAGRANTOUT; do
  echo "[$vswitch]" >> tmp.inventory
  echo "$(vagrant ssh-config $vswitch | grep HostName | cut -f 4 -d ' ')" >> tmp.inventory
done



