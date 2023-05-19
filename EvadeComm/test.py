import igraph as ig

# 创建Karate网络
karate = ig.Graph.Famous('Zachary')

# 使用Louvain算法检测社团
communities = karate.community_multilevel()

# 输出每个节点所属的社团
for node, community in enumerate(communities):
    print(f"Node {node+1} belongs to community {community}")

# 输出每个社团的连边
for community_idx, subgraph in enumerate(karate.community_subgraphs(communities)):
    edges = subgraph.get_edgelist()
    print(f"Edges in community {community_idx+1}:")
    for edge in edges:
        print(edge)

# 创建社团之间的连边图
community_graph = ig.Graph.Community(edges=karate.community_edge_betweenness().as_clustering())

# 输出社团之间的连边
community_edges = community_graph.get_edgelist()
print("Edges between communities:")
for edge in community_edges:
    print(edge)
