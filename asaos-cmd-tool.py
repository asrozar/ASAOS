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
import getpass
import argparse

def main():
    parser = argparse.ArgumentParser('usage %prog ' + '--host --user --password --enable --cmd')
    parser.add_argument('--host', dest='host', type='string', help='specify a target host')
    parser.add_argument('--host_file', dest='hosts', type=file, help='specify a target host file')
    parser.add_argument('-user', dest='user', type='string', help='specify a user name')
    parser.add_argument('--password', dest='passwd', type='string', help='specify a passwd')
    parser.add_argument('--enable', dest='en_passwd', type='string', help='specify an enable passwd')
    parser.add_argument('--cmd', dest='cmd', type='string', help='specify a command')

    args = parser.parse_args()
    host = args.host
    hosts = args.hosts
    user = args.user
    passwd = args.passwd
    en_passwd = args.en_passwd
    cmd = args.cmd

    if host is None and hosts is None:
        print('I need to know what host[s] to connect to')
        print parser.usage
        exit(0)

    if user is None:
        user = raw_input('Enter your username: ')

    if passwd is None:
        passwd = getpass.getpass(prompt='User Password: ')

    if en_passwd is None:
        en_passwd = getpass.getpass(prompt='Enable Secret: ')

    if cmd is None:
        cmd = raw_input('Enter your SNMP group: ')

    if hosts:
        for line in hosts:
            host = line.rstrip()
            child = enable_mode(user, host, passwd, en_passwd)
            if child:
                send_command(child, cmd)
    elif host:
        child = enable_mode(user, host, passwd, en_passwd)
        send_command(child, cmd)

if __name__ == '__main__':
    main()