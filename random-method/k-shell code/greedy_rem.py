import networkx as nx
import xlwt
from collections import defaultdict
import scipy.stats
from copy import deepcopy

# 该函数为k-shell分解算法
def k_shell(graph_copy):
    graph = nx.Graph(graph_copy)  # 复制一个图
    importance_dict = defaultdict(list)
    k = 1  # 初始k值
    while len(graph.degree):  # 返回节点的个数
        while True:
            level_node_list = []
            for item in graph.degree:  # 列表元祖，元组前面是节点编号，后面是节点的度
                if item[1] <= k:
                    level_node_list.append(item[0])
            graph.remove_nodes_from(level_node_list)
            importance_dict[k].extend(level_node_list)
            if not len(graph.degree):
                return importance_dict
            if min(graph.degree, key=lambda x: x[1])[1] > k:
                break
        k = min(graph.degree, key=lambda x: x[1])[1]
    return importance_dict

def accuracy(k_distribution_original, k_distribution):
    acc_absolute = 0
    node_number = 0
    for key in sorted(k_distribution.keys()):
        if k_distribution[key] < k_distribution_original[key]:
            acc_absolute = acc_absolute + 1  # 精度的位置放在哪里是个关键

    node_number = node_number + len(k_distribution)

    print(acc_absolute)
    print(node_number)

    asr = acc_absolute / node_number
    return asr

if __name__ == "__main__":
    for var in [100]:
        # 打开txt文件
        filename = '../data/usair.txt'
        G = nx.Graph()
        with open(filename) as file:
            for line in file:
                head, tail = [int(x) for x in line.split(' ')]
                G.add_edge(head, tail)
        print(G)
        all_edges = deepcopy(G.edges)
        # 计算K-shell
        k = k_shell(G)
        # print(dict(k))
        k = {value: key for key, values in dict(k).items() for value in values}
        # print(k)
        # for v in G.nodes():
        #     print(v, k[v])



        # 删除度值之和最大的边
        deg = []
        for edge in G.edges:
            deg.append(G.degree(edge[0]) + G.degree(edge[1]))
        # print(deg)
        edges = list(zip(G.edges, deg))
        edges = sorted(edges, key=lambda x: (x[1], x[0]))
        # 先按 x[1] 进行排序，若 x[1] 相同，再按照 x[0] 排序
        edges = zip(*edges)
        x_axis, y_axis = [list(x) for x in edges]
        # print(x_axis)
        G.remove_edges_from(x_axis[-var:])
        print(G)

        # 计算K-shell
        k_ = k_shell(G)
        # print(dict(k_))
        k_ = {value: key for key, values in dict(k_).items() for value in values}
        # print(k_)
        # for v in G.nodes():
        #     print(v, k_[v])

        asr = accuracy(k, k_)
        lcr = var / len(all_edges)
        print("asr:", asr)
        print("lcr:", lcr)
