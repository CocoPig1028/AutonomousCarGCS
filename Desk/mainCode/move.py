#전진 호출 명령 함수
def goAction():
    print("I'm Going Now")

#좌회전 호출 명령 함수
def leftAction():
    print("Turn Left")

#우회전 호출 명령 함수
def rightAction():
    print("Turn Right")

#정지 호출 명령 함수
def stopAction():
    print("Stop")

#상태 중립 호출 명령 함수
def neutral(comeIn, comeOut, goCount):
    tempNode = 0
    nodeSize = 0

    if ((goCount % 2) == 1):
        leftAction()
        leftAction()
        goAction()
        
        tempNode = comeIn
        comeIn = comeOut
        comeOut = tempNode

    nodeSize = comeIn - comeOut

    if (nodeSize == 1):
        rightAction()
    elif (nodeSize == -1):
        leftAction()
    elif (nodeSize == 5):
        stopAction()
    elif (nodeSize == -5):
        leftAction()
        leftAction()

def goBackNeutral(goCount):
    if((goCount % 2) == 1):
        leftAction()
        leftAction()
        goAction()
        leftAction()
        leftAction()
    else:
        leftAction()
        leftAction()
        goAction()
        goAction()
        leftAction()
        leftAction()