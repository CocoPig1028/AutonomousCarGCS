import socket
import pickle
import struct
import time

#노드정보 수신
def recv_List(port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind(('',port))
    list, addr = client_socket.recvfrom(4096)
    recdata_list = pickle.loads(list)
    client_socket.close()
    return recdata_list

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


    
