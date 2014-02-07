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

import pxssh
import getpass
import argparse
from prompts import *

def passwd_chk(host, user, password, en_passwd):
    global success
    global failure

    try:
        ssh = pxssh.pxssh()
        ssh.login(host, user, password, en_passwd)
        ssh.prompt()
        success = True
        print 'Credentials work'
        ssh.logout()
    except pxssh.ExceptionPxssh, fail:
        print str(fail)
        failure = True
        exit(0)


def main():
    parser = argparse.ArgumentParser('--host --username --password --enable')
    parser.add_argument('--host', dest='host', type=str)
    parser.add_argument('--username', dest='user', type=str)
    parser.add_argument('--password', dest='password', type=str)
    parser.add_argument('--enable', dest='en_passwd', type=str)

    args = parser.parse_args()
    host = args.host
    username = args.user
    password = args.password
    enable = args.en_passwd

    if host is None:
        host = raw_input('hostname: ')
    if username is None:
        user = raw_input('username: ')
    if password is None:
        password = getpass.getpass('password: ')
    if enable is None:
        en_passwd = getpass.getpass('enable passwd: ')
    passwd_chk(host, user, password, en_passwd)

if __name__ == '__main__':
    main()