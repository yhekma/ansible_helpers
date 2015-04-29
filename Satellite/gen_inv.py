#!/usr/bin/env python

import sys
import os
import json
import xmlrpclib
self_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(self_dir, '..'))
from ansible_helpers_libs.satellite_helpers import get_json, get_config, create_connection
try:
    import argparse
except ImportError:
    import ansible_helpers_libs.argparse_local as argparse


parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config',
                    help='Location of the config file, defaults to global variable SATELANS_CONFIG.',
                    default=os.getenv('SATELANS_CONFIG'))
parser.add_argument('-g', '--group', help='Which Satellite group(s) to query. Multiples can be comma-seperated.')
parser.add_argument('-s', '--section', help='Name of the Ansible section to generate.')
args = parser.parse_args()
groups = args.group(',')

config = get_config(args.config)
auth, connection = create_connection(
    url=config['url'],
    username=config['username'],
    password=config['password'],
)

print '[%s]' % args.section
for group in groups:
    try:
        hosts_dict = json.loads(get_json(connection, auth, group))
        hosts = hosts_dict[group]['hosts']
        print '%s' % ('\n'.join(hosts))
    except xmlrpclib.Fault:
        pass
