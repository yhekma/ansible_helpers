#!/usr/bin/env python

import sys
import os
import shlex
from subprocess import Popen, PIPE

try:
    import argparse
except ImportError:
    sys.path.insert(0, '/stage/linuxbeheer/Ansible/ansible_helpers')
    import ansible_helpers_libs.argparse_local as argparse


def generate_local_stream(path):
    dirname = os.path.dirname(path)
    item_name = os.path.basename(path)
    command_string = 'tar --totals -C %s -czf - %s' % (dirname, item_name)
    command = shlex.split(command_string)
    print "Running: %s | " % command_string,
    p_descriptor = Popen(command, stdout=PIPE)
    return p_descriptor


def generate_remote_stream(path_string):
    host, path = path_string.split(':')
    dirname = os.path.dirname(path)
    item_name = os.path.basename(path)
    command_string = "ssh %s 'tar --totals -C %s -czf  - %s'" % (
        host, dirname, item_name,
    )

    command = shlex.split(command_string)
    print "Running: %s | " % command_string,
    p_descriptor = Popen(command, stdout=PIPE)
    return p_descriptor


def write_local_stream(path, stream):
    command_string = 'tar -C %s -xvzf -' % path
    command = shlex.split(command_string)
    print ' '.join(command)
    Popen(command, stdin=stream.stdout).communicate()
    stream.stdout.close()


def write_remote_stream(path_string, stream):
    host, path = path_string.split(':')
    command_string = "ssh %s 'tar -C %s -xvzf -'" % (host, path)
    command = shlex.split(command_string)
    print command_string
    Popen(command, stdin=stream.stdout).communicate()
    stream.stdout.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""Copy files using tar/gzip. Especially worthwhile when rsync is not an option for some reason
        and you are dealing) with a large fileset""",
    )
    parser.add_argument('src', nargs="?",
                        help="The source path in the form of (host:)/path/to/file_or_directory. When a directory is "
                             "given, it is copied recursively")
    parser.add_argument('dest', nargs="?", help="The destination path in the form of (host:)/path/to/dir")
    args = parser.parse_args()
    if ':' in args.src:
        src_stream = generate_remote_stream(args.src)
    else:
        src_stream = generate_local_stream(args.src)

    if ':' in args.dest:
        write_remote_stream(args.dest, src_stream)
    else:
        write_local_stream(args.dest, src_stream)
