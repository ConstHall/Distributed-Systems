#coding=utf-8
import argparse
import rpyc
from rpyc.utils.server import ThreadedServer
# argparse库:用于解析参数,并为这些参数自动生成帮助和使用信息(用于美化UI界面)
# rpyc库:它是一个Python的库,用于实现RPC和分布式计算

#Middle类:分布式系统中间件
class Middle(rpyc.Service):
	#当客户端到服务器的连接建立时,on_connect函数会被执行
    def on_connect(self, conn):
        pass

	#当客户端到服务器的连接断开时,on_disconnect函数会被执行
    def on_disconnect(self, conn):
        #依次断开客户端和服务器的连接
        for temp in clients:
            temp.close()

    #为当前客户分配ID
    def exposed_get_id(self):
        #遍历client_ids表,寻找尚未分配的id
        for i in range(len(client_ids)):
            #若client_ids[i]尚未分配则设置其为True(已使用)并返回序号i
            if client_ids[i] == False:
                client_ids[i] = True
                return i
        return None

    #执行各种command
    def exposed_function(self, client_id, clause):
        clause = clause.strip().split()
        #将command根据空格进行分割
        #strip()可消去字符串前后的空格(不包括中间)
        #split()将字符串根据空格进行分割
        lens = len(clause)

        WRONG_MSG = 'Wrong command. Enter help if necessary.'
        if lens < 1:
            return WRONG_MSG

        #将指令的第一个单词全部转为小写,便于后续判定
        #易知指令的第一个单词小写化后只可能是:put,get,getall,del,delall,getlog
        command = clause[0].lower()

        #开始进行条件判断
        #对于PUT key value
        if command == 'put':
            if lens == 3:
                key = clause[1]
                value = clause[2]
                #client要访问服务器的代码必须通过self.conn.root.xxx才能访问
                clients[client_id].root.Put(key, value)
                #将本次操作PUT key value写到对应客户的日志中
                clients[client_id].root.Write_Log('PUT ('+str(key)+','+str(value)+')')
            else:
                return WRONG_MSG

        #对于GET key
        if command == 'get':
            if lens == 2:
                key = clause[1]
                #client要访问服务器的代码必须通过self.conn.root.xxx才能访问
                result = clients[client_id].root.Get(key)
                #将本次操作GET key写到对应客户的日志中
                clients[client_id].root.Write_Log('GET '+str(key))
            else:
                return WRONG_MSG

            if result == None:
                return 'Key %s not found.' %key
            else:
                return result

        #对于GETALL
        if command == 'getall':
            if lens == 1:
                #client要访问服务器的代码必须通过self.conn.root.xxx才能访问
                #将本次操作GETALL写到对应客户的日志中
                clients[client_id].root.Write_Log('GETALL')
                return clients[client_id].root.Get_All()
            else:
                return WRONG_MSG

        #对于DEL key
        if command == 'del':
            if lens == 2:
                key = clause[1]
                #client要访问服务器的代码必须通过self.conn.root.xxx才能访问
                clients[client_id].root.Delete(key)
                #将本次操作DEL key写到对应客户的日志中
                clients[client_id].root.Write_Log('DEL '+str(key))
            else:
                return WRONG_MSG

        #对于DELALL
        if command == 'delall':
            if lens == 1:
                #client要访问服务器的代码必须通过self.conn.root.xxx才能访问
                #将本次操作GETALL写到对应客户的日志中
                clients[client_id].root.Write_Log('DELALL')
                return clients[client_id].root.Delete_All()
            else:
                return WRONG_MSG

        #对于GETLOG
        if command == 'getlog':
            if lens == 1:
                #client要访问服务器的代码必须通过self.conn.root.xxx才能访问
                return clients[client_id].root.Get_Log()
            else:
                return WRONG_MSG


#主程序
if __name__ == '__main__':
	#(1)创建ArgumentParser()对象
	#(2)调用add_argument()方法添加参数
	#(3)使用parse_args()解析添加的参数
    parser = argparse.ArgumentParser()
    parser.add_argument('--p', type=int, default=1)
    args = parser.parse_args()

    #建立一个bool数组,初始化为args.p个False变量,表示这些id都未被使用
    client_ids = [False] * args.p

    #设置中间件的监听端口号用于和不同的服务器节点相连接
    clients = [rpyc.connect('localhost', 20000+i) for i in range(args.p)]
    #设置中间件与客户端连接的端口号
    middle = ThreadedServer(Middle, port=21000)
    print("Middleware is running...\n")
    middle.start()
