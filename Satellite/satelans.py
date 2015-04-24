#!/usr/bin/env python

import sys
import os
import ConfigParser
import json
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


def get_json_list(sat_connection, sat_auth, groups):
    result = {'_meta': {'hostvars': dict()}}

    for group in groups:
        hosts = [i['name'] for i in
                 sat_connection.systemgroup.listSystemsMinimal(sat_auth, group)]
        result[group] = {
            'hosts': hosts,
        }

        for host in hosts:
            result['_meta']['hostvars'][host] = {}
    return json.dumps(result)


if __name__ == "__main__":
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
        print get_json_list(connection, auth, config['groups'])
        sys.exit()
