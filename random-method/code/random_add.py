import pickle
import networkx as nx
import matplotlib.pyplot as plt
import scipy as sp
import random
import xlwt
from collections import defaultdict
import time
import scipy.stats


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


if __name__ == "__main__":
    for var in [0.1,0.2,0.3,0.4,0.5]:
        # 打开txt文件
        filename = 'data/PubMed.txt'
        G = nx.Graph()
        with open(filename) as file:
            for line in file:
                head, tail = [int(x) for x in line.split(' ')]
                G.add_edge(head, tail)
        print(G)

        # 计算K-shell
        print("k-shell")
        k = k_shell(G)
        # print(dict(k))
        k = {value: key for key, values in dict(k).items() for value in values}
        # print(k)
        # for v in G.nodes():
        #     print(v, k[v])

        # 计算PageRank
        print("PageRank")
        p = nx.pagerank(G, alpha=0.85)
        p = sorted(p.items(), key=lambda x: x[1], reverse=True)
        # 获取前三个值所对应的键
        p_top_keys = [x[0] for x in p[:10]]
        print("top_10_nodes:", p_top_keys)

        p = {k: v for k, v in p}
        p_top_0_key = list(p.keys())[0]
        p_top_0_value = list(p.values())[0]
        print("top_0:", p_top_0_key, p_top_0_value)

        p_top_9_key = list(p.keys())[9]
        p_top_9_value = list(p.values())[9]
        print("top_9:", p_top_9_key, p_top_9_value)
        # for v in G.nodes():  # 字典打印
        #     print(v, p[v])

        # 计算中介中心度
        print("Betweenness centrality")
        b = nx.betweenness_centrality(G)
        b = sorted(b.items(), key=lambda x: x[1], reverse=True)
        # 获取前三个值所对应的键
        b_top_keys = [x[0] for x in b[:10]]
        print("top_10_nodes:", b_top_keys)

        b = {k: v for k, v in b}
        b_top_0_key = list(b.keys())[0]
        b_top_0_value = list(b.values())[0]
        print("top_0:", b_top_0_key, b_top_0_value)

        b_top_9_key = list(b.keys())[9]
        b_top_9_value = list(b.values())[9]
        print("top_9:", b_top_9_key, b_top_9_value)

        # 计算度中心度
        print("Degree centrality")
        d = nx.degree_centrality(G)
        d = sorted(d.items(), key=lambda x: x[1], reverse=True)
        # 获取前三个值所对应的键
        d_top_keys = [x[0] for x in d[:10]]
        print("top_10_nodes:", d_top_keys)

        d = {k: v for k, v in d}
        d_top_0_key = list(d.keys())[0]
        d_top_0_value = list(d.values())[0]
        print("top_0:", d_top_0_key, d_top_0_value)

        d_top_9_key = list(d.keys())[9]
        d_top_9_value = list(d.values())[9]
        print("top_9:", d_top_9_key, d_top_9_value)

        # 计算紧密中心度
        print("Closeness centrality")
        c = nx.closeness_centrality(G)
        c = sorted(c.items(), key=lambda x: x[1], reverse=True)
        # 获取前三个值所对应的键
        c_top_keys = [x[0] for x in c[:10]]
        print("top_10_nodes:", c_top_keys)

        c = {k: v for k, v in c}
        c_top_0_key = list(c.keys())[0]
        c_top_0_value = list(c.values())[0]
        print("top_0:", c_top_0_key, c_top_0_value)

        c_top_9_key = list(c.keys())[9]
        c_top_9_value = list(c.values())[9]
        print("top_9:", c_top_9_key, c_top_9_value)

        # 计算特征向量中心度
        print("Eigenvector_centrality")
        e = nx.eigenvector_centrality(G)
        e = sorted(e.items(), key=lambda x: x[1], reverse=True)
        # 获取前三个值所对应的键
        e_top_keys = [x[0] for x in e[:10]]
        print("top_10_nodes:", e_top_keys)

        e = {k: v for k, v in e}
        e_top_0_key = list(e.keys())[0]
        e_top_0_value = list(e.values())[0]
        print("top_0:", e_top_0_key, e_top_0_value)

        e_top_9_key = list(e.keys())[9]
        e_top_9_value = list(e.values())[9]
        print("top_9:", e_top_9_key, e_top_9_value)

        # 进行网络操作，删边、重连、加边
        print("before", G)
        new_edges, rem_edges = add_and_remove_edges(G, var, 0)#0.4/0.6/0.8/1
        print("add edges num:", len(new_edges))
        print("del edges num:", len(rem_edges))
        G.add_edges_from(new_edges)
        G.remove_edges_from(rem_edges)
        print("after", G)

        # 计算K-shell
        print("k-shell")
        k_ = k_shell(G)
        # print(dict(k_))
        k_ = {value: key for key, values in dict(k_).items() for value in values}
        # print(k_)
        # for v in G.nodes():
        #     print(v, k_[v])

        # 计算PageRank
        print("PageRank")
        p_ = nx.pagerank(G, alpha=0.85)
        p_top_0_value_ = p_.get(p_top_0_key)
        print(p_top_0_key, p_top_0_value_)
        p_top_9_value_ = p_.get(p_top_9_key)
        print(p_top_9_key, p_top_9_value_)
        p_ = sorted(p_.items(), key=lambda x: x[1], reverse=True)  # 按值排序
        # 获取前三个值所对应的键
        p_top_keys_ = [x[0] for x in p_[:10]]
        print("top_10_nodes:", p_top_keys_)
        # print(p_)
        # 查找 top-1 的位置
        p_rank_0 = [item[0] for item in p_].index(p_top_0_key) + 1
        p_rank_9 = [item[0] for item in p_].index(p_top_9_key) + 1
        print("p_rank:", p_rank_0)  # 输出 3
        print("p_rank:", p_rank_9)  # 输出 3

        # 计算中介中心度
        print("Betweenness centrality")
        b_ = nx.betweenness_centrality(G)
        b_top_0_value_ = b_.get(b_top_0_key)
        print(b_top_0_key, b_top_0_value_)
        b_top_9_value_ = b_.get(b_top_9_key)
        print(b_top_9_key, b_top_9_value_)
        b_ = sorted(b_.items(), key=lambda x: x[1], reverse=True)  # 按值排序
        # 获取前三个值所对应的键
        b_top_keys_ = [x[0] for x in b_[:10]]
        print("top_10_nodes:", b_top_keys_)

        # 查找 top-1 的位置
        b_rank_0 = [item[0] for item in b_].index(b_top_0_key) + 1
        b_rank_9 = [item[0] for item in b_].index(b_top_9_key) + 1
        print("b_rank:", b_rank_0)  # 输出 3
        print("b_rank:", b_rank_9)  # 输出 3

        # 计算度中心度
        print("Degree centrality")
        d_ = nx.degree_centrality(G)
        d_top_0_value_ = d_.get(d_top_0_key)
        print(d_top_0_key, d_top_0_value_)
        d_top_9_value_ = d_.get(d_top_9_key)
        print(d_top_9_key, d_top_9_value_)
        d_ = sorted(d_.items(), key=lambda x: x[1], reverse=True)  # 按值排序
        # 获取前三个值所对应的键
        d_top_keys_ = [x[0] for x in d_[:10]]
        print("top_10_nodes:", d_top_keys_)

        # 查找 top-1 的位置
        d_rank_0 = [item[0] for item in d_].index(d_top_0_key) + 1
        d_rank_9 = [item[0] for item in d_].index(d_top_9_key) + 1
        print("d_rank:", d_rank_0)  # 输出 3
        print("d_rank:", d_rank_9)  # 输出 3

        # 计算紧密中心度
        print("Closeness centrality")
        c_ = nx.closeness_centrality(G)
        c_top_0_value_ = c_.get(c_top_0_key)
        print(c_top_0_key, c_top_0_value_)
        c_top_9_value_ = c_.get(c_top_9_key)
        print(c_top_9_key, c_top_9_value_)
        c_ = sorted(c_.items(), key=lambda x: x[1], reverse=True)  # 按值排序
        # 获取前三个值所对应的键
        c_top_keys_ = [x[0] for x in c_[:10]]
        print("top_10_nodes:", c_top_keys_)

        # 查找 top-1 的位置
        c_rank_0 = [item[0] for item in c_].index(c_top_0_key) + 1
        c_rank_9 = [item[0] for item in c_].index(c_top_9_key) + 1
        print("c_rank:", c_rank_0)  # 输出 3
        print("c_rank:", c_rank_9)  # 输出 3

        # 计算特征向量中心度
        print("Eigenvector centrality")
        e_ = nx.eigenvector_centrality(G)
        e_top_0_value_ = e_.get(e_top_0_key)
        print(e_top_0_key, e_top_0_value_)
        e_top_9_value_ = e_.get(e_top_9_key)
        print(e_top_9_key, e_top_9_value_)
        e_ = sorted(e_.items(), key=lambda x: x[1], reverse=True)  # 按值排序
        # 获取前三个值所对应的键
        e_top_keys_ = [x[0] for x in e_[:10]]
        print("top_10_nodes:", e_top_keys_)

        # 查找 top-1 的位置
        e_rank_0 = [item[0] for item in e_].index(e_top_0_key) + 1
        e_rank_9 = [item[0] for item in e_].index(e_top_9_key) + 1
        print("e_rank:", e_rank_0)  # 输出 3
        print("e_rank:", e_rank_9)  # 输出 3

        print("pagerank top-10 spearman:", scipy.stats.spearmanr(p_top_keys, p_top_keys_)[0])
        print("Betweenness top-10 spearman:", scipy.stats.spearmanr(b_top_keys, b_top_keys_)[0])
        print("Degree top-10 spearman:", scipy.stats.spearmanr(d_top_keys, d_top_keys_)[0])
        print("Closeness top-10 spearman:", scipy.stats.spearmanr(c_top_keys, c_top_keys_)[0])
        print("Eigenvector top-10 spearman:", scipy.stats.spearmanr(e_top_keys, e_top_keys_)[0])

        # 创建Workbook,相当于创建Excel
        xls = xlwt.Workbook(encoding='utf-8')
        # 创建sheet，Sheet1为表的名字，cell_overwrite_ok为是否覆盖单元格
        sheet = xls.add_sheet('sheet1', cell_overwrite_ok=True)
        # 创建的文件夹，用来写入处理后的数据

        file = r"C:\Users\hello\Desktop\数据\pubmed_random_add_"+str(var)+"%.xls"
        # 向表中添加数据
        sheet.write(0, 0, "PageRank")
        sheet.write(0, 1, "Betweenness centrality")
        sheet.write(0, 2, "Degree centrality")
        sheet.write(0, 3, "Closeness centrality")
        sheet.write(0, 4, "Eigenvector centrality")

        m = 0
        # p
        sheet.write(m + 1, 0, p_rank_0)
        sheet.write(m + 2, 0, (p_top_0_value_ - p_top_0_value) / p_top_0_value)
        sheet.write(m + 3, 0, p_rank_9)
        sheet.write(m + 4, 0, (p_top_9_value_ - p_top_9_value) / p_top_9_value)
        sheet.write(m + 5, 0, scipy.stats.spearmanr(p_top_keys, p_top_keys_)[0])
        # b
        sheet.write(m + 1, 1, b_rank_0)
        sheet.write(m + 2, 1, (b_top_0_value_ - b_top_0_value) / b_top_0_value)
        sheet.write(m + 3, 1, b_rank_9)
        sheet.write(m + 4, 1, (b_top_9_value_ - b_top_9_value) / b_top_9_value)
        sheet.write(m + 5, 1, scipy.stats.spearmanr(b_top_keys, b_top_keys_)[0])
        # d
        sheet.write(m + 1, 2, d_rank_0)
        sheet.write(m + 2, 2, (d_top_0_value_ - d_top_0_value) / d_top_0_value)
        sheet.write(m + 3, 2, d_rank_9)
        sheet.write(m + 4, 2, (d_top_9_value_ - d_top_9_value) / d_top_9_value)
        sheet.write(m + 5, 2, scipy.stats.spearmanr(d_top_keys, d_top_keys_)[0])
        # c
        sheet.write(m + 1, 3, c_rank_0)
        sheet.write(m + 2, 3, (c_top_0_value_ - c_top_0_value) / c_top_0_value)
        sheet.write(m + 3, 3, c_rank_9)
        sheet.write(m + 4, 3, (c_top_9_value_ - c_top_9_value) / c_top_9_value)
        sheet.write(m + 5, 3, scipy.stats.spearmanr(c_top_keys, c_top_keys_)[0])
        # e
        sheet.write(m + 1, 4, e_rank_0)
        sheet.write(m + 2, 4, (e_top_0_value_ - e_top_0_value) / e_top_0_value)
        sheet.write(m + 3, 4, e_rank_9)
        sheet.write(m + 4, 4, (e_top_9_value_ - e_top_9_value) / e_top_9_value)
        sheet.write(m + 5, 4, scipy.stats.spearmanr(e_top_keys, e_top_keys_)[0])

        # 保存到excel中
        xls.save(file)