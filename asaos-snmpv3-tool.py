#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Avery Rozar'
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

import pexpect
import optparse

PROMPT = ['# ', '>>> ', '>', '\$ ']
SNMPGROUPCMD = ' snmp-server group '
V3PRIVCMD = ' v3 priv '
SNMPSRVUSRCMD = ' snmp-server user '
V3AUTHCMD = ' v3 auth '
PRIVCMD = ' priv '
SNMPSRVHOSTCMD = ' snmp-server host '
VERSION3CMD = ' version 3 '
SHAHMACCMD = ' sha '
SNMPSRVENTRAP = ' snmp-server enable traps all '
WRME = ' write memory '

def send_command(child, cmd):
    child.sendline(cmd)
    child.expect(PROMPT)
    print child.before

def connect(user, host, passwd, en_passwd):
    ssh_newkey = 'Are you sure you want to continue connecting?'
    constr = 'ssh ' + user + '@' + host
    child = pexpect.spawn(constr)
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])

    if ret == 0:
        print '[-] Error Connecting'
        return
    if ret == 1:
        child.sendline('yes')
        ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])
        if ret == 0:
            print '[-] Error Connecting'
            return
    child.sendline(passwd)
    child.expect(PROMPT)
    child.sendline('enable')
    child.sendline(en_passwd)
    child.expect(PROMPT)
    child.sendline('config t')
    child.expect(PROMPT)

    return child

def main():
    parser = optparse.OptionParser('usage %prog ' + '--host --username --password --enable --group --snmp_user --snmp_host --int_name --snmp_v3_auth --snmp_v3_hmac --snmp_v3_priv --snmp_v3_encr')
    parser.add_option('--host', dest='host', type='string', help='specify a target host')
    parser.add_option('--username', dest='user', type='string', help='specify a user name')
    parser.add_option('--password', dest='passwd', type='string', help='specify a passwd')
    parser.add_option('--enable', dest='en_passwd', type='string', help='specify an enable passwd')
    parser.add_option('--group', dest='group', type='string', help='specify an snmp group')
    parser.add_option('--snmp_user', dest='snmpuser', type='string', help='specify an snmp user')
    parser.add_option('--snmp_host', dest='snmphost', type='string', help='specify an snmp server host')
    parser.add_option('--int_name', dest='intname', type='string', help='specify interface name')
    parser.add_option('--snmp_v3_auth', dest='snmpauth', type='string', help='specify the snmp user authentication')
    parser.add_option('--snmp_v3_hmac', dest='snmphmac', type='string', help='set snmp HMAC, md5 or sha')
    parser.add_option('--snmp_v3_priv', dest='snmppriv', type='string', help='specify the snmp priv password')
    parser.add_option('--snmp_v3_encr', dest='snmpencrypt', type='string', help='specify encryption, des, 3des, or aes(128/192/256)')

    (options, args) = parser.parse_args()
    host = options.host
    user = options.user
    passwd = options.passwd
    en_passwd = options.en_passwd
    group = options.group
    snmpuser = options.snmpuser
    snmphost = options.snmphost
    intname = options.intname
    snmpauth = options.snmpauth
    snmppriv = options.snmppriv
    snmpencrypt = options.snmpencrypt

    child = connect(user, host, passwd, en_passwd)
    send_command(child, SNMPGROUPCMD + group + V3PRIVCMD)
    send_command(child, SNMPSRVUSRCMD + snmpuser + ' ' + group + V3AUTHCMD + SHAHMACCMD + snmpauth + PRIVCMD + snmpencrypt + ' ' + snmppriv)
    send_command(child, SNMPSRVHOSTCMD + intname + ' ' + snmphost + VERSION3CMD + snmpuser)
    send_command(child, SNMPSRVENTRAP)
    send_command(child, WRME)

if __name__ == '__main__':
    main()