import networkx as nx

G = nx.Graph()
G.add_edges_from([(0,1),(0,2),(0,3),(0,4),(0,8),(0,5),(0,9),(0,6),(0,7),(1,2),(1,5),(2,7),(2,5),(2,4),(2,3),(3,7),(3,5),(3,4),(4,7),(4,5),(4,9),(5,7),(5,6)])
print(G)

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
G.add_edges_from([(9,5),(5,8)])
G.remove_edges_from([(0,5),(0,9)])
print("after", G)

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