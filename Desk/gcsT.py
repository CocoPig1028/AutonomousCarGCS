import socket
import pickle
import struct
# from gcs import *
import gcsDB
import asyncio


# path, action수신
def rec_pa(port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind(('',port))
    rec, addr = client_socket.recvfrom(4096)
    data = pickle.loads(rec)
    path, action = data
    client_socket.close()
    return path, action


#비동기식 데이터 수신
async def recv_end(port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind(('', port))
    loop = asyncio.get_running_loop()
    client_socket.setblocking(False)  # 소켓을 비블로킹 모드로 설정

    buffer = bytearray(1024)  # 수신 데이터를 저장할 버퍼
    await loop.sock_recvfrom_into(client_socket, buffer)
    end = buffer.decode()    
    client_socket.close()
    return end

#노드정보 송신
def send_List(resul, ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    results = gcsDB.m_info()
    for i in results :
        if i[3] == 'idle' :
            array = list(resul)
            data = pickle.dumps(array)
            client_socket.sendto(data, (ip, port))
            print(array)
            client_socket.close()
            return f'{i[0]} 모빌리티 선정 및 정보 수신 완료'

#출발지 도착지 송신
def send_Int(start, curr, ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    daInt = struct.pack('!ii', start, curr)
    client_socket.sendto(daInt, (ip, port))
    client_socket.close()
    return f'출발지, 도착지 정보 송신 완료'



    
