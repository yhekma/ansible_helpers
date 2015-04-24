#!/usr/bin/env python

import sys
import os
import ConfigParser
import json
import shlex
from libs import sat_helpers


def get_config(conf_file):
    conf_obj = ConfigParser.RawConfigParser()
    conf_obj.read(conf_file)
    return {
        'url': conf_obj.get('main', 'url'),
        'username': conf_obj.get('main', 'username'),
        'password': conf_obj.get('main', 'password'),
        'groups': shlex.split(conf_obj.get('main', 'groups')),
    }


def dump_json_list(sat_connection, groups):
    result = {'_meta': {'hostvars': dict()}}

    for group in groups:
        hosts = [i['name'] for i in
                 sat_connection.satServer.systemgroup.listSystemsMinimal(sat_connection.satAuth, group)]
        result[group] = {
            'hosts': hosts,
        }

        for host in hosts:
            result['_meta']['hostvars'][host] = {}
    print json.dumps(result)


if __name__ == "__main__":
    self_dir = os.path.dirname(os.path.abspath(__file__))
    config = get_config("%s/satelans.ini" % self_dir)
    connection = sat_helpers.create_connection(
        url=config['url'],
        username=config['username'],
        password=config['password'],
    )

    if sys.argv[1] == '--host':
        print {}
        sys.exit()
    if sys.argv[1] == '--list':
        dump_json_list(connection, config['groups'])
        sys.exit()
