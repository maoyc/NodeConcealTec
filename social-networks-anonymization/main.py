import networkx as nx
import pandas as pd

import anonymity
import graph
import queries

from sys import stderr
from datetime import datetime


def main():
    graphs = [
#        graph.create_ex_graph(),
#        graph.create_random_graph(300, 0.027),
#        graph.create_ws_graph(300, 8, 0.5),
#        graph.create_scale_free_graph(300,4),

#        graph.create_random_graph(100, 0.5),
#        graph.create_random_graph(500, 0.01),
#        graph.create_random_graph(1000, 0.005),

#        graph.create_scale_free_graph(100),
#        graph.create_scale_free_graph(500),
#        graph.create_scale_free_graph(1000),

#        graph.read_graph('data/enron.txt', 'enron-5'),
#        graph.read_graph('data/hepth.txt', 'hepth'),
       graph.read_graph('data/ba5000.txt', 'ba5000')
    ]

    with open('out/times.csv', 'a') as f:
        for g in graphs:
            compute_graph(g, f)


def compute_graph(g, f_times=None, draw=False):
    print(g)
    t1 = datetime.now()

    print(g.name, file=stderr)

    if draw:
        layout = nx.spring_layout(g)

    measures = {}
    for pert in [.01,.02,.03]:
        print('  perturbation ({:.0%} of edges)...'.format(pert), file=stderr)

        pert_graph = anonymity.perturbation(g, pert)
        nx.write_edgelist(pert_graph, "ba5000_cluster"+str(pert)+".txt", delimiter=' ', data=False)
        if draw:
            graph.draw_graph(pert_graph, pert, layout)

        print('    measurements...', file=stderr)
        measurements = graph.get_measurements(pert_graph)

        print('    h...', file=stderr)
        h = [anonymity.deanonymize_h(pert_graph, i) for i in range(0, 5)]

        print('    edge facts...', file=stderr)
        ef = [] #[anonymity.deanonymize_edgefacts(g, pert_graph, n) for n in range(0, 51, 10)]

        measures[pert] = pd.concat([measurements, *h, *ef])

    t2 = datetime.now()
    t = t2 - t1

    print('  execution time: {}'.format(t), file=stderr)

    if f_times is not None:
        print('{},{}'.format(g.name, t.total_seconds()), file=f_times)

    df = pd.DataFrame(measures)
    # print(df.to_string(), file=stderr)
    print(g)

    df.to_csv('out/{}.csv'.format(g.name))


if __name__ == '__main__':
    main()
