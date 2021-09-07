import math


# TODO
#clean this shit
#update drawing labirary to MathPlotLib


class Vertex(object):
    # this class create Vertex
    count = 1

    def __init__(self, x, y, z=0):
        self.Vertex_id = Vertex.count
        Vertex.count += 1
        self.__x = x
        self.__y = y
        self.__z = z
        self.visited = False
        self.distance = None

    def set_visited(self):
        self.visited = True

    def set_not_visited(self):
        self.visited = False

    def getxy(self):
        return self.__x, self.__y

    def set_distance(self, dis):
        self.distance = dis

    def __iter__(self):
        return [self.__x, self.__y].__iter__()

    def __del__(self):
        print("deleted")

class HalfEdge(object):

    count = 1

    def __init__(self):
        self.id = HalfEdge.count
        HalfEdge.count += 1
        self.V = None
        self.S = None
        self.N = None
        self.taken_edge = False
        self.weight = None

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
    #he1.weight=round(math.sqrt((math.pow((V1.getxy()[0] - V2.getxy()[0]),2) + math.pow((V1.getxy()[1] - V2.getxy()[1]),2))),0)
    #he2.weight=round(math.sqrt((math.pow((V2.getxy()[0] - V1.getxy()[0]),2) + math.pow((V2.getxy()[1] - V1.getxy()[1]),2))),0)
    return he1


def Splice(e1, e2):
    # this function connect  the edges
    # allow me to navigate in the structure
    temp = e1.N
    e1.N = e2.N
    e2.N = temp
