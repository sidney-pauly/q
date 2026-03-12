import json
import re
from typing import Iterable
import networkx as nx
import matplotlib.pyplot as plt

from q.utils.reactions import Reaction, Species, filter_reactions, read_reactions_dat_file
from q.utils.reactions_nx import make_reactions_graph

experiment_dir = '/home/sidney/repos/abdn/HPEM/experiments/GEC-CCP2a_NH3'
run = 'run1'
# dat_file = f'{experiment_dir}/output/{run}/icp.dat'
dat_file = f'{experiment_dir}/HPEM_Master_v01.dat'

species, reactions = read_reactions_dat_file(dat_file)

nitrous_species = [s for s in species.values() if re.search('^[NHE\*\^0-9]+$', s.name) is not None and 'HE' not in s.name]
nitrous_species_names = set(s.name for s in nitrous_species)
included_reactions = [r for r in reactions if all([(rr in nitrous_species_names) for rr in r.reactants]) and all([(rr in nitrous_species_names) for rr in r.products])]


# nitrous_species, included_reactions = filter_reactions(nitrous_species, included_reactions, filter_reactants=['H1'])

g, species_nodes, reaction_nodes, reactants_edges, product_edges, both_edges = make_reactions_graph(nitrous_species, included_reactions)

# layout = nx.shell_layout(g, [reaction_nodes, species_nodes])
# layout = nx.spring_layout(g, pos=layout, fixed=species_nodes, iterations=400)

layout = nx.spring_layout(g)

plt.figure(figsize=(16, 16))

# Draw species
species_size = 600
nx.draw_networkx_nodes(g, layout, nodelist=species_nodes, node_color='0', node_size=species_size, margins=0)
nx.draw_networkx_labels(g, layout, dict((n, n) for n in species_nodes), font_color='1', font_size=10)

# Draw reactions
reaction_size = 50
nx.draw_networkx_nodes(g, layout, nodelist=reaction_nodes, node_color='0', node_size=reaction_size)
# nx.draw_networkx_labels(g, layout, dict((n, n) for n in reaction_nodes), font_color='0', font_size=8)

# Draw edges
edgewidth = 1
nx.draw_networkx_edges(g, layout, reactants_edges, width=edgewidth, edge_color='r', arrows=True, arrowsize=30, node_size=species_size)
nx.draw_networkx_edges(g, layout, product_edges, width=edgewidth, edge_color='b', arrows=True, arrowsize=30, node_size=species_size)
nx.draw_networkx_edges(g, layout, both_edges, width=edgewidth, edge_color='0', arrows=False, node_size=species_size)


plt.box(False)
plt.savefig('reactions.png', dpi=500, bbox_inches='tight')
