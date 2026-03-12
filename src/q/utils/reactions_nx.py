import networkx as nx

def make_reactions_graph(species, reactions):
    g = nx.DiGraph()

    species_nodes = list()
    reaction_nodes = list()
    reactants_edges = set()
    product_edges = set()
    both_edges = set()

    for n in species:
        g.add_node(n.name)
        species_nodes.append(n.name)

    for r in reactions:
        as_formula = r.to_formula()

        g.add_node(as_formula)
        reaction_nodes.append(as_formula)

        for rr in r.reactants:
            g.add_edge(rr, as_formula)
            reactants_edges.add((rr, as_formula))

        for p in r.products:
            g.add_edge(as_formula, p)
            product_edges.add((as_formula, p))

        for p in product_edges:
            if (p[1], p[0]) in reactants_edges:
                both_edges.add(p)
    
    for b in both_edges:
        product_edges.remove(b)
        reactants_edges.remove((b[1], b[0]))
    
    return g,species_nodes, reaction_nodes, reactants_edges, product_edges, both_edges