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

from prompts import *
import pexpect

def config_mode(user, host, passwd, en_passwd):
    ssh_newkey = 'Are you sure you want to continue connecting (yes/no)?'
    constr = 'ssh ' + user + '@' + host
    child = pexpect.spawn(constr)
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, 'Permission denied, please try again.', '[P|p]assword:'])

    if ret == 0:
        print '[-] Error Connecting to ' + host
        return
    if ret == 1:
        child.sendline('yes')
        ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])
        if ret == 0:
            print '[-] Could not accept new key from ' + host
            return
    child.sendline(passwd)
    child.expect(PROMPT)
    child.sendline('enable')
    child.sendline(en_passwd)
    child.expect(PROMPT)
    child.sendline('config t')
    child.expect(PROMPT)
    return child