import numpy as np

#from HALF_EDGE.GUI import *
from HALF_EDGE.Turtle_drawing import *
from HALF_EDGE.half_edge import *


# TODO


class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


def BigTri(v):
    tri = []
    e = []
    x = v.getxy()[0]
    y = v.getxy()[1]
    tri.append(Vertex(x - 5000, y - 5000))
    tri.append(Vertex(x + 5000, y - 5000))
    tri.append(Vertex((x + x) / 2, y + 5000))
    e.append(MakeEdge(tri[0], tri[1]))
    e.append(MakeEdge(tri[1], tri[2]))
    e.append(MakeEdge(tri[2], tri[0]))
    Splice(e[0], e[2].Sym())
    Splice(e[1], e[0].Sym())
    Splice(e[2], e[1].Sym())
    return e


def Circlecenter(tri):
    pts = np.asarray([v.getxy() for v in tri])
    pts2 = np.dot(pts, pts.T)
    A = np.bmat([[2 * pts2, [[1],
                             [1],
                             [1]]],
                 [[[1, 1, 1, 0]]]])

    b = np.hstack((np.sum(pts * pts, axis=1), [1]))
    x = np.linalg.solve(A, b)
    bary_coords = x[:-1]
    center = np.dot(bary_coords, pts)
    center[0] = round(center[0], 0)
    center[1] = round(center[1], 0)
    radius = np.sum(np.square(pts[0] - center))  # squared distance
    return (center, radius)


def ExportData(v):
    x_cordinate = []
    y_cordinate = []
    x_cordinate.append(i.getxy()[0])
    y_cordinate.append(i.getxy()[1])
    return x_cordinate, y_cordinate


def Quicksort(l):
    if len(l) <= 1: return l
    pivolt = l[random.randint(0, len(l) - 1)]
    small, eq, larger = [], [], []
    for i in l:
        dis = i
        if dis < pivolt:
            small.append(i)
        elif dis == pivolt:
            eq.append(i)
        else:
            larger.append(i)
    return Quicksort(small) + eq + Quicksort(larger)


def InCircleFast(tri, p):
    """Check if point p is inside of precomputed circumcircle of tri.
    """
    center, radius = Circlecenter(tri)
    return np.sum(np.square(center - p.getxy())) <= radius


def RemoveSplice(t1, t2, t3):
    Splice(t1, t2)
    Splice(t3.Sym(), t2.Sym())
    Splice(t1.Sym(), t2)


def NewEdges(x, p):
    e = []
    e.append(MakeEdge(x.V, p))
    e.append(MakeEdge(x.NextV().Sym().V, p))
    e.append(MakeEdge(x.N.S.N.S.V, p))
    return e


def Newconection(x, e):
    temp = x.NextV()
    Splice(x, temp)
    Splice(x, e)
    Splice(e, temp)


def SplitingTheTri(x, p):
    e = NewEdges(x, p)
    t = x.N.S
    t1 = x.N.S.N.S
    '''
    print("=-----")
    print("MAIN EDGE: ", x.V.Vertex_id, x.S.V.Vertex_id)
    print("SPLITING THE TRIANGLE")

    print(x.V.Vertex_id, x.S.V.Vertex_id, "||", e[0].V.Vertex_id, e[0].S.V.Vertex_id)
    print(t1.V.Vertex_id, t1.S.V.Vertex_id, "||", e[2].V.Vertex_id, e[2].S.V.Vertex_id)
    print(t.V.Vertex_id, t.S.V.Vertex_id, "||", e[1].V.Vertex_id, e[1].S.V.Vertex_id)
    print(e[1].S.V.Vertex_id, e[1].S.S.V.Vertex_id, "||", e[0].S.V.Vertex_id, e[0].S.S.V.Vertex_id)
    print(e[2].S.V.Vertex_id, e[0].S.S.V.Vertex_id, "||", e[2].S.V.Vertex_id, e[2].S.S.V.Vertex_id)
    print("--------")
    '''
    Newconection(x, e[0])
    Newconection(t1, e[2])
    Newconection(t, e[1])
    Splice(e[1].S, e[0].S)
    Splice(e[0].S, e[2].S)
    return e


def Flip(x, p):
    for i in neighbours(x):
        if i.V.Vertex_id == p.Vertex_id:
            temp = x.N
            temp1 = x.N.S.N.S
            temp2 = x.S.N
            temp3 = x.S.N.S.N.S
            Splice(temp3, x)
            # Splice(x, temp)
            Splice(temp.S, temp1.S)
            Splice(temp1, x.S)
            # Splice(x.S, temp2)
            Splice(temp2.S, temp3.S)
            del x

            e = MakeEdge(temp.S.V, temp3.S.V)
            Splice(temp2.S, e.S)
            Splice(e.S, temp3.S)
            Splice(temp.S, e)
            Splice(e, temp1.S)

            return e, temp2.S, temp3
        else:
            pass


