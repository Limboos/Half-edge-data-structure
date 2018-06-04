import turtle, math, random
import data_base as db
from collections import defaultdict
from heapq import *



# TODO
# improve djikstra algorithm
# add weight to HalEdge Class
class Vertex(object):
    # this class create Vertex
    count = 1

    def __init__(self, x, y):
        self.Vertex_id = Vertex.count
        Vertex.count += 1
        self.__x = x
        self.__y = y
        self.visited = False

    def set_visited(self):
        self.visited = True

    def set_not_visited(self):
        self.visited = False

    def getxy(self):
        return self.__x, self.__y

    def set_distance(self, dis):
        self.distance = dis


class HalfEdge(object):
    # this class i use in my data structure
    # S- represent the other side of edge
    # V - represent the Vertex
    # N- represent the edge
    count = 1

    def __init__(self):
        self.id = HalfEdge.count
        HalfEdge.count += 1
        self.V = None
        self.S = None
        self.N = None
        self.taken_edge = False
        self.weight = random.randint(0, 8)

    def Sym(self):
        return self.S

    def NextV(self):
        return self.N

    def next_in(self):
        return self.S.N

    def set_taken(self):
        self.taken_edge = True

    def set_not_taken(self):
        self.taken_edge = False

    def get_weight(self):
        return self.weight


def MakeEdge(V1, V2):
    # with this function i can create a edge
    # one edge have two half-edges(it's a object class HalfEdge)
    he1 = HalfEdge()
    he2 = HalfEdge()
    he1.V = V1
    he1.S = he2
    he1.N = he1
    he2.V = V2
    he2.S = he1
    he2.N = he2
    return he1


def Splice(e1, e2):
    # this function connect to the edges
    # allow me to navigate in the structure
    temp = e1.N
    e1.N = e2.N
    e2.N = temp


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
            # for i in range(len(A)):
            # print(A[i][1].V.Vertex_id,A[i][1].Sym().V.Vertex_id)
            # print(A[i][0])

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




def creatign_faces(faces):
    # this function take the main edges in faces and return entire face
    f = []
    all = []
    for i in faces:
        eTemp = i
        while True:
            f.append(eTemp)
            eTemp = eTemp.Sym().NextV()
            if eTemp == i:
                break
        all.append(f)
        f = []
    return all


def saving_file(v, f):
    # just a basic function to saving in a .obj file
    l = []
    with open("graph4.obj", "w") as file:
        for i in v:
            x, y = i.V.getxy()
            x = str(x)
            y = str(y)
            file.write("v" + ' ' + x + "." + y + "\n")
            l.append(i.V)

        for z in f:
            file.write("f")
            eT = z
            while True:
                temp = l.index(eT.V) + 1
                file.write(" " + str(temp))
                eT = eT.Sym().NextV()
                if eT == z:
                    break
            file.write("\n")

    file.close()


def reading_file():
    # this function is not optimized
    # this function read a file and return all vertex and faces from file
    v_from_file = []
    faces = []

    with open("graph4.obj", 'r') as file:
        for line in file:
            if line[0] == "v":
                x, y = line[2:len(line) - 1].split(".")
                x = int(x)
                y = int(y)
                v_from_file.append(Vertex(x, y))
            elif line[0] == "f":
                faces.append(line[2:len(line) - 1].split(" "))

    file.close()
    return v_from_file, faces


def reading_my_graph():
    v = []
    e = []
    with open("graph3.obj", 'r') as file:
        for line in file:
            if line[0] == "v":
                x, y = line[2:len(line) - 1].split(".")
                x = int(x)
                y = int(y)
                v.append(Vertex(x, y))
            elif line[0] == "e":
                e.append(line[2:len(line) - 1].split("."))

    file.close()
    return v, e


def creating_graph(faces):
    # this function create a edges from the data form the file
    # i need to optimize this crap
    edges = []
    l = []
    for pol in faces:
        for j in range(len(pol) - 1):
            l.append([pol[j], pol[j + 1]])
        l.append([pol[0], pol[len(pol) - 1]])

    temp = []
    for i in l:
        try:
            if temp.index(i) == temp.index(i):
                pass
            elif temp.index(i[::-1]) == temp.index(i[::-1]):
                pass
        except Exception:
            edges.append(MakeEdge(V[int(i[0]) - 1], V[int(i[1]) - 1]))
        temp.append(i)
        temp.append(i[::-1])
    del temp
    del l
    return edges

def dijkstra(f, t):
    g = defaultdict(list)
    for l in bfs(f):
        g[l.V.Vertex_id].append((l.get_weight(),l.Sym().V.Vertex_id))
        for i in neighbours(l):
            g[i.V.Vertex_id].append((i.get_weight(),i.Sym().V.Vertex_id))
    q, seen = [(0,f.V.Vertex_id,())], set()
    while q:
        (cost,v1,path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == t.V.Vertex_id: return (cost, path)
            #print(g.get(v1.V, ()))
            for c, v2 in g.get(v1, ()):
                if v2 not in seen:
                    heappush(q, (cost+c, v2, path))

    return float("inf")


def drawing(V):
    # just a simple drawing function
    turtle.tracer(0)
    for i in V:
        turtle.penup()
        turtle.goto(i.getxy())
        turtle.dot()
        turtle.goto(i.getxy()[0] + 5, i.getxy()[1])
        turtle.write(i.Vertex_id)


if __name__ == '__main__':

    V, faces = reading_file()
    edges = creating_graph(faces)
    # V,ed=reading_my_graph()
    # for i in ed:
    # edges.append(MakeEdge(V[int(i[0])-1],V[int(i[1])-1]))
    fs = Fast_splice(edges)
    x = bfs(edges[0].Sym())
    remove_visited(V)
    #root_faces = bfs_edges(edges[0].Sym())
    remove_visited(V)
    remove_teken(edges)
    #creatign_faces(root_faces)
    # saving_file(x,root_faces)

    make_path = lambda tup: (*make_path(tup[1]), tup[0]) if tup else ()
    out = dijkstra(edges[0].Sym(), edges[7])
    if out!=type(float):
        path = make_path(out[1])
        print(path)
    else: print("nie ma drogi!")


    turtle.tracer(0)
    for i in edges:
        turtle.penup()
        turtle.goto(i.V.getxy())
        turtle.pendown()
        turtle.goto(i.Sym().V.getxy())
    # checking(edges)
    drawing(V)
    turtle.tracer(1)
    turtle.tracer(0)
    base=db.Data_base()
    base.creating_table()
    for i in V:
        base.add_vertex(i.getxy()[0],i.getxy()[1])
    turtle.done()
    for i in edges:
        base.adding_edge(i.V.Vertex_id,i.Sym().V.Vertex_id)

    base.read_data()