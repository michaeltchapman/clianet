# -*- coding: utf-8 -*-

import logging

from clianet.util import run_ansible

def port_add_vlan(args):
    print "Cumulus: add vlan %d to port %s on host %s" % (args.vlan,
                                                          args.port,
                                                          args.host)
    run_ansible({'port' : args.port, 'vlan' : args.vlan},
                 'cumulus/port_add_vlan.yml', args.host, args.user, private_key=args.private_key)

def port_rm_vlan(args):
    print "Cumulus: add vlan %d to port %s on host %s" % (args.vlan,
                                                          args.port,
                                                          args.host)
    run_ansible({'bridge' : args.bridge},
                 'cumulus/port_add_vlan.yml', args.host, args.user)

def bridge_create(args):
    print "Cumulus: add vlan %d to port %s on host %s" % (args.vlan,
                                                          args.port,
                                                          args.host)
    run_ansible({'port' : args.port, 'vlan' : args.vlan},
                 'cumulus/port_add_vlan.yml', args.host, args.user)

def bridge_destroy(args):
    print "Cumulus: add vlan %d to port %s on host %s" % (args.vlan,
                                                          args.port,
                                                          args.host)
    run_ansible({'port' : args.port, 'vlan' : args.vlan},
                 'cumulus/port_add_vlan.yml', args.host, args.user)

def bridge_add_vlan(args):
    pass

def bridge_rm_vlan(args):
    pass
