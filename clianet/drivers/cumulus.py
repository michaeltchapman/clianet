# -*- coding: utf-8 -*-

import logging

from clianet.util import run_ansible

def port_add_vlan(args):
    print "Cumulus: add vlan %d to port %s on host %s" % (args.vlan,
                                                          args.port,
                                                          args.host)
    run_ansible({'port' : args.port, 'vlan' : args.vlan},
                 'cumulus/port_add_vlan.yml', args)

def port_rm_vlan(args):
    print "Cumulus: remove vlan %d from port %s on host %s" % (args.vlan,
                                                          args.port,
                                                          args.host)
    run_ansible({'port' : args.port, 'vlan' : args.vlan},
                 'cumulus/port_rm_vlan.yml', args)

def bridge_create(args):
    print "Cumulus: create bridge %s on host %s" % (args.bridge,
                                                          args.port,
                                                          args.host)
    run_ansible({'bridge':  args.bridge},
                 'cumulus/bridge_create.yml', args)

def bridge_destroy(args):
    print "Cumulus: destroy bridge %s on host %s" % (args.bridge,
                                                          args.port,
                                                          args.host)
    run_ansible({'bridge':  args.bridge},
                 'cumulus/bridge_destroy.yml', args)

def bridge_add_vlan(args):
    pass

def bridge_rm_vlan(args):
    pass
