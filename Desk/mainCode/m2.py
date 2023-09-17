import pathExtraction #경로 추출 함수
import pathCalc #행동 추출 함수
import move #이동 함수
import nodeTrans #현재 노드 및 향하는 노드를 구하는 함수
import time #timeSleep을 위한 함수
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from weightCalc import *
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from setSocketM2 import *
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from mobilT import *


# HOST = '192.168.202.42' #한서대 와이파이
# PORT = 3650

##GCS의 포트번호는 50으로 고정

# from multsocket import *
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
    } # 기준노드 : {연결 가능한 노드: 가중치, 연결 가능한 노드: 가중치...}

#경로에 필요한 배열들
path = [] #경로
pathValue = [] #경로 간 수학적 계산 배열
direction = [] #방향
action = [] #기본 행동
mAction = [] #모빌리티용 세부 행동

option = 0 #while문 내의 수행 조건
nodeCount = 0 #node의 참조 배열
moveCount = 0 #행동의 참조 배열
goCount = 0 #go가 나온 횟수
errorCode = 0 #장애물 등 여러 상황에 중지 시키기 위한 에러
comeOut = 0 #현재 혹은 출발한 노드
comeIn = 0 #나중 혹은 회전시 현재 노드
port = 0
print('m2 모빌리티메인 시작!')

while True:
    if option == 0:
        port = 3000
        print("수신 대기 중")
        #출발지와 도착지를 받는 지점
#------------------------------------------------------출발지, 도착지 수신--------------------------------------------------------
        
        # 출발지 도착치 수신
        start, curr = recv_Int(port)
        print("출발지와 도착지 : ", start, curr)


#------------------------------------------------------가중치 그래프 적용 시점(가중치 테이블 수신)-------------------------------------
        #gcsGraph = DB에서 가져온 가중치 테이블
        nodeLIst = recv_List(port)
        print("Receive List : ", nodeLIst)
        gcsgraph = assign_list_values(gcsGraph, nodeLIst)
        if start != 0 and curr != 0: #명령을 받는 것을 계속 반복하여 기다릴지 아니면 행동을 할지 선택해주는 조건문
            option = 1
            time.sleep(1)

    else:
        path = pathExtraction.pathExtraction(gcsGraph, start, curr)
        #경로 추출 완료

        path_length = len(path)
        #경로의 길이

        pathValue = [path[i + 1] - path[i] for i in range(path_length - 1)]
        #행동을 추출하기 위한 산술 알고리즘

        pathCalc.directionCalc(pathValue, direction) #좌표를 기준으로 위, 아래, 좌, 우의 움직임 추출
        pathCalc.actionCalc(action, direction, path_length) #direction의 배열을 이용하여 기초 행동 추출
        pathCalc.mobilActionCalc(mAction, action, errorCode) # #direction의 배열을 이용하여 모빌리티에서 사용할 행동 추출
    #---------------------------------------------action, path송신-----------------------------
        
        send_pa(action, path, '192.168.0.17', port)
         # 유니티에 보내야함

        print("유니티에게 mAction과 출발지 도착지 송신해야함")
        send_ss(start)
        send_LList(mAction)
    

        print("출발지 도착지 보냄")
        print("행동실행")
        for i in range(len(mAction)): #노드 정보와 행동을 위한 유한(행동 크기)루프
            comeIn, comeOut = nodeTrans.nodeInOut(nodeCount, path, comeIn, comeOut)
            #현재 노드와 다음 노드를 전송해 줌
            # send_Come(comeIn, comeOut,'192.168.202.42', port) 
            #위의 코드 들어간 후 comeIn, comeOut GCS와 통신 바람

            #Error 판단
            if errorCode != 0:
                move.stopAction()
                print("ErrorCode: ", errorCode)
                    
                if errorCode == 1:
                    print("Detected Obstacle")
                    move.goBackNeutral()
                    move.neutral()
#------------------------------------------------------------------현재 상황 송신, 노드 사용 불가능(그 노드(comeOut) 가중치 100으로 올려주기)------------------------------------------------------------------
                    break

                elif errorCode == 2:
                    print("Another Mobility is in Next Node")
                    move.neutral()
                    move.goBackNeutral()
#------------------------------------------------------------------현재 상황 송신------------------------------------------------------------------

                elif errorCode == 3:
                    print("Path Error")
                    move.goBackNeutral()
                    move.neutral()
            #Error가 없을 시 동작 실행
            elif errorCode == 0:
                #에러 전송
                # send_error(errorCode)
                #아래의 부분은 모빌리티 행동 명령 호출
                if(mAction[moveCount] == 'GO'):
                    move.goAction()
                    goCount = goCount + 1
                    #Go의 갯수를 goCount에 축적

                elif(mAction[moveCount] == 'TL'):
                    move.leftAction()

                elif(mAction[moveCount] == 'TR'):
                    move.rightAction()

                else:
                    move.stopAction()

                # print("goCount: ", goCount)

                if (goCount % 2 == 0):
                    nodeCount = goCount // 2
                    #goCount가 짝수개일 때마다 노드 이동이 이루어짐을 이용하여 nodeCount의 정보 변경)

                # print("nodeCount: ", nodeCount)
                moveCount = moveCount + 1
                #다음 행동을 추출하기 위해 moveCount 증가

                time.sleep(2)
                #단위 시간대로 움직이기

        omeOut = 0
        comeIn = 0
        end = 'end'
        # print("checkpoint1",comeIn,comeOut)
        # # ============================종료 포인트======================
        # if(comeIn ==0):
        send_end(end,'192.168.0.17', port)
        print("send endPoint")
        
        port = 0
        option = 0
        nodeCount = 0
        moveCount = 0
        goCount = 0
        errorCode = 0
        
        #행동이 끝난 후 사용된 변수 0으로 초기화

        path.clear()
        pathValue.clear()
        direction.clear()
        action.clear()
        mAction.clear()
        #다음 명령을 위해 배열 초기화
#-------------------------------------------------------행동이 끝났다는 명령 필요하면 통신 추가 바람------------------------------------------------------