def R(p, p1, p2):
    px = p.getxy()[0]
    py = p.getxy()[1]
    p1x = p1.V.getxy()[0]
    p1y = p1.V.getxy()[1]
    p2x = p2.V.getxy()[0]
    p2y = p2.V.getxy()[1]
    x = np.linalg.det([[px, py, 1],
                       [p1x, p1y, 1],
                       [p2x, p2y, 1]])
    return x


def CCW(p, p1, p2):
    px = p.V.getxy()[0]
    py = p.V.getxy()[1]
    p1x = p1.V.getxy()[0]
    p1y = p1.V.getxy()[1]
    p2x = p2.V.getxy()[0]
    p2y = p2.V.getxy()[1]
    x = np.linalg.det([[px, py, 1],
                       [p1x, p1y, 1],
                       [p2x, p2y, 1]])
    return x


def Point_inside_tri(e, p):
    if int(R(p, e.S, e.N.S)) >= 0 and int(R(p, e.N.S, e)) >= 0 and int(R(p, e, e.S)) >= 0:
        return e
    else:
        return e.S


def WalkingInTri(e, p, con):
    while True:
        if int(R(p, e.S, e.N.S)) >= 0 and int(R(p, e.N.S, e)) >= 0 and int(R(p, e, e.S)) >= 0:
            if p.Vertex_id >= 2 and e.N.S.V.getxy() in con and e.V.getxy() in con and e.S.V.getxy() in con:
                e = e.N
            else:
                return e.N.S, e, e.N.S.N.S
        elif int(R(p, e.S, e.N.S)) <= 0 and int(R(p, e.N.S, e)) <= 0 and int(R(p, e, e.S)) <= 0:
            e = e.S
        elif R(p, e.S, e.N.S) < 0:
            e = e.N.S.N
        elif R(p, e.N.S, e) < 0:
            e = e.N
        elif R(p, e, e.S) < 0:
            e = e.S


def Delauny(point, edge):
    # print(" VERTEX NR:", point.Vertex_id)
    bad_triangles = WalkingInTri(edge[-1], point, tri)
    stack = Stack()
    for i in bad_triangles:
        stack.push(i)
    del edge
    edge = []
    s = SplitingTheTri(bad_triangles[0], point)
    for k in s:
        edge.append(k)
    while stack.size() != 0:
        temp = stack.pop()
        # print(temp.V.Vertex_id, temp.S.V.Vertex_id)
        # print(temp.V.Vertex_id, point.Vertex_id, temp.Sym().V.Vertex_id,
        # Point_inside_tri(temp, point).S.N.S.V.Vertex_id)
        if InCircleFast([temp.V, point, temp.Sym().V], Point_inside_tri(temp, point).S.N.S.V):
            f = Flip(temp, point)
            # print("PUSH")
            # print(f[1].V.Vertex_id, f[1].S.V.Vertex_id)
            # print(f[2].V.Vertex_id, f[2].S.V.Vertex_id)
            del temp

            stack.push(f[1])
            stack.push(f[2])
            edge.append(f[0])

        else:
            pass
    return edge


def ReturnVertex(v):
    return v


def DrawDT(drawing_points):
    t._tracer(0)
    # Function for drawing the whole DT
    for vert in drawing_points:
        for i in neighbours(vert):
            turtle.penup()
            turtle.goto(i.V.getxy()[0] + 15, i.V.getxy()[1])
            turtle.write(i.V.Vertex_id)
            turtle.goto(i.V.getxy())
            turtle.pendown()
            turtle.goto(i.Sym().V.getxy())
            turtle.penup()
            turtle.goto(i.Sym().V.getxy()[0] + 15, i.Sym().V.getxy()[1])
            turtle.write(i.Sym().V.Vertex_id)


def DeletingLine():
    global drawing_edge
    global taken_edge
    Turtle_drawingline(taken_edge, "white", 5)
    Turtle_drawingline(taken_edge, "black", 1)
    taken_edge = None


def Turtle_drawingline(edge, color, width):
    t.penup()
    t.pensize(width)
    t.pencolor(color)
    t.goto(edge.V.getxy())
    t.pendown()
    t.goto(edge.S.V.getxy())
    t.penup()
    t.pensize(1)


def DrawingLine():
    global drawing_edge
    global taken_edge
    if taken_edge != None:
        DeletingLine()
    taken_edge = drawing_edge
    drawing_edge = None
    Turtle_drawingline(taken_edge, "brown", 5)


