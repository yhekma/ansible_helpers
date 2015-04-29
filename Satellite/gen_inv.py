#!/usr/bin/env python

import sys
import os
import json
self_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(self_dir, '..'))
from ansible_helpers_libs.satellite_helpers import get_json, get_config, create_connection
try:
    import argparse
except ImportError:
    import ansible_helpers_libs.argparse_local as argparse


def main(c_auth, conn, group, section):
    hosts_dict = json.loads(get_json(conn, c_auth, [group]))
    hosts = hosts_dict['hosts']
    print '[%s]\n%s' % (section, '\n'.join(hosts))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
                        help='Location of the config file, defaults to global variable SATELANS_CONFIG.',
                        default=os.getenv('SATELANS_CONFIG'))
    parser.add_argument('-g', '--group', help='Which Satellite group to query.')
    parser.add_argument('-s', '--section', help='Name of the Ansible section to generate, defaults to groupname.')
    args = parser.parse_args()

    config = get_config(args.config)
    auth, connection = create_connection(
        url=config['url'],
        username=config['username'],
        password=config['password'],
    )


