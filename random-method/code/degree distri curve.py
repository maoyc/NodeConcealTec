# Copyright (c)2017, 东北大学软件学院学生
# All rightsreserved
# 文件名称：a.py
#  作   者：孔云
# 问题描述：统计图中的每个节点的度，并生成度序列
# 问题分析：利用networkx。代码如下:
import matplotlib.pyplot as plt  # 导入科学绘图包
import networkx as nx
from matplotlib import rcParams
import numpy as np

config = {
    "font.family": 'serif',
    "font.size": 12,
    "mathtext.fontset": 'stix',
    "font.serif": ['SimSun'],
}
rcParams.update(config)

# 打开txt文件
filename = '../data/usair.txt'
G = nx.Graph()
with open(filename) as file:
    for line in file:
        head, tail = [int(x) for x in line.split(' ')]
        G.add_edge(head, tail)
print(G)

filename = '../data/usair.txt'
H = nx.Graph()
with open(filename) as file:
    for line in file:
        head, tail = [int(x) for x in line.split(' ')]
        H.add_edge(head, tail)
print(H)

G_degree = nx.degree_histogram(G)  # 返回图中所有节点的度分布序列
# G_x = range(len(degree))  # 生成x轴序列，从1到最大度
G_data = [z / float(sum(G_degree)) for z in G_degree]
# 将数据列表转换为NumPy数组
G_data_np = np.array(G_data)
# 创建一个布尔数组，表示哪些点的值不为0
G_non_zero_mask = G_data_np != 0
# 创建一个新的NumPy数组，其中仅包含值不为0的点
G_y = G_data_np[G_non_zero_mask]
# 创建一个包含x轴坐标的NumPy数组
G_x_values = np.arange(len(G_data))
# 创建一个包含x轴坐标的NumPy数组，其中仅包含值不为0的点
G_x = G_x_values[G_non_zero_mask]

H_degree = nx.degree_histogram(H)  # 返回图中所有节点的度分布序列
# H_x = range(len(degree))  # 生成x轴序列，从1到最大度
H_data = [z / float(sum(H_degree)) for z in H_degree]
# 将数据列表转换为NumPy数组
H_data_np = np.array(H_data)
# 创建一个布尔数组，表示哪些点的值不为0
H_non_zero_mask = H_data_np != 0
# 创建一个新的NumPy数组，其中仅包含值不为0的点
H_y = G_data_np[H_non_zero_mask]
# 创建一个包含x轴坐标的NumPy数组
H_x_values = np.arange(len(H_data))
# 创建一个包含x轴坐标的NumPy数组，其中仅包含值不为0的点
H_x = H_x_values[H_non_zero_mask]
# 将频次转换为频率，这用到Python的一个小技巧：列表内涵，Python的确很方便：）
plt.plot(G_x, G_y,'--',  color="green",alpha=1, linewidth=2, label="隐匿前",dashes=(2, 2))  # 在双对数坐标轴上绘制度分布曲线
plt.plot(H_x, H_y,'--', color="red",alpha=1, linewidth=2, label="隐匿后",dashes=(3, 3))  # 在双对数坐标轴上绘制度分布曲线
plt.legend(loc="best")
# plt.scatter(G_x, G_y, c='blue')
plt.xlabel("$k$")
plt.ylabel("$p_k$")

plt.savefig(r'C:/Users/hello/OneDrive/毕业论文/隐匿前后的度分布曲线/usair.eps', dpi=300, format='eps')
# plt.show()  # 显示图表
