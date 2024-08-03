from graph_tool.all import *
import graph_tool as gt
from graph_tool.inference import *


def recon(fun):
    #g = gt.Graph(directed=False)
    edge_list = []
    with open(fun + '_PPI_edge.txt') as f:
        for line in f:
            line = line.strip('\n')
            edge_list.append((line.split('\t')[0],line.split('\t')[1]))
    g= Graph(edge_list, hashed=True,hash_type="string",directed=False)

    state = gt.inference.CliqueState(g)
    state.mcmc_sweep(niter=10000)
    cliques = []
    for v in state.f.vertices():      # iterate through factor graph
        if state.is_fac[v]:
            continue                  # skip over factors
        #print(state.c[v], state.x[v]) # clique occupation
        if state.x[v] > 0:
            cliques.append(state.c[v])

    cliques_hash = []
    for c in cliques:
        if len(c) > 2:
            cliques_hash.append(sorted([g.vp.ids[i] for i in c]))
        
    cliques_max = max([len(i) for i in cliques_hash])
    w_f = open(fun + '_re.txt', 'w+')
    for cliques in cliques_hash:
        w_f.write('\t'.join(cliques) + '\t'*(cliques_max - len(cliques)) + '\n')
    w_f.close()
    print(fun)

fun_type = [ 'EPS']
#fun_type = ['gvp', 'cas']
for i in fun_type:
    recon(i)