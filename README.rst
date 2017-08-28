Clianet
======================

This module is intended to provide a CLI interface to perform common
operations on networking equipment, using the ansible-networking modules.

Usage
-----

Add an allowed vlan to a port

    clianet port [port number] add-vlan [vlan-number] [SWITCH_HOST]
    clianet port [port number] rm-vlan [vlan-number] [SWITCH_HOST]

License
-------

Uses the `MIT`_ license.


.. _MIT: http://opensource.org/licenses/MIT
