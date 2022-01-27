#coding=gbk
from concurrent import futures
import time
import grpc
import msg_pb2
import msg_pb2_grpc
_ONE_DAY_IN_SECONDS = 60 * 60 * 24
# ����RPC�ر��İ����Լ��ղ����ɵ������ļ�(grpc,msg_pb2,msg_pb2_grpc)
# ��ΪRPCӦ�ó�ʱ�����У����ǵ����ܣ�����Ҫ�õ������Ŀ�(time,concurrent)

# �ڷ������˴�������Ҫʵ��proto�ļ��ж���ķ���ӿڣ�MsgService��,����д��������GetMsg��
# Python gRPC�ķ���ʵ����дһ������ȥ�̳�proto�������ɵ�userinfo_pb2_grpc.UserInfoServicer
# ������������ʵ��RPC�ľ������������ͬʱ����д��ķ�����ʵ�����Ժ���ӵ�grpc��������

class MsgService(msg_pb2_grpc.MsgServiceServicer):
# ��������
    def GetMsg(self, request, context):
    # ��GetMsg�����msg.proto�ж����MsgResponse
    # ���յ���request�����ݽ��ж�ȡ
        str = request.text
        msg = "�ӿͻ����յ�����ϢΪ: {}\n".format(request.text)
        # �ڷ������˴�ӡ�ӿͻ����յ������ݲ���ӡ��������ڼ�����յĽ���Ƿ���ȷ
        print(msg)

        # ��������ظ��ͻ���
        return msg_pb2.MsgResponse(id = 2,result = str)

# ͨ�������⣬������˷ŵ������������
def serve():
# gRPC ������
    # ������������������������,corcurrent.futures��һ�������⣬�������̳߳صĸ���
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))# ����һ��������server
    msg_pb2_grpc.add_MsgServiceServicer_to_server(MsgService(), server)# �ڷ���������������Ľӿڷ����Լ�ʵ�ֵĴ�������
    server.add_insecure_port('[::]:50052')# ��Ӽ����˿�,ע�Ᵽ֤3���������ļ����˿ڲ�ͬ
    print("�������Ѵ򿪣����ڵȴ��ͻ�������...\n")
    server.start() # ������������ͬʱstart()�����������������ʱ���·�������ѭ���ȴ�
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)# �رշ�����
if __name__ == '__main__':
    serve()