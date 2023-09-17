# from gcs import *
from muls import *
import gcsDB
import subprocess
import sys
import threading
import locale
import asyncio
# import threading
from weightCalc import *
from gcsFunction import *

#제한 시간을 가진 Input 기능 코드
class Local:
    # check if timeout occurred
    _timeout_occurred = False

    def on_timeout(self, process):
        self._timeout_occurred = True
        process.kill()
        # clear stdin buffer (for Linux)
        try:
            import termios
            termios.tcflush(sys.stdin, termios.TCIFLUSH)
        except ImportError:
            # Windows, just exit
            pass

    def input_timer_main(self, prompt_in, timeout_sec_in):
        # print with no new line
        print(prompt_in, end="")
        sys.stdout.flush()

        # new python input process create
        cmd = [sys.executable, '-c', 'print(input())']
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
            timer_proc = threading.Timer(timeout_sec_in, self.on_timeout, [proc])
            try:
                # timer set
                timer_proc.start()
                stdout, stderr = proc.communicate()

                # get stdout and trim new line character
                result = stdout.decode(locale.getpreferredencoding()).strip("\r\n")
            finally:
                # timeout clear
                timer_proc.cancel()

        # timeout check
        if self._timeout_occurred or not result:
            # move the cursor to the next line
            print("")
            return None  # Return None when timeout occurs or no input is provided
        return result
    
def input_timer(prompt, timeout_sec):
    t = Local()
    return t.input_timer_main(prompt, timeout_sec)

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


#Program start
processCount = 0
mobilityCount = 0
mobilityCountForGCS = 0
count = 0
port = 0
ip = 0
print('지씨에스메인 시작!')

async def main():
    global processCount
    global mobilityCount
    global mobilityCountForGCS 
    global count
    global port
    global ip

    mobileArray = [20, 30, 40]

    while True:
        #출발지, 목적지 입력 제한시간 내 입력. 만약 시간 내에 입력 되지 않으면 사이클 돌아감. 여기서는 1초로 지점
        start = 0
        curr = 0

        try:
            start = None
            curr = None
            a = input_timer("* start: ", 1)
            if a is None:
                print("Timeout occurred!")
            else:
                start = int(a)

            a = input_timer("* curr: ", 1)
            if a is None:
                print("Timeout occurred!")
            else:
                curr = int(a)

            # print("start:", start)
            # print("curr:", curr)
            count = count+1
            print(count)

        except TimeoutError as e:
            print("Timeout...")
            # print("start:", start)
            # print("curr:", curr)
            continue

        # print("done")
        
        if (start != None and curr != None):
            if(start == 0 or curr == 0):
                print("Wrong Node")
            else:
                #모빌리티 생성
                mobilityCount = mobilityCount + 1
                # print('mobilityCount: ', mobilityCount)

                #모빌리티에게 출발지 목적지 송신
                print('모빌리티를 선정합니다.')
                choice_M = mobility_choice()
                # if choice_M == 'm1':
                #     port = 2000
                #     ip = '192.168.203.34'
                # elif choice_M == 'm2':
                #     port = 3000
                #     ip = '192.168.201.25'
                # elif choice_M == 'm3' :
                #     port = 4000
                #     ip = '192.168.202.42' 
                ip = '192.168.0.17'
                if choice_M == 'm1':
                    port = 2000
                    # ip = '192.168.202.42'
                elif choice_M == 'm2':
                    port = 3000
                    # ip = '192.168.202.42'
                elif choice_M == 'm3' :
                    port = 4000
                    # ip = '192.168.202.42'    
                send_Int(start, curr, ip, port) #어떤 모빌리티에게 보내야 하는지
                print('선정된 모빌리티는 ', choice_M, ' 입니다.')


                #모빌리티에게 DB에 저장된 현재 가중치 송신
                resul = gcsDB.systemOn_node_info()
                resul = list(resul[-1])
                del resul[0]
                print(ip)
                send_List(resul,ip, port) #어떤 모빌리티에게 보내야 하는지 / 노드 상태 정보 송신
                mobility_set_info(choice_M, start, curr) # 시,도,상 할당 
        #-----------------------------------path, action받기----------------------------------------------
                    
                
                action, path = rec_pa(port)
                # print("Receive Path : ",path)
                # print("Received action : ",action)

                path_apply(choice_M, path)
                action_apply(choice_M, action)
                weight_dic = weightCalc.weightCalc(gcsGraph, action, path)

                weight_list = convert_dict_values_to_list(weight_dic)

                gcsDB.node_info_apply_weight(weight_list)

                mobilityCountForGCS = mobilityCountForGCS + 1
        # ----------------------------미션 끝---------------------------------------
        try:
            end = await asyncio.wait_for(recv_end(20), timeout=2)
            print("수신시도")
            if end is not None:
                name = 'm1'
                # path action 가지고 오고 현재 가중치 가지고 오고 계산해서 빼주고 다시 가중치 넣어주는 방식 
                misson_complete(name)
                print(name, "이제 끝났냐")
        except:
            print("빨리하라고")
        try:
            end = await asyncio.wait_for(recv_end(30), timeout=2)
            print("수신시도")
            if end is not None:
                name = 'm2'
                misson_complete(name)
                print(name, "이제 끝났냐")
        except:
            print("빨리하라고")
        # try:
        #     end = await asyncio.wait_for(recv_end(40), timeout=2)
        #     print("수신시도")
        #     if end is not None:
        #         name = 'm3'
        #         misson_complete(name)
        #         print(name, "이제 끝났냐")
        # except:
        #     print("빨리하라고")


asyncio.run(main())
