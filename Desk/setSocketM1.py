import socket
import struct
import json

HOST = '192.168.202.42' #한서대 와이파이
# HOST = '192.168.0.17'
PORT = 3650

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
#모빌리티에서 유니티에게 시작점 전송
def send_ss(start):
    sInt = struct.pack('!i', start)
    client_socket.send(sInt)
    # client_socket.close()
    return print("시작점 송신")

# 모빌리티에서 mAction을 유니티에게 전송
def send_LList(array):
    arr = list(array)
    data_json = json.dumps(arr)
    data_bytes = data_json.encode()
    data_length = len(data_bytes)
    client_socket.send(struct.pack('!I',data_length))
    client_socket.send(data_bytes)
    # client_socket.close()
    return print("리스트 전송")
