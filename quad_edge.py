import turtle,  math
import numpy as np


#TODO
#class Quad_edge
#class Vertex
#class Face ???????????



class Vertex(object):
    count = 1

    def __init__(self, x, y, z=1):
        self.Vertex_id = Vertex.count
        Vertex.count += 1
        self.__x = x
        self.__y = y
        self.__z = z

    def getxy(self):
        return self.__x, self.__y
    def getxyz(self):
        return self.__x, self.__y, self.__z

class Face(object):
    def __init__(self):
        self.face = None

    def calculateface(self,p1,p2,p3):
        x=(p1.getxy()[0]+p2.getxy()[0]+p3.getxy()[0])/3
        y=(p1.getxy()[1]+p2.getxy()[1]+p3.getxy()[1])/3
        return x,y



class Quad_edge(object):
    def __init__(self):
        self.V = None
        self.S = None
        self.N = None
        self.R = None

    def Sym(self):
        return self.S

    def NextV(self):
        return self.N
    def NextInTri(self):
        return self.R.R.R.N.R
    def NextR(self):
        return self.R.N
    def next_in(self):
        return self.S.N

def MakeEdge(V1, V2):
    qe1 = Quad_edge()
    qe2 = Quad_edge()
    qe3 = Quad_edge()
    qe4 = Quad_edge()
    qe1.V = V1
    qe1.R = qe2
    qe1.S = qe3
    qe1.N = qe1
    qe3.V = V2
    qe3.R = qe4
    qe3.S = qe1
    qe3.N = qe3
    qe2.R = qe3
    qe4.R = qe1
    DV1=DV2=None
    qe2.V = DV1
    qe4.V = DV2
    return qe1


def Splice(e1, e2):
    # this function connect to the edges
    # allow me to navigate in the structure
    temp1=e1.R.R.R
    e1.R.N=e2.R.R.R
    e2.R.N=temp1
    temp = e1.N
    e1.N = e2.N
    e2.N = temp




if __name__ == '__main__':
    v=[]
    v.append(Vertex(10,100))
    v.append(Vertex(10,-100))
    v.append(Vertex(200,200))
    v.append(Vertex(70,50))
    for i in v:
        turtle.penup()
        turtle.goto(i.getxy())
        turtle.dot()
        turtle.goto(i.getxy()[0]+10,i.getxy()[1]+10)
        turtle.write(i.Vertex_id)
    e=[]

    x=Delunay()
    for i in v:
        e.append(x.AddPoint(i))

    for i in e:
        turtle.goto(i.V.getxy())
        turtle.pendown()
        turtle.goto(i.Sym().V.getxy())
        turtle.penup()
    turtle.done()





