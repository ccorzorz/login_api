#!/usr/bin/env python
# encoding: utf-8
# Auther:ccorz Mail:ccniubi@163.com

import time,getpass,os
#  将输入用户赋值于user_name变量
# print('=============',os.popen('pwd').read())
user_name=input('请输入您的用户名:')
#  打开文件user_list,user_lock,赋予读写权限
user_list=open('user_list','r+')
user_lock=open('user_lock','r+')
#设置日志文件,open如果,用追加模式
log_file=open('login.log','a+')
#  设置一个退出标识符
break_flag=0
time_now=time.strftime('%Y-%m-%d %H:%M:%S')

#遍历user_lock被锁用户文件
for line in user_lock:
    # 设置被锁用户的变量,strip()将字符串两边的空格符去掉
    lock_name=line.strip()
    #判断输入用户是否与遍历用户相同
    if user_name==lock_name:
        print('您的用户已被锁定...请尝试其他的用户')
        log_file.write('\n%s:被锁定用户%s尝试登陆!'%(time_now,user_name))
        #修改退出标识符的值,以便区分既在user_list,又在user_lock的用户
        break_flag=1
        #退出循环
        break
#将空字典赋予变量account
account={}
for line in user_list:
    #遍历user_list文件,将一行的字符串去掉空格,并按":"分割为key value,并将key value添加入dict中
    account[line.strip().split(':')[0]]=line.strip().split(':')[1]
# print(account)

# break_flag==0用来区分在user_list,user_lock中同时存在的用户,
# 如果没有此标识符,上面遍历锁用户文件也会执行以下程序
if user_name in account and break_flag==0:
    #设置计数器,初始值为0
    count=0
    #循环3次
    while count < 3:
        password=input('请输入%s的密码:'%user_name)
        # 校验密码
        if password==account[user_name]:
            print('欢迎登陆系统.......')
            log_file.write('\n%s,user %s had login.'%(time_now,user_name))
            # 退出循环
            break
        else:
            # 密码错误,将计数器+1
            count+=1
            print('%s的密码错误,请重新输入,您还有%s次机会'% (user_name,3-count))
    # 循环超过3次,执行下面命令
    else:
        print('用户%s已经被锁定,请联系管理员!'%user_name)
        # 将密码输入超过3此的用户名添加进user_lock,写入日志文件
        user_lock.write('\n%s'%user_name)
        log_file.write('\n%s:%s is locked!'%(time.strftime('%Y-%m-%d %H:%M:%S'),user_name))
if user_name not in account:
    # \033[1;44;33m....\033[0m 高亮显示,并提醒用户无此用户,是否用此用户名注册
    regis_or_quit=input('''\033[1;44;33m没有用户%s,是否注册此用户?\033[0m
\033[1;44;33m输入"y"继续注册,输入"q"退出:\033[0m'''%user_name)
    #将输入的字符串转化为小写并与y或者q匹配
    if regis_or_quit.lower()=='q':
        print('Bye!!!!!!!!')
    elif regis_or_quit.lower()=='y':
        #直接使用user_name注册,第一次输入密码密码,如果不想显示明文密码可用getpass.getpass('...')
        regis_pass=input('请输入%s的密码:'%user_name)
        #允许两次确认密码,设置循环2次,故也无需设置计数器
        for i in range(2):
            #确认注册密码,防止用户忘记密码
            regis_pass_again=input('请确认注册用户%s的密码:'%user_name)
            # 校验注册密码
            if regis_pass_again==regis_pass:
                # 校验密码成功,将user_name regis_pass两个变量的值写入user_list文件,并提醒用户注册成功
                user_list.write('\n%s:%s'%(user_name,regis_pass))
                log_file.write('\n%s:%s注册成功'%(time_now,user_name))
                print('用户%s注册成功.....'%user_name)
                # 退出循环
                break
            #校验注册密码失败,进入下一次循环
            else:
                print('\033[1;33;44m密码与上次不一致.......\033[0m')
        #密码确认超过两次,注册失败
        else:
            print('用户%s注册失败'%user_name)
    #输入不为y或者q,其他字符串或者回车 空格时,程序显示退出
    else:
        print('输入不符合规范,程序已退出.....')
#将open的两个账户文件关闭,也可用with open() as xxx,open() as xxxx
user_list.close()
user_lock.close()
log_file.close()






