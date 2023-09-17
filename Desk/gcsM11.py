from gcsT import *
import gcsFunction
import subprocess
import sys
import threading
import locale
import asyncio
from mainCode import weightCalc
from gcsFunction import *

#Input with Timeout
class Local:
    # check if timeout occurred
    _timeout_occurred = False

    def on_timeout(self, process):
        self._timeout_occurred = True
        process.kill()
        try:
            import termios
            termios.tcflush(sys.stdin, termios.TCIFLUSH)
        except ImportError:
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
    } # NodeGraph : {Available Node: Weight, Available Node: Weight...}


#Program start
processCount = 0
mobilityCount = 0
mobilityCountForGCS = 0
count = 0
port = 0
print('지씨에스메인 시작!')

async def main():
    global processCount
    global mobilityCount
    global mobilityCountForGCS 
    global count
    global port

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

            count = count+1
            print(count)

        except TimeoutError as e:
            print("Timeout...")
            continue
        
        if (start != None and curr != None):
            if(start == 0 or curr == 0):
                print("Wrong Node")
            else:
                #create Mobility
                mobilityCount = mobilityCount + 1

                choice_M = mobility_choice()
                if choice_M == 'm1':
                    port = 20
                elif choice_M == 'm2':
                    port = 30
                else :
                    port = 40    
                send_Int(start, curr,'192.168.202.42', port)
                print('선정된 모빌리티는 ', choice_M, ' 입니다.')


                #모빌리티에게 DB에 저장된 현재 가중치 송신
                resul = gcsDB.systemOn_node_info()
                resul = list(resul[-1])
                del resul[0]
                send_List(resul,'192.168.202.42', port)
                mobility_set_info(choice_M, start, curr)
                    
                
                action, path = rec_pa(port)

                path_apply(choice_M, path)
                action_apply(choice_M, action)
                weight_dic = weightCalc.weightCalc(gcsGraph, action, path)

                weight_list = convert_dict_values_to_list(weight_dic)

                gcsDB.node_info_apply_weight(weight_list)

                mobilityCountForGCS = mobilityCountForGCS + 1
        try:
            end = await asyncio.wait_for(recv_end(2000), timeout=2)
            print("수신시도")
            if end is not None:
                name = 'm1'
                misson_complete(name)
                print(name, "동작 종료 확인")
        except:
            print("수신 신호 없음")
        try:
            end = await asyncio.wait_for(recv_end(3000), timeout=2)
            print("수신시도")
            if end is not None:
                name = 'm2'
                misson_complete(name)
                print(name, "동작 종료 확인")
        except:
            print("수신 신호 없음")
        #M3 추가 시 주석 해제
        # try:
        #     end = await asyncio.wait_for(recv_end(40), timeout=2)
        #     print("수신시도")
        #     if end is not None:
        #         name = 'm3'
        #         misson_complete(name)
        #         print(name, "동작 종료 확인")
        # except:
        #     print("수신확인중")


asyncio.run(main())
