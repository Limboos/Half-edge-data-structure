from HALF_EDGE.half_edge import *
from HALF_EDGE.Half_Edge_DS import *
from HALF_EDGE.reading_data import *
def sort(l):
    if len(l) <= 1: return l
    pivolt =l[random.randint(0, len(l) - 1)].V.distance
    small, eq, larger = [], [], []
    for i in l:
        dis =i.V.distance
        if dis < pivolt:
            small.append(i)
        elif dis == pivolt:
            eq.append(i)
        else:
            larger.append(i)
    return sort(small) + eq + sort(larger)
def neighbours(edges):
    # this function return all neighbours of a Vertex
    l = []
    eTemp = edges
    while True:
        l.append(eTemp.Sym())
        eTemp = eTemp.NextV()
        if eTemp == edges:
            break
    return l
def bubblesort(list,t):
# Swap the elements to arrange in order
    for iter_num in range(len(list)-1,0,-1):
        for idx in range(iter_num):
            if list[idx].V.distance+heuristick(list[idx],t) > list[idx+1].V.distance+heuristick(list[idx+1],t):
                temp = list[idx]
                list[idx] = list[idx+1]
                list[idx+1] = temp

def dijkstra(f,t):
    toVisit=[]
    f.V.distance=0
    came_from = {}
    came_from[f.V.Vertex_id] = None
    toVisit.append(f)
    while toVisit:
        v=toVisit[0]
        del toVisit[0]
        if v.V==t.V:
            break
        v.V.visited=True
        for i in neighbours(v):
            weight = v.V.distance + i.weight
            if i.V.visited == False or weight < i.V.distance:
                i.V.distance=weight
                if i not in toVisit:
                    toVisit.append(i)
                came_from[i.V.Vertex_id] = v.V.Vertex_id

        toVisit=sort(toVisit)
    return came_from

def heuristick(g,s):
    return  round(math.sqrt((math.pow((g.V.getxy()[0] - s.V.getxy()[0]),2) + math.pow((g.V.getxy()[1] - s.V.getxy()[1]),2))),0)

def a_star(f,t):
    toVisit=[]
    f.V.distance=0
    came_from = {}
    came_from[f.V.Vertex_id] = None
    toVisit.append(f)
    while toVisit:
        v=toVisit[0]
        del toVisit[0]
        if v.V==t.V:
            break
        v.V.visited=True
        for i in neighbours(v):
            weight = v.V.distance +i.weight
            if i.V.visited == False or weight < i.V.distance:
                i.V.distance=weight
                if i not in toVisit:
                    toVisit.append(i)
                came_from[i.V.Vertex_id]=v.V.Vertex_id

        bubblesort(toVisit,t)
    return came_from

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path
