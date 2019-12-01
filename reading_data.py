from HALF_EDGE.Half_Edge_DS import *
from HALF_EDGE.half_edge import *
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
    with open("graph6.obj", "w") as file:
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

    with open("graph6.obj", 'r') as file:
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
    with open("graph5.obj", 'r') as file:
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


def creating_graph(faces, V):
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

def get_data():
    V,faces = reading_file()
    edges = creating_graph(faces,V)
    return edges, V