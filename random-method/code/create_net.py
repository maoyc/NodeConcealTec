import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import pickle
from networkx.algorithms import community
import networkx.algorithms.community as nx_comm
import scipy.sparse as sp
from collections import defaultdict

def generate_graph(edges):
    G = nx.Graph()
    G.add_edges_from(edges)
    return G

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
    config = {
        "font.family": 'serif',
        "font.size": 12,
        "mathtext.fontset": 'stix',
        "font.serif": ['SimSun'],
    }
    rcParams.update(config)

    # ER = nx.gnp_random_graph(10, 0.4)
    ER = nx.gnm_random_graph(10, 4)
    WS = nx.watts_strogatz_graph(10, 4, 0.25)
    BA = nx.barabasi_albert_graph(10, 2)
    # G = nx.dual_barabasi_albert_graph(300,2,4,0.1)
    # G = nx.extended_barabasi_albert_graph(100,3,0.3,0.3)
    # print(G)
    pos = nx.circular_layout(ER)
    nx.draw_networkx(ER, pos, with_labels = False)
    plt.savefig(r'C:/Users/hello/OneDrive/毕业论文/图片/ER.jpg', bbox_inches='tight')
    plt.show()

    # G = nx.karate_club_graph()
    # file = open("dolphin.pkl", "rb")
    # edges = pickle.load(file)
    # G = generate_graph(edges)

    # 打开txt文件
    # filename = '../data/PubMed.txt'
    # G = nx.Graph()
    # with open(filename) as file:
    #     for line in file:
    #         head, tail = [int(x) for x in line.split(' ')]
    #         G.add_edge(head, tail)
    # print(G)


    # 打开npz文件
    # adj = sp.load_npz("dblp_medium_adj.npz")
    # print(type(adj))
    # G = nx.from_scipy_sparse_array(adj)
    # print(G)

    # 计算K-shell
    # kshell = k_shell(G)
    # print(kshell)
    # 输出最大的K-shell编号
    # max_k = max(kshell.keys())
    # print("最大的K-shell编号为：", max_k)
    # print("网络密度：", nx.average_clustering(G))

    # 用 label_propagation 算法进行社团检测
    # communities = nx_comm.louvain_communities(G)
    # print("社团划分：",list(communities))
    # print("Q:",nx_comm.modularity(G, nx_comm.louvain_communities(G)))

    # 将社团信息写入节点的属性
    # node_attributes = {}
    # for i, comm in enumerate(tuple(sorted(c) for c in next(communities))):
    #     for node in comm:
    #         node_attributes[node] = {'commID': i}
    # print(node_attributes)
    # nx.set_node_attributes(ws, node_attributes)

    # 构造社团信息的字典
    # comm_dict = {}
    # for i, comm in enumerate(communities):
    #     for node in comm:
    #         comm_dict[node] = i
    # print(comm_dict)
    # # 将社团信息作为节点属性标记在节点上
    # nx.set_node_attributes(G, comm_dict, "commID")

    # 度分布
    # degree = nx.degree_histogram(G)  # 返回图中所有节点的度分布序列
    # x = range(len(degree))  # 生成x轴序列，从1到最大度
    # y = [z / float(sum(degree)) for z in degree]
    # # 将频次转换为频率，这用到Python的一个小技巧：列表内涵，Python的确很方便：）
    # plt.bar(x, y, color="blue", linewidth=2)  # 在双对数坐标轴上绘制度分布曲线
    # plt.xlabel("$k$")
    # plt.ylabel("$p_k$")
    # plt.savefig(r'C:/Users/hello/OneDrive/毕业论文/度分布/PubMed.eps', dpi=300, format='eps')
    # plt.show()  # 显示图表

    # 输出边列表txt文件
    # nx.write_edgelist(G, "ban100_0.9.txt", delimiter=' ', data=False)

    # # 输出pickle文件
    # file = open('er.pickle', 'wb')
    # pickle.dump(er.edges, file)
    # file.close()

    # 将节点的社团写入 GML 文件中
    # print(G.edges)
    # nx.write_gml(G, "ba300.gml")
    #
    # H = nx.read_gml("ba300.gml")
    # print(H.edges)
