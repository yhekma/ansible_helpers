#!/usr/bin/env python

import sys
import os
self_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(self_dir, '..'))
from ansible_helpers_libs import satellite_helpers


if __name__ == "__main__":
    config = satellite_helpers.get_config()

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
