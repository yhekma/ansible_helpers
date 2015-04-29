#!/usr/bin/env python

import sys
import os
import ConfigParser
import shlex
self_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(self_dir, '..'))
from ansible_helpers_libs import satellite_helpers


def get_config(conf_file):
    conf_obj = ConfigParser.RawConfigParser()
    conf_obj.read(conf_file)
    return {
        'url': conf_obj.get('main', 'url'),
        'username': conf_obj.get('main', 'username'),
        'password': conf_obj.get('main', 'password'),
        'groups': shlex.split(conf_obj.get('main', 'groups')),
    }


if __name__ == "__main__":
    conf_path = os.getenv('SATELANS_CONFIG')
    config = get_config(conf_path)

    if not config:
        conf_path = os.path.join(self_dir, 'satelans.ini')
        config = get_config(conf_path)

    auth, connection = satellite_helpers.create_connection(
        url=config['url'],
        username=config['username'],
        password=config['password'],
    )

    if sys.argv[1] == '--host':
        print {}
        sys.exit()
    if sys.argv[1] == '--list':
        print satellite_helpers.get_json(connection, auth, config['groups'])
        sys.exit()
