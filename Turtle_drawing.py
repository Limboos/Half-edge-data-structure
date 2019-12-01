import turtle
from turtle import *

from HALF_EDGE.Delauny_Triangulation import *
from HALF_EDGE.Half_Edge_DS import *
from HALF_EDGE.half_edge import *
import numpy as np


def DrawDT(drawing_points):
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

    pass


def DeletingLine():
    global drawing_edge
    global taken_edge
    Turtle_drawingline(taken_edge, "white", 5)
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
        DeletingLine(taken_edge)
    taken_edge = drawing_edge
    drawing_edge = None
    Turtle_drawingline(taken_edge, "brown", 5)


def NextEdge():
    t.setheading(90)
    t.forward(100)


def PrevEdge():
    pass





def SymEdge():
    pass


def ExitScrean():
    turtle.bye()


def DistanceFrom(e, point):
    x1, y1 = ((e[0].V.getxy()[0] + e[0].S.V.getxy()[0]) // 2), ((e[0].V.getxy()[1] + e[1].S.V.getxy()[1]) // 2)
    x2, y2 = ((e[1].V.getxy()[0] + e[1].S.V.getxy()[0]) // 2), ((e[1].V.getxy()[1] + e[1].S.V.getxy()[1]) // 2)
    x3, y3 = ((e[2].V.getxy()[0] + e[2].S.V.getxy()[0]) // 2), ((e[2].V.getxy()[1] + e[2].S.V.getxy()[1]) // 2)
    distance = math.sqrt((x1 - point.getxy()[0]) ** 2, (y1 - point.getxy()[1]) ** 2)
    distance1 = math.sqrt((x2 - point.getxy()[0]) ** 2, (y2 - point.getxy()[1]) ** 2)
    distance2 = math.sqrt((x3 - point.getxy()[0]) ** 2, (y3 - point.getxy()[1]) ** 2)
    if distance < distance1 and distance < distance2:
        return e[0]
    elif distanc1 < distance and distance1 < distance2:
        return e[1]
    elif distance2 < distance1 and distance2 < distance0:
        return e[2]

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

def ClickOnEdge(x, y):
    # Findning the nearest line to the position where you click
    global drawing_edge
    global taken_edge
    global main_edge
    point = Vertex(x, y)
    searching_tri=WalkingInTri(main_edge, point, t1)
    drawing_edge = DistanceFrom(searching_tri, point)
    DrawingLine()

    pass


def AddPoint(x, y):
    pass


def Graphicaluserinterface(e,drawing_points,t):
    global drawing_edge
    global taken_edge
    global main_edge
    global t1
    t1=t
    main_edge=e
    drawing_edge = None
    taken_edge = None
    t = turtle.Turtle()
    t.speed(0)
    DrawDT(drawing_points)

    turtle.onkey(NextEdge, 'Up')

    turtle.onkey(PrevEdge, 'Up')

    turtle.onkey(SymEdge, 'Up')

    turtle.onkey(ExitScrean, 'q')

    turtle.onscreenclick(ClickOnEdge, 1)

    turtle.onscreenclick(AddPoint, 3)

    turtle.listen()

    turtle.mainloop()
