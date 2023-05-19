import random
import math
import copy
import networkx as nx
import igraph
from sklearn.metrics import adjusted_mutual_info_score


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

def temperature_met(current_temperature, final_temperature):
    return current_temperature <= final_temperature


# 设置模拟退火算法的参数
initial_temperature = 100
final_temperature = 1
cooling_rate = 0.95
num_iterations = 100

# G = nx.karate_club_graph()

path = '../biyesheji/data/er300.txt'
G = nx.Graph()
with open(path) as file:
    for line in file:
        head, tail = [int(x) for x in line.split(' ')]
        G.add_edge(head, tail)
print(G)
k = int(len(G.edges)*0.05)
print(k)

# 进行社团划分
comm = nx.community.greedy_modularity_communities(G)

# 创建一个字典，将每个节点与其所属的社团标签关联起来
node_colors = {}
for i, c in enumerate(comm):
    for node in c:
        node_colors[node] = i

# 创建一个列表，用于存储每个社团内部的边
internal_edges = []

# 创建一个列表，用于存储社团之间的边
external_edges = []

# 迭代每个社团，找到社团内部的边
for c in comm:
    edges = G.subgraph(c).edges()
    internal_edges.extend(edges)
print("内部连边数量：", len(internal_edges))

# 遍历网络的边，找到社团之间的边
for edge in G.edges():
    u, v = edge
    u_comm = node_colors[u]
    v_comm = node_colors[v]
    if u_comm != v_comm:
        external_edges.append(edge)
print("外部连边数量：", len(external_edges))

# 构建修改后的网络
modified_G = G.copy()

# 原网络的社团划分
# networkx->igraph
G_ = copy.deepcopy(G)
e_ = list(G_.edges)
Adjacency_List = get_adj_list(e_)
# specify nodes in the network
num_vertices = G_.number_of_nodes()
IG_edgeList = []
for i in e_:
    IG_edgeList.append((i[0], i[1]))
# print(IG_edgeList)
g_copy = igraph.Graph(directed=False)
g_copy.add_vertices(num_vertices)
g_copy.add_edges(IG_edgeList)
origin_comm = g_copy.community_multilevel()

# 开始模拟退火算法
current_temperature = initial_temperature
current_comm = copy.deepcopy(comm)

for iteration in range(num_iterations):
    # 随机选择并删除5条社团内连边
    modified_G_copy = copy.deepcopy(modified_G)
    internal_edges_copy = copy.deepcopy(internal_edges)
    rem_edges = random.sample(internal_edges_copy, k)
    print(rem_edges)
    for i in rem_edges:
        modified_G_copy.remove_edges_from([i])

    # 随机选择并添加5条社团之间连边
    external_edges_copy = copy.deepcopy(external_edges)
    add_edges = random.sample(external_edges_copy, k)
    for i in add_edges:
        modified_G_copy.add_edges_from([i])

    # networkx->igraph
    G_modified = copy.deepcopy(modified_G_copy)
    e_ = list(G_modified.edges)
    Adjacency_List = get_adj_list(e_)
    # specify nodes in the network
    num_vertices = G_modified.number_of_nodes()
    IG_edgeList = []
    for i in e_:
        IG_edgeList.append((i[0], i[1]))
    # print(IG_edgeList)
    modified_g_copy = igraph.Graph(directed=False)
    modified_g_copy.add_vertices(num_vertices)
    modified_g_copy.add_edges(IG_edgeList)
    # 进行修改后的网络的社团划分
    modified_comm_copy = modified_g_copy.community_multilevel()

    # 计算当前网络社团划分与修改后网络社团划分之间的NMI
    best_nmi = igraph.compare_communities(origin_comm, modified_comm_copy, method="nmi")
    print("first NMI:", best_nmi)

    # 把修改的图还原
    for i in rem_edges:
        modified_G_copy.add_edges_from([i])
    for i in add_edges:
        modified_G_copy.remove_edges_from([i])
    # 把修改的图还原

    # 温度终止条件
    current_temperature = initial_temperature
    while not temperature_met(current_temperature, final_temperature):
        # 降低温度
        current_temperature *= cooling_rate

        for j in range(0,10):
            index = random.randint(0, len(rem_edges) - 1)
            random_element = random.choice(internal_edges_copy)
            rem_edges[index] = random_element

            index = random.randint(0, len(add_edges) - 1)
            random_element = random.choice(external_edges_copy)
            add_edges[index] = random_element

            for i in rem_edges:
                modified_G_copy.remove_edges_from([i])
            for i in add_edges:
                modified_G_copy.add_edges_from([i])

            # networkx->igraph
            G_modified = copy.deepcopy(modified_G_copy)
            e_ = list(G_modified.edges)
            Adjacency_List = get_adj_list(e_)
            # specify nodes in the network
            num_vertices = G_modified.number_of_nodes()
            IG_edgeList = []
            for i in e_:
                IG_edgeList.append((i[0], i[1]))
            # print(IG_edgeList)
            modified_g_copy = igraph.Graph(directed=False)
            modified_g_copy.add_vertices(num_vertices)
            modified_g_copy.add_edges(IG_edgeList)
            # 进行修改后的网络的社团划分
            modified_comm_copy = modified_g_copy.community_multilevel()

            # 计算当前网络社团划分与修改后网络社团划分之间的NMI
            current_nmi = igraph.compare_communities(origin_comm, modified_comm_copy, method="nmi")
            # print("current NMI:", current_nmi)

            # 判断是否接受更优的解
            if current_nmi-best_nmi <0:
                best_nmi = current_nmi
            elif random.random() < math.exp(-(current_nmi-best_nmi) / current_temperature):
                best_nmi = current_nmi

            # 把修改的图还原
            for i in rem_edges:
                modified_G_copy.add_edges_from([i])
            for i in add_edges:
                modified_G_copy.remove_edges_from([i])
            # 把修改的图还原



    # 输出当前迭代次数和当前最优NMI值
    print(f"Iteration: {iteration + 1}/{num_iterations}, Best NMI: {best_nmi}")
