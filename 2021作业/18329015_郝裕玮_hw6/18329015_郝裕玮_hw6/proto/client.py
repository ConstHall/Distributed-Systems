#coding=gbk
from __future__ import print_function
import grpc
import msg_pb2
import msg_pb2_grpc
import copy

def run():
    times = 1 #记录重发次数

    # 客户端很好理解,网络连接得到一个channel,拿channel去实例化一个stub,通过stub调用RPC函数
    # 这里连接3个服务器，所以需要3个channel
    channel1 = grpc.insecure_channel('localhost:50051')
    channel2 = grpc.insecure_channel('localhost:50052')
    channel3 = grpc.insecure_channel('localhost:50053')

    # 使用grpc.insecure_channel('localhost:50051')进行连接服务端,接着在这个channel上创建stub
    # 同样分别在3个服务器上创建不同的stub
    stub1 = msg_pb2_grpc.MsgServiceStub(channel1)
    stub2 = msg_pb2_grpc.MsgServiceStub(channel2)
    stub3 = msg_pb2_grpc.MsgServiceStub(channel3)
    # 在msg_pb2_grpc里可以找到MsgServiceStub这个类相关信息。这个stub可以调用远程的GetMsg函数
    
    text1 = input() #输入发送给3个服务器的内容
    #复制内容,便于发往服务器2,3
    text2 = copy.deepcopy(text1) 
    text3 = copy.deepcopy(text1)

    #用于验证重发功能
    #text1 = "Different!"
    #text2 = "Different!"
    #text3 = "Different!"
    print('\n')

    # response为服务器端发来的内容
    # MsgRequest中的内容即msg.proto中定义的数据。在回应里可以得到msg.proto中定义的msg
    response1 = stub1.GetMsg(msg_pb2.MsgRequest(text = text1))
    response2 = stub2.GetMsg(msg_pb2.MsgRequest(text = text2))
    response3 = stub3.GetMsg(msg_pb2.MsgRequest(text = text3))
    
    # 比较从3个服务器收到的结果是否一致，若不一致则将不一致的消息进行重发
    # 服务器1出错的情况
    if response2.result == response3.result and response1.result != response3.result:
        #客户端重发10次
        while times<=10:
            #对服务器1进行重发
            response1 = stub1.GetMsg(msg_pb2.MsgRequest(text = text1)) 
            #打印重发后服务器1返回的信息
            print("客户端第{}次重发，服务器{}返回的消息为: {}\n".format(times,response1.id,response1.result))
            #若某次重发后结果与其他两个服务器返回一致则不再重发
            if response1.result == response3.result:
                break
            else:#反之times+1,继续重发
                times+=1

    #服务器2出错的情况
    elif response1.result == response3.result and response2.result != response3.result:
        while times<=10:
            response2 = stub2.GetMsg(msg_pb2.MsgRequest(text = text2))
            print("客户端第{}次重发，服务器{}返回的消息为: {}\n".format(times,response2.id,response2.result))

            if response2.result == response3.result:
                break
            else:
                times+=1

    #服务器3出错的情况
    elif response1.result == response2.result and response3.result != response1.result:
        while times<=10:
            response3 = stub3.GetMsg(msg_pb2.MsgRequest(text = text3))
            print("客户端第{}次重发，服务器{}返回的消息为: {}\n".format(times,response3.id,response3.result))

            if response3.result == response1.result:
                break
            else:
                times+=1

    #服务器1,2,3均出错的情况
    elif response1.result != response2.result and response2.result != response3.result and response1.result != response3.result:
        while times<=10:
            response1 = stub1.GetMsg(msg_pb2.MsgRequest(text = text1))
            print("客户端第{}次重发，服务器{}返回的消息为: {}\n".format(times,response1.id,response1.result))

            response2 = stub2.GetMsg(msg_pb2.MsgRequest(text = text2))
            print("客户端第{}次重发，服务器{}返回的消息为: {}\n".format(times,response2.id,response2.result))      

            response3 = stub3.GetMsg(msg_pb2.MsgRequest(text = text3))
            print("客户端第{}次重发，服务器{}返回的消息为: {}\n".format(times,response3.id,response3.result))

            if response1.result == response2.result and response2.result == response3.result:
                break
            else:
                times+=1

    #重发结束后
    if response1.result == response2.result and response2.result == response3.result:
        if times == 1:
            print("无需重发,3个服务器返回结果一致!\n")
        else:
            print("重发{}次后,3个服务器返回结果一致!\n".format(times-1))
    else:
        print("重发{}次后,3个服务器返回结果仍不一致!\n".format(times-1))

    print("最终,服务器{}返回的消息为: {}\n".format(response1.id,response1.result))
    print("最终,服务器{}返回的消息为: {}\n".format(response2.id,response2.result))
    print("最终,服务器{}返回的消息为: {}\n".format(response3.id,response3.result))

if __name__ == '__main__':
    run()