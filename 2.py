import os
from sys import argv

def dfs(v, colorDict, d):
    colorDict[v] = 'grey'
    for y in d[v]:
        if colorDict[y] == 'white':
            dfs(y, colorDict, d)
        if colorDict[y] == 'grey':
            print('Ошибка, обнаружен цикл!')
            exit()
    colorDict[v] = 'black'

if (len(argv) == 1):
    print('Не было передано аргументов!')
    exit

sourcePath = argv[1][7::]
destinationPath = argv[2][8::]

if (not os.path.isfile(sourcePath)):
    print("Не удалось открыть файл-источник, такого файла нет!")
    exit()

else:
    source = open(sourcePath, 'r')
    edges = []
    for x in source.read().split(sep='), '):
        edges.append(x[1:].split(sep=', '))

    edgesAmount = len(edges)
    edges[edgesAmount - 1][2] = edges[edgesAmount - 1][2][:-1:]

    for i in range(0, edgesAmount - 1):
        edge1 = edges[i]
        for edge2 in edges:
            if edge1 != edge2:
                if edge1[1] == edge2[1] and edge1[2] == edge2[2]:
                    print("Ошибка формата! Строка:", i + 1)
                    exit()

    edges.sort(key=lambda i: (i[1], i[2]))

    vertexList = []
    for i in range(edgesAmount):
        vertexList.append(edges[i][0])
        vertexList.append(edges[i][1])
    vertexList.sort()
    uniqueVertexList = []
    for x in vertexList:
        if x not in uniqueVertexList:
            uniqueVertexList.append(x)

    # тут начинается 2 задание
    d = {} # в d положим список смежности

    for vertex in uniqueVertexList:
        tempList = []
        for edge in edges:
            if edge[1] == vertex:
                tempList.append(edge[0])
        d[vertex] = tempList

    # проверим, есть ли в графе цикл
    colorDict = {}
    for vertex in uniqueVertexList:
        colorDict[vertex] = 'white'
    for vertex in uniqueVertexList:
        dfs(vertex, colorDict, d)

    # если нет, то продолжаем
    # найдем стоки
    drains = []
    for vertex in uniqueVertexList:
        isDrain = True
        for edge in edges:
            if edge[0] == vertex:
                isDrain = False
        if isDrain:
            drains.append(vertex)

    def calculateGraphFun(x, graphFun): # вычисление функции графа
        if len(d[x]) == 0:
            return graphFun
        graphFun += '('
        i = 0
        for y in d[x]:
            if i != 0:
                graphFun += ', '
            graphFun += f'{y}'
            graphFun = calculateGraphFun(y, graphFun)
            i += 1
        graphFun += ')'

        return graphFun

    destination = open(destinationPath, "w+")

    for drain in drains:
        graphFun = calculateGraphFun(drain, f'{drain}')
        destination.write(graphFun + '\n')