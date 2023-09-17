def nodeInOut(nodeCount, path, comeIn, comeOut):
    comeOut = path[nodeCount]
    comeIn = path[nodeCount + 1]
    comeInD = int(comeIn)
    comeOutD = int(comeOut)
#--------------------------------------------------현재 노드, 다음 노드 송신---------------------------------------------

    print("출발 노드: ", comeOut, "향하는 노드: ", comeIn)
    return comeInD, comeOutD