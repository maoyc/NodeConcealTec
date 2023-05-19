import pickle
import networkx as nx
from igraph import *

with open('ws.pickle', 'rb') as file:  # 用with的优点是可以不用写关闭文件操作
    dict_get = pickle.load(file)
print(dict_get)
nwx = nx.Graph(dict_get)

g = Graph.from_networkx(nwx)
print(g.get_edgelist())

lst = []

v1 = g.vcount()

for x in range(g.vcount()):
    c = 0
    for y in range(0, g.vcount()):
        if g.degree(x) == g.degree(y):
            c = c + 1
        if c > 1:
            break

    if c == 1:
        lst.append(x)

print(lst)
z = g.maxdegree()

if len(lst) == 1:
    if g.degree(lst[0]) < z:
        t1 = z - g.degree(lst[0])
        print("t1",t1)
        g.add_vertices(t1)
        for j in range(v1, g.vcount()):
            g.add_edges([(lst[0], j)])

    else:
        minn1 = 100000000000000
        minn2 = 0
        for i in range(0, g.vcount()):
            if lst[0] != i:
                if g.degree(lst[0]) - g.degree(i) < minn1:
                    minn1 = g.degree(lst[0]) - g.degree(i)
                    minn2 = g.degree(i)
                    print("minn2", minn2)

        for i in range(0, g.vcount()):
            if g.degree(i) == minn2:
                t2 = z - g.degree(i)
                g.add_vertices(t2)
                for j in range(v1, g.vcount()):
                    g.add_edges([(i, j)])
                v1 = g.vcount()
else:
    maxx_degree = 0
    for i in range(0, len(lst)):
        if maxx_degree < g.degree(lst[i]):
            maxx_degree = g.degree(lst[i])
    print(maxx_degree)

    for i in range(0, len(lst)):
        if g.degree(lst[i]) != maxx_degree:
            t = maxx_degree - g.degree(lst[i])
            g.add_vertices(t)
            for j in range(v1, g.vcount()):
                g.add_edges([(lst[i], j)])
            v1 = g.vcount()

print(g.get_edgelist())
