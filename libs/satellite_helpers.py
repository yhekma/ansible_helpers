import re
import xmlrpclib


def getserver():
    with open('/etc/sysconfig/rhn/up2date', 'r') as up2date_handle:
        up2date_config = up2date_handle.read()
        return "%s/rpc/api" % re.match('.*\n\s*serverURL=(.*?)XMLRPC', up2date_config).group(0)


def create_connection(url, username, password, verbose=0):
    server_con = xmlrpclib.ServerProxy(uri=url, verbose=verbose)
    auth = server_con.auth.login(username, password)
    return auth, server_con
