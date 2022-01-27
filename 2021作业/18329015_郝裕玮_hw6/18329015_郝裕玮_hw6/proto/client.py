#coding=gbk
from __future__ import print_function
import grpc
import msg_pb2
import msg_pb2_grpc
import copy

def run():
    times = 1 #��¼�ط�����

    # �ͻ��˺ܺ����,�������ӵõ�һ��channel,��channelȥʵ����һ��stub,ͨ��stub����RPC����
    # ��������3����������������Ҫ3��channel
    channel1 = grpc.insecure_channel('localhost:50051')
    channel2 = grpc.insecure_channel('localhost:50052')
    channel3 = grpc.insecure_channel('localhost:50053')

    # ʹ��grpc.insecure_channel('localhost:50051')�������ӷ����,���������channel�ϴ���stub
    # ͬ���ֱ���3���������ϴ�����ͬ��stub
    stub1 = msg_pb2_grpc.MsgServiceStub(channel1)
    stub2 = msg_pb2_grpc.MsgServiceStub(channel2)
    stub3 = msg_pb2_grpc.MsgServiceStub(channel3)
    # ��msg_pb2_grpc������ҵ�MsgServiceStub����������Ϣ�����stub���Ե���Զ�̵�GetMsg����
    
    text1 = input() #���뷢�͸�3��������������
    #��������,���ڷ���������2,3
    text2 = copy.deepcopy(text1) 
    text3 = copy.deepcopy(text1)

    #������֤�ط�����
    #text1 = "Different!"
    #text2 = "Different!"
    #text3 = "Different!"
    print('\n')

    # responseΪ�������˷���������
    # MsgRequest�е����ݼ�msg.proto�ж�������ݡ��ڻ�Ӧ����Եõ�msg.proto�ж����msg
    response1 = stub1.GetMsg(msg_pb2.MsgRequest(text = text1))
    response2 = stub2.GetMsg(msg_pb2.MsgRequest(text = text2))
    response3 = stub3.GetMsg(msg_pb2.MsgRequest(text = text3))
    
    # �Ƚϴ�3���������յ��Ľ���Ƿ�һ�£�����һ���򽫲�һ�µ���Ϣ�����ط�
    # ������1��������
    if response2.result == response3.result and response1.result != response3.result:
        #�ͻ����ط�10��
        while times<=10:
            #�Է�����1�����ط�
            response1 = stub1.GetMsg(msg_pb2.MsgRequest(text = text1)) 
            #��ӡ�ط��������1���ص���Ϣ
            print("�ͻ��˵�{}���ط���������{}���ص���ϢΪ: {}\n".format(times,response1.id,response1.result))
            #��ĳ���ط�������������������������һ�������ط�
            if response1.result == response3.result:
                break
            else:#��֮times+1,�����ط�
                times+=1

    #������2��������
    elif response1.result == response3.result and response2.result != response3.result:
        while times<=10:
            response2 = stub2.GetMsg(msg_pb2.MsgRequest(text = text2))
            print("�ͻ��˵�{}���ط���������{}���ص���ϢΪ: {}\n".format(times,response2.id,response2.result))

            if response2.result == response3.result:
                break
            else:
                times+=1

    #������3��������
    elif response1.result == response2.result and response3.result != response1.result:
        while times<=10:
            response3 = stub3.GetMsg(msg_pb2.MsgRequest(text = text3))
            print("�ͻ��˵�{}���ط���������{}���ص���ϢΪ: {}\n".format(times,response3.id,response3.result))

            if response3.result == response1.result:
                break
            else:
                times+=1

    #������1,2,3����������
    elif response1.result != response2.result and response2.result != response3.result and response1.result != response3.result:
        while times<=10:
            response1 = stub1.GetMsg(msg_pb2.MsgRequest(text = text1))
            print("�ͻ��˵�{}���ط���������{}���ص���ϢΪ: {}\n".format(times,response1.id,response1.result))

            response2 = stub2.GetMsg(msg_pb2.MsgRequest(text = text2))
            print("�ͻ��˵�{}���ط���������{}���ص���ϢΪ: {}\n".format(times,response2.id,response2.result))      

            response3 = stub3.GetMsg(msg_pb2.MsgRequest(text = text3))
            print("�ͻ��˵�{}���ط���������{}���ص���ϢΪ: {}\n".format(times,response3.id,response3.result))

            if response1.result == response2.result and response2.result == response3.result:
                break
            else:
                times+=1

    #�ط�������
    if response1.result == response2.result and response2.result == response3.result:
        if times == 1:
            print("�����ط�,3�����������ؽ��һ��!\n")
        else:
            print("�ط�{}�κ�,3�����������ؽ��һ��!\n".format(times-1))
    else:
        print("�ط�{}�κ�,3�����������ؽ���Բ�һ��!\n".format(times-1))

    print("����,������{}���ص���ϢΪ: {}\n".format(response1.id,response1.result))
    print("����,������{}���ص���ϢΪ: {}\n".format(response2.id,response2.result))
    print("����,������{}���ص���ϢΪ: {}\n".format(response3.id,response3.result))

if __name__ == '__main__':
    run()