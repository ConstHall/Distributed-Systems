#coding=utf-8
import argparse 
import rpyc 
from rpyc.utils.server import ThreadedServer
from multiprocessing import Process 
from sqlitedict import SqliteDict 
# argparse库:用于解析参数,并为这些参数自动生成帮助和使用信息(用于美化UI界面)
# rpyc库:它是一个Python的库,用于实现RPC和分布式计算
# multiprocessing库:用于编写多线程/多进程程序
# sqlitedict库:用于将字典信息存入数据库中,且支持多线程访问

#用于记录当前进程下的每步操作(一个客户对应一个进程)
log=[]

#Server类:服务器
class Server(rpyc.Service):
	#当客户端到服务器的连接建立时,on_connect函数会被执行
	def on_connect(self, conn):
		#连接建立时,创建一个字典数据库用于存储键值
		#'./database.sqlite'代表数据库文件存储路径和文件名
		#autocommit=True代表会对每次对数据库操作的结果自动提交
		self.database = SqliteDict('./database.sqlite', autocommit=True)

	#当客户端到服务器的连接断开时,on_disconnect函数会被执行
	def on_disconnect(self, conn):
		#pass代表不进行任何操作
		pass

	#注意,Server类中"exposed_"开头的函数才能被客户端调用
	#调用时需将对应函数的exposed_删去再调用
	#生成/修改键值对(key,value)
	def exposed_Put(self, key, value):
		self.database[key] = value

	#查询键值对(key,value)
	def exposed_Get(self, key):
		#通过key来查询对应的value
		if key not in self.database:
			return None
		else:
			return self.database[key]

	#删除键值对(key,value)
	def exposed_Delete(self, key):
		if key not in self.database:
			#return
			return None
		else:
			#根据键值k删除键值对(key,value)
			del self.database[key]

	#获取数据库中所有键值对(key,value)
	def exposed_Get_All(self):
		res = [(key, self.database[key]) for key in self.database]
		#对键值对进行字典序排序(根据key值排序)
		res.sort()
		return res

	#删除数据库中所有键值对(key,value)
	def exposed_Delete_All(self):
		all_keys = [key for key in self.database]
		for key in all_keys:
			del self.database[key]
	
	#将操作记录写入日志
	def exposed_Write_Log(self,msg):
		log.append(msg)

	#展示日志
	def exposed_Get_Log(self):
		return log


#设置服务器监听端口号并运行服务器
def run(id):
	port1 = id + 20000
	server = ThreadedServer(Server, port=port1)
	try:
		#运行服务器
		server.start()
	except KeyboardInterrupt:
		server.close()

#主程序
if __name__ == '__main__':
	#(1)创建ArgumentParser()对象
	#(2)调用add_argument()方法添加参数
	#(3)使用parse_args()解析添加的参数
	parser = argparse.ArgumentParser()
	parser.add_argument('--p', type=int, default=1)
	args = parser.parse_args()

	#限制服务器在同一时间段内最多只能接受10个客户端的连接和请求
	if args.p > 10:
		raise Exception("The max number of clients is 10.")

	#创建args.p个进程
	processes = [Process(target=run,args=(i,)) for i in range(args.p)]
	print("Server is running and it can connect with %d clients at the same time." %args.p)

	#启动args.p个进程,并用join函数进行堵塞
	#join函数:在进程中可以阻塞主进程的执行,直到等待子线程全部完成之后,再继续运行主线程后面的代码
	for i in range(args.p):
		processes[i].start()
	for i in range(args.p):
		processes[i].join()

