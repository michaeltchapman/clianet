# -*- coding: utf-8 -*-

import logging

from clianet.util import run_ansible

def port_add_vlan(args):
    print ": add vlan %d to port %s on host %s" % (args.vlan,
                                                          args.port,
                                                          args.host)
    run_ansible({'port' : args.port, 'vlan' : args.vlan},
                 'arista/port_add_vlan.yml', args)

def port_rm_vlan(args):
    print "Arista: remove vlan %d from port %s on host %s" % (args.vlan,
                                                          args.port,
                                                          args.host)
    run_ansible({'port' : args.port, 'vlan' : args.vlan},
                 'arista/port_rm_vlan.yml', args)

def bridge_create(args):
    print "Arista: add bridge %s on host %s" % (args.vlan,
                                                          args.port,
                                                          args.host)
    run_ansible({'port' : args.port, 'vlan' : args.vlan},
                 'arista/bridge_create.yml', args)

def bridge_destroy(args):
    print "Arista: destroy bridge %s on host %s" % (args.vlan,
                                                          args.port,
                                                          args.host)
    run_ansible({'port' : args.port, 'vlan' : args.vlan},
                 'arista/bridge_destroy.yml', args)

def bridge_add_vlan(args):
    pass

def bridge_rm_vlan(args):
    pass
