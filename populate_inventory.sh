#!/bin/bash

# This script will build the ansible inventory based on the current
# running vagrant machines

# TODO move to yaml and add connection info for things like eos

if [ -f tmp.inventory ]; then
  rm tmp.inventory
fi
VAGRANTOUT=$(vagrant status | grep running | cut -f 1 -d ' ')

for vswitch in $VAGRANTOUT; do
  echo "[$vswitch]" >> tmp.inventory
  vswitch_ip="$(vagrant ssh-config $vswitch | grep HostName | cut -f 4 -d ' ')"
  echo $vswitch_ip >> tmp.inventory
  echo "$vswitch : $vswitch_ip"
done



