import matplotlib.pyplot as plt
import igraph
import networkx as nx
import copy
import random

# function to create an adjacency list for the graph
def get_adj_list(E):
    Adjacency_List = {}
    for i in range(0, len(E)):
        e = E[i]
        s = e[0]
        t = e[1]
        if (s in Adjacency_List.keys()):
            Adjacency_List[s].append(t)
        else:
            Adjacency_List[s] = []
            Adjacency_List[s].append(t)
        if (t in Adjacency_List.keys()):
            Adjacency_List[t].append(s)
        else:
            Adjacency_List[t] = []
            Adjacency_List[t].append(s)
    return Adjacency_List

# G = nx.karate_club_graph()

path = '../biyesheji/data/ba300.txt'
G = nx.Graph()
with open(path) as file:
    for line in file:
        head, tail = [int(x) for x in line.split(' ')]
        G.add_edge(head, tail)
print(G)

print("Node Degree")
for v in G:
    print(f"{v:4} {G.degree(v):6}")

# nx.draw_circular(G, with_labels=True)

# networkx->igraph
G_=copy.deepcopy(G)
e_ = list(G_.edges)
Adjacency_List = get_adj_list(e_)
# specify nodes in the network
num_vertices = G_.number_of_nodes()
IG_edgeList = []
for i in e_:
    IG_edgeList.append((i[0], i[1]))
# print(IG_edgeList)
g = igraph.Graph(directed=False)
g.add_vertices(num_vertices)
g.add_edges(IG_edgeList)

# 进行社团划分
comm = nx.community.greedy_modularity_communities(G)
# comm = nx.community.louvain_communities(G, seed=1)
print(comm)

communities = g.community_multilevel()
comm_ori = copy.deepcopy(communities)

# 创建一个字典，将每个节点与其所属的社团标签关联起来
node_colors = {}
for i, c in enumerate(comm):
    for node in c:
        node_colors[node] = i

# 创建一个列表，用于存储每个社团内部的边
internal_edges = []
# 创建一个列表，用于存储社团之间的边
external_edges = []
# 创建一个列表，用于存储社团之间没有连接的节点对
disconnected_pairs = []

# 迭代每个社团，找到社团内部的边
for c in comm:
    edges = G.subgraph(c).edges()
    internal_edges.extend(edges)
# print("内部连边：", internal_edges)
print("内部连边数量：", len(internal_edges)*0.05)
pertu = int(len(internal_edges)*0.05)

# 遍历网络的边，找到社团之间的边
for edge in G.edges():
    u, v = edge
    u_comm = node_colors[u]
    v_comm = node_colors[v]
    if u_comm != v_comm:
        external_edges.append(edge)
# print("外部连边：", external_edges)

# 遍历社团列表，找到社团之间没有连接的节点对
for i in range(len(comm)):
    for j in range(i + 1, len(comm)):
        comm_i = comm[i]
        comm_j = comm[j]
        disconnected_nodes = []
        for node_i in comm_i:
            for node_j in comm_j:
                if not G.has_edge(node_i, node_j):
                    disconnected_nodes.append((node_i, node_j))
        disconnected_pairs.append(disconnected_nodes)

disconnected_pairs_ls=[]
for item in disconnected_pairs:
    for i in range(0,len(item)):
        disconnected_pairs_ls.append(item[i])
# print("未连接的外部连边：", disconnected_pairs_ls)

common_edges = []
for edge1 in internal_edges:
    for edge2 in disconnected_pairs_ls:
        if set(edge1) & set(edge2):
            common_edges.append([edge1, edge2])
print("组合[(删除,添加)]：",common_edges)

samp = random.sample(common_edges, pertu)
print("随机选择5%组连边：",samp)
for edge in samp:
    print("remove：",edge[0])
    G.remove_edges_from([edge[0]])
    print("add：",edge[1])
    G.add_edges_from([edge[1]])

# networkx->igraph
e_ = list(G.edges)
Adjacency_List = get_adj_list(e_)
# specify nodes in the network
num_vertices = G.number_of_nodes()
IG_edgeList = []
for i in e_:
    IG_edgeList.append((i[0], i[1]))
# print(IG_edgeList)
g_ = igraph.Graph(directed=False)
g_.add_vertices(num_vertices)
g_.add_edges(IG_edgeList)

communities = g_.community_multilevel()
nmi = igraph.compare_communities(comm_ori, communities, method="nmi")
print("NMI:",nmi)
# 绘制网络图形，并根据节点所属的社团进行着色
plt.figure(figsize=(8, 6))
pos = nx.spring_layout(G)
nx.draw_networkx(G, pos, node_color=[node_colors[node] for node in G.nodes()], cmap='viridis', with_labels=True)

# 绘制社团内部的边
nx.draw_networkx_edges(G, pos, edgelist=internal_edges, edge_color='red', width=2)

# 绘制社团之间的边
nx.draw_networkx_edges(G, pos, edgelist=external_edges, edge_color='blue', width=2)
plt.show()
