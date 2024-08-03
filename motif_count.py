from graph_tool.all import *
import graph_tool as gt
from graph_tool.inference import *

edge_list = []
with open('TCA_PPI_edge.txt') as f:
    for line in f:
        line = line.strip('\n')
        edge_list.append((line.split('\t')[0],line.split('\t')[1]))
g= Graph(edge_list, hashed=True,hash_type="string",directed=False)
motifs_3 = graph_tool.clustering.motifs(g, 3,  return_maps=False)
motifs_4 = graph_tool.clustering.motifs(g, 4,  return_maps=False)
motifs_5 = graph_tool.clustering.motifs(g, 5,  return_maps=False)
G_map = motifs_3[0] + motifs_4[0] + motifs_5[0]

def motif_count(fun, g_map):
    #g = gt.Graph(directed=False)
    edge_list = []
    with open(fun + '_PPI_edge.txt') as f:
        for line in f:
            line = line.strip('\n')
            edge_list.append((line.split('\t')[0],line.split('\t')[1]))
    g= Graph(edge_list, hashed=True,hash_type="string",directed=False)
    
    motifs_3 = graph_tool.clustering.motifs(g, 3, motif_list = g_map[:2], return_maps=False)
    motifs_4 = graph_tool.clustering.motifs(g, 4, motif_list = g_map[2:8], return_maps=False)
    motifs_5 = graph_tool.clustering.motifs(g, 5, motif_list = g_map[8:], return_maps=False)
    count = motifs_3[1] + motifs_4[1] + motifs_5[1]
    G_map = motifs_3[0] + motifs_4[0] + motifs_5[0]
    
    write_file = open('PPI.count.txt', 'a+')
    write_file.write(fun + '\t' + '\t'.join([str(i) for i in count])  +'\n')
    print(fun)
    
fun_type = [ 'gvp', 'HM', 'KKS', 'CF', 'OP', 'TCA', 'ph', 'N', 'S', 'cas', 'SM', 'RM', 'XM', 'FAM', 'GLY', 'PPP', 'SUM', 'MM', 'CCM', 'ROS', 'P', 'AAT', 'AAG', 'AP', 'BBS', 'TEVIT']
#fun_type = ['gvp', 'cas']
for i in fun_type:
    motif_count(i, G_map)