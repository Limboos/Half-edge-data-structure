from random import randint
from math import atan2
import turtle

class Punkt(object):
    def __init__(self,x,y):
        self.__x = x
        self.__y = y
    def getxy(self):
        return (self.__x,self.__y)
    def rysuj(self):
        turtle.penup()
        turtle.goto(self.__x,self.__y)
        turtle.dot()

class Wektor(object):
    def __init__(self,p1,p2):
        self.p1=p1
        self.p2=p2
    def rysuj(self):
        turtle.goto(self.p1.getxy())
        turtle.pendown()
        turtle.goto(self.p2.getxy())


def list_of_points(n):
    l=[]
    for i in n:
        l.append(Punkt(i.V.getxy()[0],i.V.getxy()[1]))
    return l
def quicksort(a):
    if len(a)<=1: return a
    pivolt=angel(a[randint(0,len(a)-1)])
    small, eq, larger=[],[],[]
    for i in a:
        ange=angel(i)
        if ange<pivolt:
            small.append(i)
        elif ange==pivolt:
            eq.append(i)
        else:
            larger.append(i)
    return quicksort(small)+sorted(eq,key=distance)+quicksort(larger)
def angel(p0,p1=None):
    global root
    if p1==None: p1=root
    x_dis = p0.getxy()[0] - p1.getxy()[0]
    y_dis = p0.getxy()[1] - p1.getxy()[1]
    return atan2(y_dis,x_dis)

def distance(p0,p1=None):
    global root
    if p1==None: p1=root
    x_dis = p0.getxy()[0] - p1.getxy()[0]
    y_dis = p0.getxy()[1] - p1.getxy()[1]
    return y_dis**2+x_dis**2

def det(p1,p2,p3):
    p1 = p1.getxy()
    p2 = p2.getxy()
    p3 = p3.getxy()
    return (p2[0]-p1[0])*(p3[1]-p1[1]) -(p2[1]-p1[1])*(p3[0]-p1[0])


def graham(points):
    global root
    min = 0
    for i in points:  # zwraca punkt z najmniejsza wpsółrzędna X
        if i.getxy()[1] < min:
            root = i
            min = i.getxy()[1]
    sorted_pts=quicksort(points)
    del sorted_pts[sorted_pts.index(root)]
    gl=[root,sorted_pts[0]]
    for s in sorted_pts[1:]:
            while det(gl[-2],gl[-1],s)<=0:
                del gl[-1]

            gl.append(s)
    return gl

def main(point):
    #turtle.tracer(0)
    l=list_of_points(point)
    root=l[1]
    g=graham(l)
    point_with_cord=[]
    for cord in g:
        point_with_cord.append(cord.getxy())

    return point_with_cord

