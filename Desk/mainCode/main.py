import weightCalc
import pathCalc
import pathExtraction
# import nodeInfo
import move

gcsGraph = {
        1 : {6 : 0},
        2 : {7 : 0},
        3 : {8 : 0},
        5 : {6 : 0},
        6 : {1 : 0, 5 : 0, 7 : 4, 11 : 0},
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

node = {
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

print("Please enter path node!")

start = 1
curr = 2

path = []
pathValue = []
direction = []
action = []
mAction = []

path = pathExtraction.pathExtraction(gcsGraph, start, curr)

path_length = len(path)
path_lengthM = path_length - 1

pathValue = [path[i + 1] - path[i] for i in range(path_length - 1)]

pathCalc.directionCalc(pathValue, direction)
pathCalc.actionCalc(action, direction, path_length)
pathCalc.mobilActionCalc(mAction, direction, path_length)
weightCalc.weightCalc(gcsGraph, action, path)
print("행동실행")
move.moveMain(mAction)
# nodeInfo.nodeInfo(gcsGraph, node)
weightCalc.weightReset(gcsGraph, action, path)