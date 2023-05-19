import networkx as nx
import random
import matplotlib.pyplot as plt


def generate_price_network(N, p, m0, m):
    # 生成一个节点数为m0的初始强连通网络
    G = nx.Graph()
    initial_nodes = range(m0)
    G.add_nodes_from(initial_nodes)
    G.add_edges_from((i, (i + 1) % m0) for i in range(m0))
    target_nodes = list(initial_nodes)

    # 将初始网络中每条边指向的节点存入数组Array
    target_array = [(i, (i + 1) % m0) for i in range(m0)]

    # for i in range(m0, N)
    for i in range(m0, N):
        # 新增一个节点
        G.add_node(i)
        # 随机选择m个节点与新增节点相连
        targets = []
        for j in range(m):
            r = random.random()
            if r < p:
                # 随机选择一个节点与新增节点相连
                target = random.choice(target_nodes)
            else:
                # 从Array随机选择一个节点与新增节点相连
                target = random.choice(target_array)
                target = target[1] if target[0] == i else target[0]
            targets.append(target)
            # 将新增节点与目标节点相连
            G.add_edge(i, target)
        # 将新增节点的连边放入Array
        target_array.extend([(i, t) for t in targets])
        # 更新目标节点列表
        target_nodes.extend(targets)
        target_nodes.append(i)

    # 使用度分布指数alpha重置网络节点的度数

    return G


p = 0.99
G = generate_price_network(100, p, 10, 3)
print(G)
degree = nx.degree_histogram(G)  # 返回图中所有节点的度分布序列
x = range(len(degree))  # 生成x轴序列，从1到最大度
y = [z / float(sum(degree)) for z in degree]
# 将频次转换为频率，这用到Python的一个小技巧：列表内涵，Python的确很方便：）
plt.bar(x, y, color="blue", linewidth=2)  # 在双对数坐标轴上绘制度分布曲线
plt.xlabel("$k$")
plt.ylabel("$p_k$")
plt.show()  # 显示图表

nx.write_edgelist(G, "ba100_" + str(p) + ".txt", delimiter=' ', data=False)
