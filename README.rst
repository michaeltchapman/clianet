Clianet
======================

This module is intended to provide a CLI and python interface to perform common
operations on networking equipment, using the ansible-networking modules.

Usage
-----

Add an allowed vlan to a port

    clianet port [port number] add-vlan [vlan-number] [SWITCH_HOST]
    clianet port [port number] rm-vlan [vlan-number] [SWITCH_HOST]

(EOS) Run a playbook that prints the version of the switch:

   vagrant up arista
   ARISTA_IP=$(./populate_inventory.sh | grep arista | cut -f '2' -d ':')
   clianet --debug --user vagrant -p ~/.vagrant.d/insecure_private_key $ARISTA_IP arista status version 

License
-------

Uses the `MIT`_ license.


.. _MIT: http://opensource.org/licenses/MIT
