# implementation for the baseline - DICE

import igraph
from copy import deepcopy
from random import randint
from scipy.stats import entropy
import numpy as np
import networkx as nx

def read_Graph(dataset):
	return igraph.Graph.Read_GML(dataset)

def get_Communities(graph):
	return graph.community_multilevel()

def delete_graph_edge(graph, list_edge_ID):
	graph.delete_edges(list_edge_ID)

def find_deletion_edge(graph, target_community_vertices):
	edge_List = graph.get_edgelist()
	for i in edge_List:
		if (i[0] in target_community_vertices and i[1] in target_community_vertices):
			return i 
	return randint(0, graph.ecount()-1)

def add_graph_edge(graph, list_vertex_tuple):
	graph.add_edges([list_vertex_tuple])

def find_addition_tuple(graph, target_community_vertices):
	v1 = target_community_vertices[randint(0, len(target_community_vertices)-1)]
	v2 = randint(0, graph.vcount()-1)
	while (v2 in target_community_vertices):
		v2 = randint(0, graph.vcount()-1)
	return (v1, v2)

def DICE_algorithm(graph, beta, target_community_vertices):
	operation_count = randint(0, beta)

	for i in range(operation_count):
		deletion_edge_tuple = find_deletion_edge(graph, target_community_vertices)
		delete_graph_edge(graph, deletion_edge_tuple)

	for i in range(beta - operation_count):
		addition_edge_tuple = find_addition_tuple(graph, target_community_vertices)
		add_graph_edge(graph, addition_edge_tuple)

	return graph

def calculate_NMI(communities_before, communities_after):
	return igraph.compare_communities(communities_after, communities_before, method = "nmi")

def check_neighbours(neighbours, communities):
	ctr = 0
	List = []
	for i in range(len(communities)):
		for j in communities[i]:
			if j in neighbours:
				List.append(i)
				ctr += 1
			if ctr == len(neighbours):
				return List
	return List

def get_neighborhood_community(graph, target_community):
	neighborhood_community = []
	for j in target_community:
		neighborhood_community.extend(graph.neighbors(j))

	return list(set(neighborhood_community))

def create_subgraph_adjacency_list(Adjacency_List, target_community):
	new_adj = {}
	for j in range(len(Adjacency_List)):
		if j in target_community:
			new_adj[j] = []
			for k in Adjacency_List[j]:
				if k in target_community:
					new_adj[j].append(k)
	return new_adj

def num_comm(target_comm, communities):
	uni_comm = []
	comm_list = []
	for node in target_comm:
		for c in communities:
			if node in c:
				comm_list.append(c)
				if c not in uni_comm:
					uni_comm.append(c)
					break
	return len(uni_comm), comm_list

def get_entropy(labels, base = None):
	values, counts = np.unique(labels, return_counts = True)
	return entropy(counts, base = base)

path = '../Datasets/data/ban300_0.01.txt'

graph = nx.Graph()
with open(path) as file:
	for line in file:
		head, tail = [int(x) for x in line.split(' ')]
		graph.add_edge(head, tail)
print(graph)

# convert to igraph
original_graph = igraph.Graph.from_networkx(graph)

# original_graph = read_Graph(path)
graph = deepcopy(original_graph)
communities_before = get_Communities(original_graph)

NMI_list = []
neighborhood_NMI_list = []
sum_entropy, sum_comm = 0, 0

nmi_ls=[]
for i in communities_before:
	target_community = i

	beta = int(0.3*len(target_community))

	neighborhood_community = get_neighborhood_community(graph, target_community)
	final_graph = DICE_algorithm(graph, beta, target_community)
	communities_after = get_Communities(final_graph)

	pre_neighbors = check_neighbours(neighborhood_community, communities_before)
	post_neighbors = check_neighbours(neighborhood_community, communities_after)

	NMI_Score = calculate_NMI(communities_before, communities_after)
	print(NMI_Score)
	nmi_ls.append(NMI_Score)
	neighborhood_NMI_Score = calculate_NMI(pre_neighbors, post_neighbors)
	subgraph_adjacency_list = create_subgraph_adjacency_list(final_graph.get_adjlist(), target_community)
	
	NMI_list.append(NMI_Score)
	neighborhood_NMI_list.append(neighborhood_NMI_Score)

	num_splits, comm_list = num_comm(target_community, communities_after)
	sum_comm = sum_comm + num_splits
	entropy_val = get_entropy(comm_list)
	sum_entropy = sum_entropy + entropy_val

	graph = original_graph
print("平均值：",sum(nmi_ls)/len(nmi_ls))