#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
(C) Copyright [2014] InfoSec Consulting, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

         ...
    .:::|#:#|::::.
 .:::::|##|##|::::::.
 .::::|##|:|##|:::::.
  ::::|#|:::|#|:::::
  ::::|#|:::|#|:::::
  ::::|##|:|##|:::::
  ::::.|#|:|#|.:::::
  ::|####|::|####|::
  :|###|:|##|:|###|:
  |###|::|##|::|###|
  |#|::|##||##|::|#|
  |#|:|##|::|##|:|#|
  |#|##|::::::|##|#|
   |#|::::::::::|#|
    ::::::::::::::
      ::::::::::
       ::::::::
        ::::::
          ::
"""
__author__ = 'Avery Rozar'

import pexpect
import getpass
import argparse


def check_creds(host, user, passwd, en_passwd):

    ssh_newkey = 'Are you sure you want to continue connecting (yes/no)?'
    constr = 'ssh ' + user + '@' + host
    ssh = pexpect.spawn(constr)
    ret = ssh.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])
    if ret == 0:
        print '[-] Error Connecting to ' + host
        return
    if ret == 1:
        ssh.sendline('yes')
        ret = ssh.expect([pexpect.TIMEOUT, '[P|p]assword:'])
        if ret == 0:
            print '[-] Could not accept new key from ' + host
            return
    ssh.sendline(passwd)
    auth = ssh.expect(['[P|p]assword:', '.>', '.#'])
    if auth == 0:
        print 'User password is incorrect'
        return
    if auth == 1:
        print('login is correct')
        ssh.sendline('enable')
        ssh.sendline(en_passwd)
        enable = ssh.expect([pexpect.TIMEOUT, '.#'])
        if enable == 0:
            print 'enable password is incorrect'
            return
        if enable == 1:
            print 'enable password is correct'
            return
    if auth == 2:
        print 'privilege mode creds work'
        return
    else:
        print 'creds are incorrect'
        return

def main():
    parser = argparse.ArgumentParser('--host --user --passwd --en_passwd')
    parser.add_argument('--host', dest='host', type=str)
    parser.add_argument('--user', dest='user', type=str)
    parser.add_argument('--passwd', dest='passwd', type=str)
    parser.add_argument('--en_passwd', dest='en_passwd', type=str)

    args = parser.parse_args()
    host = args.host
    user = args.user
    passwd = args.passwd
    en_passwd = args.en_passwd

    if host is None:
        host = raw_input('host: ')
    if user is None:
        user = raw_input('user: ')
    if passwd is None:
        passwd = getpass.getpass('passwd: ')
    if en_passwd is None:
        en_passwd = getpass.getpass('en_passwd: ')
    check_creds(host, user, passwd, en_passwd)

if __name__ == '__main__':
    main()