def NextEdge():
    global taken_edge
    global drawing_edge
    if taken_edge == None:
        pass
    drawing_edge = taken_edge.N
    DrawingLine()


def PrevEdge():
    global taken_edge
    global drawing_edge
    if taken_edge == None:
        pass
    drawing_edge = taken_edge.S.N.S.N.S
    DrawingLine()


def SymEdge():
    global taken_edge
    global drawing_edge
    if taken_edge == None:
        pass
    drawing_edge =taken_edge.S
    DrawingLine()
def ExitScrean():
    turtle.bye()


def distance(point, coef):
    return abs((coef[0] * point[0]) - point[1] + coef[1]) / math.sqrt((coef[0] * coef[0]) + 1)


def DistanceFrom(e, point):
    distance = np.linalg.norm(np.cross(np.array(e[0].S.V.getxy()) - np.array(e[0].V.getxy()),
                                       np.array(e[0].V.getxy()) - np.array(point.getxy()))) / np.linalg.norm(
        np.array(e[0].S.V.getxy()) - np.array(e[0].V.getxy()))
    distance1 = np.linalg.norm(np.cross(np.array(e[1].S.V.getxy()) - np.array(e[1].V.getxy()),
                                        np.array(e[1].V.getxy()) - np.array(point.getxy()))) / np.linalg.norm(
        np.array(e[1].S.V.getxy()) - np.array(e[1].V.getxy()))
    distance2 = np.linalg.norm(np.cross(np.array(e[2].S.V.getxy()) - np.array(e[2].V.getxy()),
                                        np.array(e[2].V.getxy()) - np.array(point.getxy()))) / np.linalg.norm(
        np.array(e[2].S.V.getxy()) - np.array(e[2].V.getxy()))

    if distance < distance1 and distance < distance2:
        return e[0]
    elif distance1 < distance and distance1 < distance2:
        return e[1]
    elif distance2 < distance1 and distance2 < distance:
        return e[2]


def ClickOnEdge(x, y):
    # Findning the nearest line to the position where you click
    global drawing_edge
    global taken_edge
    global main_edge
    point = Vertex(x, y)
    if taken_edge != None:
        turtle.resetscreen()
        remove_teken(edges)
        remove_visited(vertex)
        drawing_points = bfs(taken_edge)
        DrawDT(drawing_points)
        taken_edge = None
    searching_tri = WalkingInTri(main_edge, point, tri)
    drawing_edge = DistanceFrom(searching_tri, point)
    DrawingLine()



def AddPoint(x, y):
    global edges
    global vertex
    global taken_edge
    vertex.append(Vertex(x, y))

    et = Delauny(vertex[-1], edges)
    for ez in et:
        edges.append(ez)
    turtle.resetscreen()
    remove_teken(edges)
    remove_visited(vertex)
    drawing_points = bfs(edges[-1])
    DrawDT(drawing_points)
    # NIE DZIAŁA DODAWANIE PUNKTU, COS NIE TAK Z bfs


if __name__ == '__main__':
    global drawing_edge
    global taken_edge
    global main_edge
    global drawing_points
    global vertex
    global edges
    vertex = []
    vertex.append(Vertex(20, 50))
    vertex.append(Vertex(120, 80))
    vertex.append(Vertex(100, 220))
    vertex.append(Vertex(300, 250))
    vertex.append(Vertex(200, 25))
    # for i in range(100):
    #    vertex.append(Vertex(random.randint(-300, 300), random.randint(-300, 300)))

    edges = []
    global tri
    tri = BigTri(vertex[0])

    for edg in tri:
        edges.append(edg)
    # print(R(vertex[0], edges[0], edges[0].Sym()))
    for element in range(len(tri)):
        tri[element] = tri[element].V.getxy()
    for j in vertex:
        et = Delauny(j, edges)
        for ez in et:
            edges.append(ez)
    drawing_points = bfs(edges[-1])
    print(len(drawing_points))
    turtle.tracer(0)

    '''
    
    # a=Circlecenter([vertex[0],vertex[1],vertex[2]])
    turtle.tracer(1)
    turtle.tracer(0)
    turtle.done()
    # main(vertex)
    '''
    #        del edge

    main_edge = edges[0]
    drawing_edge = None
    taken_edge = None
    t = turtle.Turtle()
    t.speed(0)
    DrawDT(drawing_points)

    turtle.onkey(NextEdge, 'w')

    turtle.onkey(PrevEdge, 'e')

    turtle.onkey(SymEdge, 's')

    turtle.onkey(ExitScrean, 'q')

    turtle.onscreenclick(ClickOnEdge, 1)

    turtle.onscreenclick(AddPoint, 3)

    turtle.listen()

    turtle.mainloop()

