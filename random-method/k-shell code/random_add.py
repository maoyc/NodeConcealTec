import pickle
import networkx as nx
import matplotlib.pyplot as plt
import scipy as sp
import random
import xlwt
from collections import defaultdict
import time
import scipy.stats
from copy import deepcopy


def add_and_remove_edges(G, p_new_connection, p_remove_connection):
    '''
    for each node,
      add a new connection to random other node, with prob p_new_connection,
      remove a connection, with prob p_remove_connection

    operates on G in-place
    '''
    new_edges = []
    rem_edges = []

    for node in G.nodes():
        # find the other nodes this one is connected to
        connected = [to for (fr, to) in G.edges(node)]
        # and find the remainder of nodes, which are candidates for new edges
        unconnected = [n for n in G.nodes() if not n in connected]

        # probabilistically add a random edge
        if len(unconnected):  # only try if new edge is possible
            if random.random() < p_new_connection:
                new = random.choice(unconnected)
                # G.add_edge(node, new)
                # print("\tnew edge:\t {} -- {}".format(node, new))
                new_edges.append((node, new))
                # book-keeping, in case both add and remove done in same cycle
                unconnected.remove(new)
                connected.append(new)

                # probabilistically remove a random edge
        if len(connected):  # only try if an edge exists to remove
            if random.random() < p_remove_connection:
                remove = random.choice(connected)
                # G.remove_edge(node, remove)
                # print("\tedge removed:\t {} -- {}".format(node, remove))
                rem_edges.append((node, remove))
                # book-keeping, in case lists are important later?
                connected.remove(remove)
                unconnected.append(remove)
    return new_edges, rem_edges


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

# k-shell的分解精度,该返回值越大，则攻击效果越差
def accuracy(k_distribution_original, k_distribution):
    acc_absolute = 0
    node_number = 0
    for key in sorted(k_distribution.keys()):
        if k_distribution[key] < k_distribution_original[key]:
            acc_absolute = acc_absolute + 1  # 精度的位置放在哪里是个关键

    node_number = node_number + len(k_distribution)
    asr = acc_absolute / node_number
    return asr

if __name__ == "__main__":
    m = 0
    asr_ls=[]
    lcr_ls=[]
    # 创建Workbook,相当于创建Excel
    xls = xlwt.Workbook(encoding='utf-8')
    # 创建sheet，Sheet1为表的名字，cell_overwrite_ok为是否覆盖单元格
    sheet = xls.add_sheet('sheet1', cell_overwrite_ok=False)
    for var in [0.1]:
        # 打开txt文件
        filename = '../data/ws300.txt'
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
        print(k)
        # for v in G.nodes():
        #     print(v, k[v])



        # 进行网络操作，删边、重连、加边
        print("before", G)
        new_edges, rem_edges = add_and_remove_edges(G, var, var)#0.4/0.6/0.8/1
        print("add edges num:", len(new_edges))
        print("del edges num:", len(rem_edges))
        G.add_edges_from(new_edges)
        G.remove_edges_from(rem_edges)
        print("after", G)
        print(list(nx.connected_components(G)))
        nx.draw_networkx(G,node_size = 30, with_labels = False)
        # plt.show()


        # 计算K-shell
        k_ = k_shell(G)
        # print(dict(k_))
        k_ = {value: key for key, values in dict(k_).items() for value in values}
        print(k_)
        # for v in G.nodes():
        #     print(v, k_[v])

        asr = accuracy(k,k_)
        lcr = (len(new_edges)+len(rem_edges))/len(all_edges)
        print("asr:",asr)
        print("lcr:",lcr)
        asr_ls.append(asr)
        lcr_ls.append(lcr)



        # 创建的文件夹，用来写入处理后的数据
        file = r"C:\Users\hello\Desktop\k-shell隐匿\er300_random_rew.xls"
        # 向表中添加数据

        sheet.write(0, m, lcr_ls[m])
        sheet.write(1, m, asr_ls[m])
        m+=1

        # 保存到excel中
        # xls.save(file)