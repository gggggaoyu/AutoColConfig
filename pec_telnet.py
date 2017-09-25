#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pexpect
from pexpect import spawn as sp


def telnet_command_test(command):
    # 即将 telnet 所要登录的远程主机的域名
    ipAddress = '10.10.1.187 32790'
    # 登录用户名
    loginName = 'admin'
    # 用户名密码
    loginPassword = 'admin'
    # 提示符，可能是’ $ ’ , ‘ # ’或’ > ’
    loginprompt = '[$#>]'

    telnet_newkey = 'Are you sure you want to continue connecting ? (yes/no)'
    # 拼凑 telnet 命令
    cmd = 'telnet ' + ipAddress
    # 为 telnet 生成 spawn 类子程序
    child = sp(cmd)
    #print child.before

    index = child.expect(["telnet_newkey","(?i)login:","()", pexpect.EOF, pexpect.TIMEOUT])
    print index
    print child.before
    print child.after
    print "test1"
    child.expect('.*?')
    child.sendline('admin')
    child.expect('admin')
    child.expect('(?i)password:')
    child.sendline('admin')
    child.expect('.*?')
    print "test2"
    child.sendline('show version | no-more')
    child.expect('show version')
    child.expect('| no-more')
    child.expect('(.*?)#')
    # child.sendline('\n')
    # child.expect('(?!)--More--')
    # child.sendline('\n')
    # child.expect('(?!)--More--')
    text = child.before
    print child.before
    print child.after
    #print "test3"
    text = child.before

    child.close(force = True)
    return text

def telnet_command(command):
    # 即将 telnet 所要登录的远程主机的域名
    ipAddress = '10.10.1.187 32790'
    # 登录用户名
    loginName = 'admin'
    # 用户名密码
    loginPassword = 'admin'
    # 提示符，可能是’ $ ’ , ‘ # ’或’ > ’
    loginprompt = '[$#>]'

    telnet_newkey = 'Are you sure you want to continue connecting ? (yes/no)'
    # 拼凑 telnet 命令
    cmd = 'telnet ' + ipAddress
    # 为 telnet 生成 spawn 类子程序
    child = sp(cmd)
    index = child.expect(["telnet_newkey","(?i)login:","()", pexpect.EOF, pexpect.TIMEOUT])
    child.expect('.*?')
    child.sendline('admin')
    child.expect('admin')
    child.expect('(?i)password:')
    child.sendline('admin')
    child.expect('.*?')
    print "正在输入命令"
    child.sendline(command + ' | xml | no-more')
    child.expect(command + ' | xml | no-more')
    child.expect('(.*?)#')

    text_before = child.before
    text_after = child.after
    #print text_after#这个打印不能去掉不知道为什么
    child.close(force = True)
    return text_after

if __name__ == '__main__':
    command_a = 'show version'
    command_b = 'show ip interface brief'
    child = telnet_command(command_b)
    print child
