from __future__ import print_function
import grpc
import msg_pb2
import msg_pb2_grpc

def run():
    # 客户端很好理解,网络连接得到一个channel,拿channel去实例化一个stub,通过stub调用RPC函数
    channel = grpc.insecure_channel('localhost:50051')
    # 使用grpc.insecure_channel('localhost:50051')进行连接服务端,接着在这个channel上创建stub
    stub = msg_pb2_grpc.MsgServiceStub(channel)
    # 在msg_pb2_grpc里可以找到MsgServiceStub这个类相关信息。这个stub可以调用远程的GetMsg函数
    
    a1 = float(input());# 输入运算数1，并转为float型
    op1 = input();# 输入运算符号类型
    b1 = float(input());# 输入运算数2，并转为float型

    response = stub.GetMsg(msg_pb2.MsgRequest(a=a1,op=op1,b=b1))# response为服务器端发来的内容
    # MsgRequest中的内容即msg.proto中定义的数据。在回应里可以得到msg.proto中定义的msg

    msg = "服务器端运算结果为：{}\n".format(response.result)#打印从服务器端接收到的数据，即运算结果
    print(msg)

if __name__ == '__main__':
    run()