# -*- coding: utf-8 -*-

import argparse
import logging
import os
import sys

def main():
    main_parser = create_parsers()
    args = main_parser.parse_args(sys.argv[1:])

    formatter = '%(asctime)s %(levelname)s: %(message)s'
    logging.basicConfig(filename="clianet.log",
        format=formatter,
        datefmt='%m/%d/%Y %I:%M:%S %p',
        level=logging.DEBUG)

    use_driver(args)

def create_parsers():
    main_parser = argparse.ArgumentParser()
    main_parser.add_argument('host', help='host to operate on')
    main_parser.add_argument('--user',default='root',help='user to connect as')
    main_parser.add_argument('-p', '--private-key',default=None,help='private key for ansible connection')
    main_parser.add_argument('-i', '--inventory',default=None,help='inventory for ansible connection')
    main_parser.add_argument('driver', help='vendor driver to use')
    subparsers = main_parser.add_subparsers(help='sub-command help')
    create_port_parser(subparsers)
    create_bridge_parser(subparsers)
    return main_parser

def create_port_parser(subparsers):
    port_parser = subparsers.add_parser('port', help='port help')
    port_parser.add_argument('port', help='port to operate on')
    port_subparsers = port_parser.add_subparsers()

    add_vlan = port_subparsers.add_parser('add_vlan', help='add vlan to port')
    add_vlan.add_argument('vlan', type=int, help='vlan to add')
    add_vlan.set_defaults(func='port_add_vlan')

    rm_vlan = port_subparsers.add_parser('remove_vlan',
                                         help='remove vlan from port')
    rm_vlan.add_argument('vlan', type=int, help='vlan to add')
    rm_vlan.set_defaults(func='port_rm_vlan')

def create_bridge_parser(subparsers):
    bridge_parser = subparsers.add_parser('bridge', help='bridge help')
    bridge_parser.add_argument('bridge', help='bridge to operate on')
    bridge_subparsers = bridge_parser.add_subparsers()

    create = bridge_subparsers.add_parser('create', help='create a bridge')
    create.set_defaults(func='bridge_create')

    destroy = bridge_subparsers.add_parser('destroy', help='destroy a bridge')
    destroy.set_defaults(func='bridge_destroy')

    add_port = bridge_subparsers.add_parser('add_port',
                                            help='add port to bridge')
    add_port.set_defaults(func='bridge_add_port')
    rm_port = bridge_subparsers.add_parser('remove_port',
                                           help='remove port from bridge')
    rm_port.set_defaults(func='bridge_rm_port')

def use_driver(args):
    # Maybe not good...
    module = __import__('clianet.drivers.'+args.driver, globals(), locals(), [args.driver], -1)
    func = getattr(module, args.func)
    func(args)
