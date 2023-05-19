# encoding: utf-8

import importlib
import sys

import networkx as nx
import scipy.sparse as sp

importlib.reload(sys)

def parse_index_file(filename):
    index = []
    for line in open(filename):
        index.append(int(line.strip()))
    return index


def load_data(dataset):
    # load the data: x, tx, allx, graph
    path = './datasets/'
    
    if dataset == 'karate':
       
        g = nx.karate_club_graph()
        # features = sp.vstack((nx.to_scipy_sparse_matrix(g))).tolil()
        adj = nx.to_numpy_matrix(nx.from_dict_of_lists(nx.to_dict_of_lists(g)))
        print(adj)

    return adj



