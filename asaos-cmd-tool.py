#!/usr/bin/python
# -*- coding: utf-8 -*-
#             ...
#        .:::|#:#|::::.
#     .:::::|##|##|::::::.
#     .::::|##|:|##|:::::.
#      ::::|#|:::|#|:::::
#      ::::|#|:::|#|:::::
#      ::::|##|:|##|:::::
#      ::::.|#|:|#|.:::::
#      ::|####|::|####|::
#      :|###|:|##|:|###|:
#      |###|::|##|::|###|
#      |#|::|##||##|::|#|
#      |#|:|##|::|##|:|#|
#      |#|##|::::::|##|#|
#       |#|::::::::::|#|
#        ::::::::::::::
#          ::::::::::
#           ::::::::
#            ::::::
#              ::
__author__ = 'Avery Rozar'

from modules.enable_mode import *
from modules.send_cmd import *
import optparse

def main():
    parser = optparse.OptionParser('usage %prog ' + '-H <host> -u <user> -p <passwd> -e <en_passwd> -c <command>')
    parser.add_option('-H', dest='host', type='string', help='specify a target host')
    parser.add_option('-u', dest='user', type='string', help='specify a user name')
    parser.add_option('-p', dest='passwd', type='string', help='specify a passwd')
    parser.add_option('-e', dest='en_passwd', type='string', help='specify an enable passwd')
    parser.add_option('-c', dest='cmd', type='string', help='specify a command')

    (options, args) = parser.parse_args()
    host = options.host
    user = options.user
    passwd = options.passwd
    en_passwd = options.en_passwd
    cmd = options.cmd

    if host is None or passwd is None or user is None or en_passwd is None or cmd is None:
        print parser.usage
        exit(0)

    child = enable_mode(user, host, passwd, en_passwd)
    send_command(child, cmd)

if __name__ == '__main__':
    main()