import turtle
import math

#TODO
#DUŻO
#djikstra
#dodac wagi
class Vertex(object):                           #klasa tworzaca wierzcholki
    count=1
    def __init__(self,x,y):
        self.Vertex_id=Vertex.count
        Vertex.count+=1
        self.__x=x
        self.__y=y
        self.visited=False
    def set_visited(self):
        self.visited=True
    def set_not_visited(self):
        self.visited=False
    def getxy(self):
        return self.__x,self.__y

class HalfEdge(object):                         #klasa tworzaca krawedzie
    count=1
    def __init__(self):
        self.id=HalfEdge.count
        HalfEdge.count+=1
        self.V=None
        self.S=None
        self.N=None
        self.taken_edge=False
    def Sym(self):
        return self.S
    def NextV(self):
        return self.N
    def next_in(self):
        return self.S.N
    def set_taken(self):
        self.taken_edge=True
    def set_not_taken(self):
        self.taken_edge=False

def MakeEdge(V1,V2):                        #funkcja tworzaca krawedzie
    he1=HalfEdge()
    he2=HalfEdge()
    he1.V=V1
    he1.S=he2
    he1.N=he1
    he2.V=V2
    he2.S=he1
    he2.N=he2
    return he1

def Splice( e1,e2):                         #funkcja ktora laczy krawedzie
    temp= e1.N
    e1.N=e2.N
    e2.N=temp

def Fast_splice(edges):
    V_id={}
    for i in edges:
        V_id.update({i.V.Vertex_id:None})               #tworze slownik, poniewaz bez tego wywala blad zwiazany z
        V_id.update({i.Sym().V.Vertex_id:None })        # brakiem danej warotsci podczas sprawdzania w nastepnej petli

    for e in edges:
        if V_id[e.V.Vertex_id]==None:
            V_id[e.V.Vertex_id]=[]
        V_id[e.V.Vertex_id].append(e)
        if V_id[e.Sym().V.Vertex_id]==None:
            V_id[e.Sym().V.Vertex_id]=[]
        V_id[e.Sym().V.Vertex_id].append(e.Sym())       #tworzenie slwonika z odpowiadajacymi krawedzami
                                                        # dla danego wierzcholka

    A=[]
    for az in V_id.values():
        for i in az:
            A.append([Azymut(i),i])                 #licze azymuty i dodaje do tablicy wraz z krawedzia
        A.sort()                                    #sortuje po azzymutach
        
        if len(A)==2:
            Splice(A[1][1],A[0][1])
        else:
            #for i in range(len(A)):               #przechodze petla po liscie z azymutami
                #print(A[i][1].V.Vertex_id,A[i][1].Sym().V.Vertex_id)
                #print(A[i][0])

            for i in range(len(A)-1):               #przechodze petla po liscie z azymutami
                Splice(A[0][1], A[i+1][1])

        A=[]                                        #kasuje zawartosc tablicy aby petla moga od nowa ja zapelnic
    return V_id

def Azymut(e):
    # zerwoy element to elemnet przy przy wierzchołku
    x=e.Sym().V.getxy()[0]-e.V.getxy()[0]
    y=e.Sym().V.getxy()[1] - e.V.getxy()[1]
    
    if x==0 and y>0:
        return 0
    elif x==0 and y<0:
        return 180
    elif y==0 and x>0:
        return 90
    elif y==0 and x<0:
        return 270
    else:
        pi = math.degrees(math.atan(math.fabs(x / y)))
        if x>0 and y>0:
            pi=pi
        elif x<0 and y>0:
            pi=360-pi
        elif x<0 and y<0:
            pi=180+pi
        elif x>0 and y<0:
            pi=180-pi
    return pi                   #licze azymut, sprawdzaja wszystkie warunki zawarte w definicji azzymutu

def remove_visited(vertex):
    #ustawia wierzcholki jako nieodwiedzone
    for i in vertex:
        i.set_not_visited()

def remove_teken(e):
    for i in e:
        i.set_not_taken()
        i.Sym().set_not_taken()

def neighbours(edges):
    l=[]
    eTemp=edges
    while True:
        l.append(eTemp.Sym())
        eTemp=eTemp.NextV()
        if eTemp==edges:
            break
    return l

def bfs(start):
    explored = []
    queue = [start]

    levels = {}                                 #dodaje poziomy oddalenia od wierzcholka
    levels[start]= 0

    explored.append(start)                      #dodaje od odwiedzonych aby na koniec zwrócic liste wszystkich wierzcholkow
    while queue:                                #nie wiem czy stosować kolejke czy bazowac na tylko strukturze
        node = queue.pop(0)                     #tworze zmienna z aktualna pozycja
        node.V.set_visited()                    #ustawiam jako odwiedzonego za pomoca zmiennej w klasie wierzcholek
        nb = neighbours(node)                   #sprawdzam sasiadow za pomoca funkcji ktora jest wyzej

        for neighbour in nb:                            #przechodze po liscie sasiadow
            if neighbour.V.visited==False:                  #jezeli nie odwiedzony to dodaje go do kolejki i ustawiam jako odwiedzony
                queue.append(neighbour)
                explored.append(neighbour)

                neighbour.V.set_visited()

                #levels[neighbour]= levels[node]+1       #zwiekszam poziom  czyli odleglosc od wierzcholka glownego


    #print(levels)
    return explored

