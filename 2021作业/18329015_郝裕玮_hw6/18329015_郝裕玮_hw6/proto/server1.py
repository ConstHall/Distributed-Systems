#coding=gbk
from concurrent import futures
import time
import grpc
import msg_pb2
import msg_pb2_grpc
_ONE_DAY_IN_SECONDS = 60 * 60 * 24
# 导入RPC必备的包，以及刚才生成的两个文件(grpc,msg_pb2,msg_pb2_grpc)
# 因为RPC应该长时间运行，考虑到性能，还需要用到并发的库(time,concurrent)

# 在服务器端代码中需要实现proto文件中定义的服务接口（MsgService）,并重写处理函数（GetMsg）
# Python gRPC的服务实现是写一个子类去继承proto编译生成的userinfo_pb2_grpc.UserInfoServicer
# 并且在子类中实现RPC的具体服务处理方法，同时将重写后的服务类实例化以后添加到grpc服务器中

class MsgService(msg_pb2_grpc.MsgServiceServicer):
# 工作函数
    def GetMsg(self, request, context):
    # 在GetMsg中设计msg.proto中定义的MsgResponse
    # 对收到的request的内容进行读取
        str = request.text
        msg = "从客户端收到的信息为: {}\n".format(request.text)
        # 在服务器端打印从客户端收到的内容并打印结果，用于检验接收的结果是否正确
        print(msg)

        # 将结果返回给客户端
        return msg_pb2.MsgResponse(id = 1,result = str)

# 通过并发库，将服务端放到多进程里运行
def serve():
# gRPC 服务器
    # 定义服务器并设置最大连接数,corcurrent.futures是一个并发库，类似于线程池的概念
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))# 创建一个服务器server
    msg_pb2_grpc.add_MsgServiceServicer_to_server(MsgService(), server)# 在服务器中添加派生的接口服务（自己实现的处理函数）
    server.add_insecure_port('[::]:50051')# 添加监听端口,注意保证3个服务器的监听端口不同
    print("服务器已打开，正在等待客户端连接...\n")
    server.start() # 启动服务器，同时start()不会阻塞，如果运行时无事发生，则循环等待
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)# 关闭服务器
if __name__ == '__main__':
    serve()