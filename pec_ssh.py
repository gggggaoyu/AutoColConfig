#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pexpect
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
    ssh_newkey = 'Are you sure you want to continue connecting ?'
    Password = 'Password: '
    loginprompt = '.*?[$#>]'
    index = child.expect([loginprompt,Password,ssh_newkey,pexpect.EOF,pexpect.TIMEOUT])

    # 直接就登陆了,执行命令.
    if index == 0:
        print "many login so direct exec command!"
        child.sendline(command)
        # DesiredContent = command
        # i = child.expect([DesiredContent,pexpect.EOF,pexpect.TIMEOUT])
        # if i != 0:
        #     print "match content failed!"
        #     child.close(force=True)
        return child

    # 输入密码.
    elif index == 1:
        child.sendline('JCFWnantian2014')  # 如果登录超时，打印出错信息，并退出.
        i = child.expect([loginprompt, pexpect.EOF, pexpect.TIMEOUT])
        if i != 0:
            print "ssh login failed ,password is worng!"
            child.close(force=True)

        child.sendline(command)
        DesiredContent = 'cisco.*'
        i = child.expect([DesiredContent, pexpect.EOF, pexpect.TIMEOUT])
        if i != 0:
            print "match content failed!"
            child.close(force=True)
        return child

    # 如果 ssh 没有 public key，接受它.
    elif index == 2:  # SSH does not have the public key. Just accept it.
        child.sendline('yes')
        i = child.expect([Password, pexpect.EOF, pexpect.TIMEOUT])
        if i!= 0:
            print "ssh login failed , can't match Password!"
            child.close(force=True)

        child.sendline('JCFWnantian2014')  # 如果登录超时，打印出错信息，并退出.
        i = child.expect([loginprompt, pexpect.EOF, pexpect.TIMEOUT])
        if i != 0:
            print "ssh login failed ,password is worng!"
            child.close(force=True)

        child.sendline(command)
        DesiredContent = 'cisco.*'
        i = child.expect([DesiredContent, pexpect.EOF, pexpect.TIMEOUT])
        if i != 0:
            print "match content failed!"
            child.close(force=True)
        return child


    elif index == 3:
        print 'pexpect.EOF！'
        print 'SSH could not login. Here is what SSH said:`'
        return child

    else:# Timeout
        print 'TIMEOUT!'
        print 'SSH could not login. Here is what SSH said:`'
        return child

        # child.expect('.*[$#>]?')
        # child.sendline(command +'| no-more')
        # child.expect('.*[$#>]?' + command)
        # child.expect('.*?')

if __name__ == '__main__':
    command_a = 'show version'
    command_b = 'show ip interface brief'
    command_c = ''
    child = ssh_command(command_a)
    print child.before
    print 80*"{}"
    print child.after

"""
当 expect() 过程匹配到关键字（或者说正则表达式）之后，系统会自动给3个变量赋值，分别是 before, after 和 match

process.before - 保存了到匹配到关键字为止，缓存里面已有的所有数据。也就是说如果缓存里缓存了 100 个字符的时候终于匹配到了关键字，那么 before 就是除了匹配到的关键字之外的所有字符
process.after - 保存匹配到的关键字，比如你在 expect 里面使用了正则表达式，那么表达式匹配到的所有字符都在 after 里面
process.match - 保存的是匹配到的正则表达式的实例，和上面的 after 相比一个是匹配到的字符串，一个是匹配到的正则表达式实例
如果 expect() 过程中发生错误，那么 before 保存到目前位置缓存里的所有数据， after 和 match 都是 None

作者：羽风之歌
链接：http://www.jianshu.com/p/cfd163200d12
來源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

"""