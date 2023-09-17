#모빌리티에서 방향 추출할 함수
def directionCalc(pathValue, direction):
    for i in range(len(pathValue)):
        if pathValue[i] == 1:
            direction.append('R')
            #1의 경우 오른쪽으로 간다는 것을 의미
        elif pathValue[i] == -1:
            direction.append('L')
            #-1의 경우 왼쪽으로 간다는 것을 의미
        elif pathValue[i] == 5:
            direction.append('D')
            #5의 경우 아래로 간다는 것을 의미
        elif pathValue[i] == -5:
            direction.append('U')
            #-5의 경우 위로 간다는 것을 의미
    
    print(direction)
    return direction

#모빌리티에서 GCS로 넘겨줄 행동 추출
def actionCalc(action, direction, path_length,):
    action.append('GO')
    #시작 시의 직진 행동을 추가해즘
    
    for i in range(path_length - 2):
        a = direction[i]
        b = direction[i+1]
        #각 좌표 행동에 따라 모빌리티가 수행할 행동으로 변환 (가중치를 계산할 목적으로 단위시간 참조 안함)
        if (a == 'D'):
            if(b == 'D'):
                action.append('GO')
            elif(b == 'R'):
                action.append('TL')
            elif(b == 'L'):
                action.append('TR')
            else:
                action.append("ER")

        elif (a == 'U'):
            if(b == 'U'):
                action.append('GO')
            elif(b == 'L'):
                action.append('TL')
            elif(b == 'R'):
                action.append('TR')
            else:
                action.append("ER")

        elif (a == 'R'):
            if(b == 'R'):
                action.append('GO')
            elif(b == 'U'):
                action.append('TL')
            elif(b == 'D'):
                action.append('TR')
            else:
                action.append("ER")

        elif (a == 'L'):
            if(b == 'L'):
                action.append('GO')
            elif(b == 'D'):
                action.append('TL')
            elif(b == 'U'):
                action.append('TR')
            else:
                action.append("ER")

    # action.append('GO')
    print("action : ", action)
    

#모빌리티가 사용할 행동
def mobilActionCalc(mAction, action, errorCode):
    for i in range(len(action)):
        if (action[i] == 'GO'):
            mAction.append('GO')
            mAction.append('GO')

        elif (action[i] == "TL"):
            mAction.append('TL')
            mAction.append('GO')
            mAction.append('GO')

        elif (action[i] == "TR"):
            mAction.append('TR')
            mAction.append('GO')
            mAction.append('GO')

        else:
            mAction.append('ER')
            errorCode = 3
            print(errorCode)

    print("mAction : ", mAction)
    # 이건 맞는지 모름