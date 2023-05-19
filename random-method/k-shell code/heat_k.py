import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np

# 图片显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False  # 减号unicode编码

config = {
    "font.family": 'serif',
    "font.size": 10,
    "mathtext.fontset": 'stix',
    "font.serif": ['SimSun'],
}
rcParams.update(config)

data = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0.19, 0.99, 1,0.64,0.99,1, 0.24, 0.45, 0.68,0.29,0.65,0.28],
        [0.1, 0.07, 0.04,0.08,0.10,0.02, 0.07, 0.14, 0.31,0.09,0.34,0.09],
        [0.05, 0.03, 0.01,0.01,0.01,0.08, 0.1, 0.05, 0.14,0.01,0.03,0.05],
        [0, 0.05, 0,0.09,0.15,0.12, 0.09, 0.06, 0.12,0.04,0.08,0.05],
        [0.24, 0.92, 0.99,0.26,0.9,0.99, 0.13, 0.30, 0.49,0.20,0.37,0.25],
        [0.12, 0.08, 0.13,0, 0, 0, 0.11, 0.09, 0.21, 0, 0, 0],
        [0.52, 0.28, 0.32,0, 0, 0, 0.19, 0.39, 0.59, 0, 0, 0],]
datasets = ['BA300', 'ER300', 'WS300', 'BA10000', 'ER10000', 'WS10000', 'Circuit', '685-BUS', 'Usair97', 'US-Grid',
            'DBLP', 'PubMed']
alo = ['随机增边', '随机删边', '随机重连边', 'Cluster', 'k度匿名', 'top-k度值边删除', 'ROAM','GA']

fig, ax = plt.subplots(dpi=180)

im = ax.imshow(data, cmap='coolwarm', interpolation='nearest')

# 设置坐标轴标签和刻度
ax.set_xticks(np.arange(len(datasets)))
ax.set_yticks(np.arange(len(alo)))
ax.set_xticklabels(datasets)
ax.set_yticklabels(alo)

ax.set_xticks(np.arange(len(datasets))-.5, minor=True)
ax.set_yticks(np.arange(len(alo))-.5, minor=True)
# 关闭网格并用白色加宽网格
for edge, spine in ax.spines.items():
    spine.set_visible(False)
ax.grid(which="minor", color="w", linestyle='-', linewidth=2)

plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")



# 为每个单元格添加文本注释
for i in range(len(alo)):
    for j in range(len(datasets)):
        text = ax.text(j, i, data[i][j],
                       ha='center', va='center', color='black')

# 添加颜色条
cbar = ax.figure.colorbar(im, ax=ax, cmap='coolwarm', shrink=0.6)
cbar.ax.set_ylabel("ASR", rotation=-90, va="bottom")

# 显示图形
plt.savefig(r"C:/Users/hello/Desktop./new_result.png", dpi=180, bbox_inches='tight')
plt.show()
