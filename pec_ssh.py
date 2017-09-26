#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pexpect
import getpass,os
import logging,re
from pexpect import spawn as sp

def ssh_command(command):
    account_name = 'cisco'
    manage_ip = '10.10.1.243'
    """
       This runs a command on the remote host. This could also be done with the
       pxssh class, but this demonstrates what that class does at a simpler level.
       This returns a pexpect.spawn object. This handles the case when you try to
       connect to a new host and ssh asks you if you want to accept the public key
       fingerprint and continue connecting.
       """
    # 为 ssh 命令生成一个 spawn 类的子程序对象.
    child = sp('ssh -l %s %s' % (account_name, manage_ip), maxread=2000)
    ssh_newkey = 'Are you sure you want to continue connecting'
    Password = 'password: '
    loginprompt = '.*?[$#>]'
    i = child.expect([pexpect.TIMEOUT, ssh_newkey, Password,loginprompt])

    # 如果登录超时，打印出错信息，并退出.
    if i == 0:  # Timeout
        print 'TIMEOUT!'
        print 'SSH could not login. Here is what SSH said:'
        print child.before, child.after
        return None

    # 如果 ssh 没有 public key，接受它.
    if i == 1:  # SSH does not have the public key. Just accept it.
        child.sendline('yes')
        p = child.expect([pexpect.TIMEOUT, 'password: '])
        if p == 0:  # Timeout
            print 'TIMEOUT!'
            return None
            print 'SSH could not login. Here is what SSH said:'
            print child.before, child.after
        if p == 1:
            child.sendline('JCFWnantian2014')

    # 输入密码.
    if i == 2:
        child.sendline('JCFWnantian2014')

    else:
        child.sendline(command)
        child.expect('(.*?)[$#>]?')
        return child

if __name__ == '__main__':
    command_a = 'show version'
    command_b = 'show ip interface brief'
    child = ssh_command(command_a)
    #
    print child.before
    print 80*"{}"
    print child.after