def bfs_edges(start):
    face = []
    queue = [start]
    while queue:
        node = queue.pop(0)
        node.V.set_visited()
        nb = neighbours(node)
        for neighbour in nb:
            if neighbour.V.visited==False:
                queue.append(neighbour)
            if neighbour.taken_edge==False:
                face.append(neighbour)

                neighbour.set_taken()
                eTemp=neighbour
                while True:
                    eTemp.set_taken()
                    eTemp=eTemp.Sym().NextV()
                    if eTemp==neighbour:
                        break

                neighbour.V.set_visited()

    return face

def bfs_paths(start, goal):                      #funkcja sprawdzajaca drogi

    queue = [[start]]                         #kolejka ktora zaczyna od punktu startowego
    while queue:
        path = queue.pop(0)
        node=path[-1]
        if node.V.visited==False:                       #jezeli nieodwiedozny
            for ng in neighbours(node):                 #petla po sasiadach
                new_path=list(path)                         #tworze liste z droga
                new_path.append(ng)                         #dodaje sasiada do tej listy
                queue.append(new_path)                      #powiekszam kolejke o liste new_path
                if ng.V.Vertex_id==goal.V.Vertex_id:            #sprawdzam czy osiagnalem cel
                    return new_path
            node.V.set_visited()                            #ustawiam wierzcholek na odwiedzony
    return "nie ma drogi"

def creatign_faces(faces):
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

def saving_file(v,f):
    l=[]
    with open("graph2.obj","w") as file:
        for i in v:
            x, y = i.V.getxy()
            x = str(x)
            y = str(y)
            file.write("v"+' ' + x + "." + y + "\n")
            l.append(i.V)

        for z in f:
            file.write("f")
            eT=z
            while True:
                temp=l.index(eT.V)+1
                file.write(" "+str(temp))
                eT=eT.Sym().NextV()
                if eT==z:
                    break
            file.write("\n")

    file.close()

def reading_file():
    v_from_file = []
    faces = []

    with open("graph1.obj", 'r') as file:
        for line in file:
            if line[0] == "v":
                x, y = line[2:len(line) - 1].split(".")
                x = int(x)
                y = int(y)
                v_from_file.append(Vertex(x, y))
            elif line[0] == "f":
                faces.append(line[2:len(line) - 1].split(" "))

    file.close()
    return v_from_file,faces

def creating_graph(faces):
    edges=[]
    l=[]
    for pol in faces:
        for j in range(len(pol)-1):
            l.append([pol[j],pol[j+1]])
        l.append([pol[0],pol[len(pol)-1]])

    temp=[]
    for i in l:
        try:
            if temp.index(i)==temp.index(i):
                pass
            elif temp.index(i[::-1])==temp.index(i[::-1]):
                pass
        except Exception:
            edges.append(MakeEdge(V[int(i[0]) - 1], V[int(i[1]) - 1]))
        temp.append(i)
        temp.append(i[::-1])
    del temp
    del l
    return edges
def manual():
    V = []
    edges = []
    V.append(Vertex(1, 55))
    V.append(Vertex(1, 70))
    V.append(Vertex(50, 55))
    V.append(Vertex(50, 70))
    V.append(Vertex(1, 3))  # 4
    V.append(Vertex(-20, 35))  # 5
    V.append(Vertex(25, 110))  # 6
    V.append(Vertex(70, 60))  # 7
    V.append(Vertex(45, 10))  # 8

    edges.append(MakeEdge(V[0], V[1]))
    edges.append(MakeEdge(V[0], V[2]))
    edges.append(MakeEdge(V[0], V[4]))
    edges.append(MakeEdge(V[1], V[3]))
    edges.append(MakeEdge(V[3], V[2]))
    edges.append(MakeEdge(V[2], V[4]))
    edges.append(MakeEdge(V[5], V[0]))
    edges.append(MakeEdge(V[5], V[4]))
    edges.append(MakeEdge(V[5], V[1]))
    edges.append(MakeEdge(V[6], V[3]))
    edges.append(MakeEdge(V[6], V[1]))
    edges.append(MakeEdge(V[7], V[3]))
    edges.append(MakeEdge(V[7], V[2]))
    edges.append(MakeEdge(V[8], V[2]))
    edges.append(MakeEdge(V[8], V[4]))

    return V,edges
def drawing(V):
    turtle.tracer(0)
    for i in V:
        turtle.penup()
        turtle.goto(i.getxy())
        turtle.dot()
        turtle.goto(i.getxy()[0]+5,i.getxy()[1])
        turtle.write(i.Vertex_id)

if __name__ == '__main__':



    V,faces=reading_file()
    edges=creating_graph(faces)
    #V,edges=manual()

    fs = Fast_splice(edges)
    # print(neighbours(edges[2].Sym()))
    x = bfs(edges[0].Sym())
    remove_visited(V)
    root_faces = bfs_edges(edges[0].Sym())
    remove_visited(V)
    remove_teken(edges)
    creatign_faces(root_faces)
    #saving_file(x,root_faces)
    turtle.speed(1)
    for i in edges:
        turtle.penup()
        turtle.goto(i.V.getxy())
        turtle.pendown()
        turtle.goto(i.Sym().V.getxy())

    #checking(edges)
    drawing(V)

    turtle.done()
