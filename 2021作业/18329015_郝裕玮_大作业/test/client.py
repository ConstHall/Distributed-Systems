#coding=utf-8
import argparse
import rpyc
# argparse库:用于解析参数,并为这些参数自动生成帮助和使用信息(用于美化UI界面)
# rpyc库:它是一个Python的库,用于实现RPC和分布式计算

#Client类:客户端
class Client(object):
    #在cmd中输入help会显示如下信息
    """
    Commands Help:
    PUT key value —— Generate/Modify (key, value)
    GET key —— Query (key, value) by the key
    GETALL —— Get all (key, value) in the database
    DEL key —— Delete (key, value) by the key
    DELALL —— Delete all (key, value) in the database
    GETLOG —— Get the log
    """

    #客户端与master节点连接
    def connect(self):
        self.conn = rpyc.connect('localhost', 21000)
        #获取自己独有的客户ID
        #client要访问Master节点的代码必须通过self.conn.root.xxx才能访问
        self.id = self.conn.root.get_id()
        return self.id

    #进入运行界面
    def run(self):
        try:
            while True:
                #输入指令
                command = input("Client %d >> " %self.id)
                #指令为help则输出指南
                if command == 'help':
                    print(self.__doc__)
                #反之则调用Master节点中对应的功能函数
                else:
                    msg = self.conn.root.function(self.id, command)
                    #打印结果信息
                    if msg != None:
                        print(msg)
        except KeyboardInterrupt:
            pass


#主程序
if __name__ == '__main__':
    users = {} #初始用户列表为空
    #打开文件读取
    with open('user.txt') as file:
        for i in file.readlines():
            #每一行是用户名+空格+密码,用split函数将其分开
            #users[i[0]] = i[1]代表建立字典对应值,即users[用户名]=密码
            i = i.split()
            users[i[0]] = i[1]

    #用户登录
    username = input('Please input your username:')
    password = input('Please input your password:')
    #检测用户名和密码是否匹配
    if username in users.keys() and users[username] == password:
        client = Client()
        client_id = client.connect()

        if client_id == None:
            print('Connection Failed.')
        else:
            print('\nWelcome to Distributed Key-Value System!\n')
            print('Your client ID is %d\n' %client_id)
            print("Enter \"help\" for the list of commands:\n")
            client.run()
    else:
        print('Your username or password has something wrong.Please try again!')
