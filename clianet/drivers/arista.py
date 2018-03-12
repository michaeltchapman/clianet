# -*- coding: utf-8 -*-

import logging

from clianet.util import run_ansible

# connection info for switch
#--extra-vars '{"eos_connection": { "host": "{{ inventory_hostname }}", "username": "eapiuser", "password" : "icanttellyou", "transport": "eapi", "use_ssl" : "false", "validate_certs" : no, "port" : 8081 }}'

def get_eos_connection(args):

    # really this would be loading a config file from somewhere,
    # or populating from inventory args
    return { 'host' : args.host,
             'username' : 'eapiuser',
             'password' : 'icanttellyou',
             'transport' : 'eapi',
             'use_ssl' : 'false',
             'validate_certs' : 'no',
             'port' : 8080 }

def port_add_vlan(args):
    print(": add vlan %d to port %s on host %s" % (args.vlan,
                                                          args.port,
                                                          args.host))
    run_ansible({'port' : args.port, 'vlan' : args.vlan, 'eos_connection' :
                 get_eos_connection(args)},
                 'arista/port_add_vlan.yml', args, True)

def port_rm_vlan(args):
    print("Arista: remove vlan %d from port %s on host %s" % (args.vlan,
                                                          args.port,
                                                          args.host))

def bridge_create(args):
    print("Arista: add bridge %s on host %s" % (args.vlan,
                                                          args.port,
                                                          args.host))

def bridge_destroy(args):
    print("Arista: destroy bridge %s on host %s" % (args.vlan,
                                                          args.port,
                                                          args.host))

def status_version(args):
    run_ansible({'eos_connection' :
                 get_eos_connection(args)},
                 'arista/status_version.yml', args, True)

def bridge_add_vlan(args):
    pass

def bridge_rm_vlan(args):
    pass
