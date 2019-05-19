import turtle, random
from HALF_EDGE import data_base as db
from HALF_EDGE.Half_Edge_DS import *
from HALF_EDGE.reading_data import *
from HALF_EDGE.path_finding import *
def Fast_splice(edges):
    # this function connect all edges that should be connect
    # i use a dictionary to create a 'neighborhood matrix'
    v_id = {}
    for i in edges:
        v_id.update({i.V.Vertex_id: None})
        v_id.update({i.Sym().V.Vertex_id: None})

    for e in edges:
        if v_id[e.V.Vertex_id] == None:
            v_id[e.V.Vertex_id] = []
        v_id[e.V.Vertex_id].append(e)
        if v_id[e.Sym().V.Vertex_id] == None:
            v_id[e.Sym().V.Vertex_id] = []
        v_id[e.Sym().V.Vertex_id].append(e.Sym())

    A = []

    for az in v_id.values():
        for i in az:
            A.append([Azymut(i), i])
        A.sort()
        if len(A) == 2:
            Splice(A[1][1], A[0][1])
        else:
            for i in range(len(A) - 1):
                Splice(A[0][1], A[i + 1][1])
        A = []
    return v_id


def Azymut(e):
    # funciton to count angle betwen two vertex
    # this function return an Angle
    # i am useing a Geodesy theory for angel
    x = e.Sym().V.getxy()[0] - e.V.getxy()[0]
    y = e.Sym().V.getxy()[1] - e.V.getxy()[1]

    if x == 0 and y > 0:
        return 0
    elif x == 0 and y < 0:
        return 180
    elif y == 0 and x > 0:
        return 90
    elif y == 0 and x < 0:
        return 270
    else:
        pi = math.degrees(math.atan(math.fabs(x / y)))
        if x > 0 and y > 0:
            pi = pi
        elif x < 0 and y > 0:
            pi = 360 - pi
        elif x < 0 and y < 0:
            pi = 180 + pi
        elif x > 0 and y < 0:
            pi = 180 - pi
    return pi


def remove_visited(vertex):
    # this function set vertex to not visited
    for i in vertex:
        i.set_not_visited()


def remove_teken(e):
    # this function set all edges to not taken
    for i in e:
        i.set_not_taken()
        i.Sym().set_not_taken()

def bfs(start):
    # this i a breadth-first search function
    # i use this to travel in graph and return all Vertex
    explored = []
    queue = [start]

    levels = {}
    levels[start] = 0

    explored.append(start)
    while queue:
        node = queue.pop(0)
        node.V.set_visited()
        nb = neighbours(node)

        for neighbour in nb:
            if neighbour.V.visited == False:
                queue.append(neighbour)
                explored.append(neighbour)
                neighbour.V.set_visited()

                # levels[neighbour]= levels[node]+1

    # print(levels)
    return explored


def bfs_edges(start):
    # return 'main' edges in faces in the graph
    # i use the BFS algorithm in this function
    face = []
    queue = [start]
    while queue:
        node = queue.pop(0)
        node.V.set_visited()
        nb = neighbours(node)
        for neighbour in nb:
            if neighbour.V.visited == False:
                queue.append(neighbour)
            if neighbour.taken_edge == False:
                face.append(neighbour)

                neighbour.set_taken()
                eTemp = neighbour
                while True:
                    eTemp.set_taken()
                    eTemp = eTemp.Sym().NextV()
                    if eTemp == neighbour:
                        break

                neighbour.V.set_visited()
    return face


def bfs_paths(start, goal):
    # return a path betwen two vertex

    queue = [[start]]
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node.V.visited == False:
            for ng in neighbours(node):
                new_path = list(path)
                new_path.append(ng)
                queue.append(new_path)
                if ng.V.Vertex_id == goal.V.Vertex_id:
                    return new_path
            node.V.set_visited()
    return "nie ma drogi"



def reading_base():
    base=db.Data_base()
    base.creating_table()
    for i in V:
        base.add_vertex(i.getxy()[0],i.getxy()[1])
    turtle.done()
    for i in edges:
        base.adding_edge(i.V.Vertex_id,i.Sym().V.Vertex_id)

    base.read_data()
    return V, edges
def drawing(V):
    # just a simple drawing function
    for i in V:
        turtle.penup()
        turtle.goto(i.getxy())
        turtle.dot()
        turtle.goto(i.getxy()[0] + 15, i.getxy()[1])
        turtle.write(i.Vertex_id)
        turtle.goto(i.getxy()[0] + 15, i.getxy()[1] - 10)
        turtle.color("red")
        turtle.write(i.distance)
        turtle.color("black")
def draw_path(x):
    temp=[]
    for i in x:
        for j in V:
            if j.Vertex_id==i:
                temp.append(j)
    for z in range(len(temp)-1):
        turtle.penup()
        turtle.goto(temp[z].getxy())
        turtle.pendown()
        turtle.pensize(5)
        turtle.color("orange")
        turtle.goto(temp[z+1].getxy())


if __name__ == '__main__':

    edges, V=get_data()
    fs = Fast_splice(edges)



    remove_visited(V)
    path_d = reconstruct_path(dijkstra(edges[0].Sym(), edges[5]), edges[0].Sym().V.Vertex_id, edges[5].V.Vertex_id)
    remove_visited(V)
    path_a = reconstruct_path(a_star( edges[0].Sym(), edges[5]), edges[0].Sym().V.Vertex_id, edges[5].V.Vertex_id)

    print (edges[0].Sym().V.Vertex_id)
    print(edges[5].V.Vertex_id)
    print("Droga algorymem Dijkstry:", path_d)

    print("Droga algorymem A*:" ,path_a)

    turtle.tracer(0)
    for i in edges:
        turtle.penup()
        turtle.goto(i.V.getxy())
        turtle.pendown()
        turtle.goto(i.Sym().V.getxy())
    drawing(V)
    draw_path(path_a)
    turtle.tracer(1)
    turtle.tracer(0)
    turtle.done()