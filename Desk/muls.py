import socket
import pickle
import struct
from gcsFunction import *
import gcsDB
import asyncio
import time
# from gcs11 import *

#노드정보 수신
def recv_List(port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind(('',port))
    list, addr = client_socket.recvfrom(4096)
    recdata_list = pickle.loads(list)
    client_socket.close()
    return recdata_list

# path, action수신
def rec_pa(port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind(('',port))
    rec, addr = client_socket.recvfrom(4096)
    data = pickle.loads(rec)
    path, action = data
    client_socket.close()
    return path, action

# path, action 송신
def send_pa(action, path, ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = (action, path)
    dataa = pickle.dumps(data)
    client_socket.sendto(dataa, (ip, port))
    client_socket.close()


#출발지 도착지 수신
def recv_Int(port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind(('',port))
    data, addr = client_socket.recvfrom(8)
    daInt = struct.unpack('!ii',data)
    start, curr = daInt
    client_socket.close()
    return start, curr

#컴인컴아웃 수신
def recv_Come(port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind(('',port))
    data, addr = client_socket.recvfrom(8)
    comeda = struct.unpack('!ii',data)
    comeIn, comeOut = comeda
    client_socket.close()
    return comeIn, comeOut

#비동기식 데이터 수신
async def recv_end(port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.bind(('', port))
    loop = asyncio.get_running_loop()
    client_socket.setblocking(False)  # 소켓을 비블로킹 모드로 설정

    buffer = bytearray(1024)  # 수신 데이터를 저장할 버퍼
    await loop.sock_recvfrom_into(client_socket, buffer)
    # end, address = buffer.decode()
    end = buffer.decode()

    # client_socket.sendto(b'ACK', address)
    
    client_socket.close()
    return end

def rec(port):
    print("수신 대기중")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind(('', port))
    end = client_socket.recv(1024).decode('utf-8')
    print(end, "받음!")
    if port ==20:
        name = 'm1'
    elif port == 30:
        name = 'm2'
    elif port == 40:
        name = 'm3'
    misson_complete(name)
                
    return print(name, "이제 끝났냐")
    

    

#컴인컴아웃 송신
def send_Come(comeIn, comeOut, ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = struct.pack('!ii',comeIn, comeOut)
    client_socket.sendto(data, (ip, port))
    client_socket.close()

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

import time
# 엔드포인트 송신
def send_end(end, ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(3)  # 타임아웃 시간을 6초로 설정

    try:
        start_time = time.time()  # 전송 시작 시간 기록
        while time.time() - start_time <= 3:  # 6초 동안 반복
            client_socket.sendto(end.encode(), (ip, port))

        print("데이터 전송 완료")
    except socket.timeout:
        print("데이터 전송 중 타임아웃 발생")
    finally:
        client_socket.close()


    
