from datetime import datetime
from datetime import timedelta
from _thread import *
import gcsDB
import weightCalc
# from setSocket import *


class Mobility:
    def __init__(self, name):
        self.mobility_name = name
        #self.departure = None
        #self.destination = None
        self.comeIn = None
        self.comeOut = None
        self.status = ''
        self.path = []
        self.action = []

    def mobility_set_departure(self, departure):
        self.departure = departure

    def mobility_set_destination(self, destination):
        self.destination = destination

    def comeIn_set(self, comeIn):
        self.comeIn = comeIn

    def comeOut_set(self, comeOut):
        self.comeOut = comeOut

    def status_set(self, status):
        self.status = status

    def receive_path(self, path):
        self.path = path
        
    def receive_action(self, action):
        self.action = action

def mobility_choice(): #도착지 출발지 무조건 추가하기 
    results = gcsDB.m_info()
    for i in results :
        if i[3] == 'idle' :
            return i[0]

# 선정된 모빌리티로부터 받은 정보를 할당 / 데이터가 어떻게 넘어오는지 알아야 함
def mobility_set_info(M_name, departure, destination) : 
    if M_name == 'm1' :
        mobilities[0].mobility_set_departure(departure)
        mobilities[0].mobility_set_destination(destination)
    elif M_name == 'm2' :
        mobilities[1].mobility_set_departure(departure)
        mobilities[1].mobility_set_destination(destination)
    elif M_name == 'm3' :
        mobilities[2].mobility_set_departure(departure)
        mobilities[2].mobility_set_destination(destination)
    else :
        print('mobility_set_info error')
    gcsDB.m_info_assignment(M_name, departure, destination)
    
def path_apply(M_name, path) :
    str_arr = ' '.join(str(s) for s in path)
    gcsDB.on_path(M_name, str_arr)
    if M_name == 'm1' :
        mobilities[0].receive_path(path)
    elif M_name == 'm2' :
        mobilities[1].receive_path(path)
    elif M_name == 'm3' :
        mobilities[2].receive_path(path)
    else :
        print("경로 설정에 오류 발생")

# 가중치 반영 // 수정이 필요할 수도 
def node_weight_apply(node_weight) :
        gcsDB.node_info_apply_weight(node_weight) # 배열에 시간이 넘어오면 DB쪽 함수도 바꿔야함 
        
# comein comeout을 송신 
def comeIn_comeOut(M_name, comeout, comein) :
    #path에서 단위시간에 맞게 전송 
    gcsDB.on_comeinout(M_name, comeout, comein)
    try : 
        if M_name == 'm1' :
            mobilities[0].comeIn_set(comein)
            mobilities[0].comeOut_set(comeout)
        elif M_name == 'm2' :
            mobilities[1].comeIn_set(comein)
            mobilities[1].comeOut_set(comeout)
        elif M_name == 'm3' :
            mobilities[2].comeIn_set(comein)
            mobilities[2].comeOut_set(comeout)
        else :
            print("INOUT 설정에 오류 발생")
    except :
        print("앙")
        #전송문

#임무 완료 시
def misson_complete(M_name) :
    gcsDB.m_info_finish(M_name)
    gcsDB.del_path(M_name)

        
def convert_dict_values_to_list(dictionary):
    values = []

    
    values = [value for edges in dictionary.values() for value in edges.values()]
    return values


def action_apply(M_name, action) :
    str_arr = ' '.join(str(s) for s in action)
    gcsDB.on_action(M_name, str_arr)
    if M_name == 'm1' :
        mobilities[0].receive_action(action)
    elif M_name == 'm2' :
        mobilities[1].receive_action(action)
    elif M_name == 'm3' :
        mobilities[2].receive_action(action)
    else :
        print("경로 설정에 오류 발생")

mobilities = [Mobility('m1'), Mobility('m2'), Mobility('m3')]
#mobilities = [Mobility(i) for i in range(1,4)]

def misson_complete(M_name) :
    finish_path = gcsDB.path_info(M_name)
    finish_path = list(map(int, finish_path))
    finish_action = gcsDB.action_info(M_name)
    finish_weight_dic = weightCalc.weightCalc(gcsGraph, finish_action, finish_path)
    finish_weight_list = convert_dict_values_to_list(finish_weight_dic)
    finish_node = gcsDB.systemOn_node_info()
    finish_node = list(finish_node[0])
    del finish_node[0]
    finish_result = weight_minus(finish_node, finish_weight_list)
    node_weight_apply(finish_result)
    gcsDB.m_info_finish(M_name)
    gcsDB.del_path(M_name)
    gcsDB.del_action(M_name)
    gcsDB.del_comeinout(M_name)

def weight_minus(a, b) :
    result = [x - y for x, y in zip(a, b)]
    return result


gcsGraph = {
        1 : {6 : 0},
        2 : {7 : 0},
        3 : {8 : 0},
        5 : {6 : 0},
        6 : {1 : 0, 5 : 0, 7 : 0, 11 : 0},
        7 : {2 : 0, 6 : 0, 8 : 0, 12 : 0},
        8 : {3 : 0, 7 : 0, 9 : 0, 13 : 0},
        9 : {8 : 0},
        10 : {11 : 0},
        11 : {6 : 0, 10 : 0, 12 : 0, 16 : 0},
        12 : {7 : 0, 11 : 0, 13 : 0, 17 : 0},
        13 : {8 : 0, 12 :0, 14 : 0, 18 : 0},
        14 : {13 : 0},
        15 : {16 : 0},
        16 : {11 : 0, 15 : 0, 17 : 0, 21 : 0},
        17 : {12 : 0, 16 : 0, 18 : 0, 22 : 0},
        18 : {13 : 0, 17 : 0, 19 : 0, 23 : 0},
        19 : {18  : 0},
        21 : {16 : 0},
        22 : {19 : 0},
        23 : {18 : 0}
    }