
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def create_heterogeneous_ba_network(n, m, p):
    G = nx.Graph()
    # 添加初始m个节点
    nodes = list(range(m))
    G.add_nodes_from(nodes)
    # 初始化度数序列
    degrees = [m - 1] * m
    # 逐步添加新节点
    for i in range(m, n):
        # 计算每个节点被连接的概率
        probs = np.array(degrees) ** p
        probs /= np.sum(probs)
        # 随机选择m个节点进行连接
        targets = np.random.choice(nodes, m, replace=False, p=probs)
        # 将新节点连接到已有节点
        G.add_node(i)
        for t in targets:
            G.add_edge(i, t)
            degrees[t] += 1
        degrees.append(m)
        nodes.append(i)
    return G

# 测试
n = 300
m = 4
p = 0.01
hetero_ba_g = create_heterogeneous_ba_network(n, m, p)
print(hetero_ba_g)
print(nx.degree_histogram(hetero_ba_g))

degree = nx.degree_histogram(hetero_ba_g)  # 返回图中所有节点的度分布序列
x = range(len(degree))  # 生成x轴序列，从1到最大度
y = [z / float(sum(degree)) for z in degree]
# 将频次转换为频率，这用到Python的一个小技巧：列表内涵，Python的确很方便：）
plt.figure(dpi=200)
plt.bar(x, y, color="blue", linewidth=2)  # 在双对数坐标轴上绘制度分布曲线
plt.xlabel("$k$")
plt.ylabel("$p_k$")
plt.show()  # 显示图表

nx.write_edgelist(hetero_ba_g, "data/ban300_0.01.txt", delimiter=' ', data=False)
