import networkx as nx
import matplotlib.pyplot as plt
from scipy.io import mmread

# Load matrix
A = mmread("datasets/bcspwr01.mtx.gz")

# Graph বানাও
G = nx.from_scipy_sparse_array(A)

# Self-loop remove করো
G.remove_edges_from(nx.selfloop_edges(G))

print(f"Nodes: {G.number_of_nodes()}")
print(f"Edges: {G.number_of_edges()}")

# Basic graph info
print(f"Average degree: {sum(dict(G.degree()).values()) / G.number_of_nodes():.2f}")
print(f"Max degree node: {max(G.degree(), key=lambda x: x[1])}")

# Visualize
nx.draw(G, with_labels=True, node_color='lightblue', node_size=500)
plt.title("BCSPWR01 - Self-loop removed")
plt.show()



def power_dominating_set_greedy(G):
    observed = set()
    pds = set()
    remaining = set(G.nodes())

    def propagate():
        changed = True
        while changed:
            changed = False
            for v in observed.copy():
                neighbors = set(G.neighbors(v))
                unobserved = neighbors - observed
                if len(unobserved) == 1:
                    observed.update(unobserved)
                    changed = True

    while observed != set(G.nodes()):
        best = max(
            remaining,
            key=lambda v: len(set(G.neighbors(v)) - observed)
        )
        pds.add(best)
        remaining.discard(best)

        
        observed.add(best)
        observed.update(G.neighbors(best))

        propagate()

    return pds


pds = power_dominating_set_greedy(G)
print(f"PDS size: {len(pds)}")
print(f"PDS nodes: {sorted(pds)}")

# Visualize — PDS node in red color
color_map = ['red' if node in pds else 'lightblue' for node in G.nodes()]
nx.draw(G, with_labels=True, node_color=color_map, node_size=500)
plt.title(f"BCSPWR01 — Greedy PDS (size={len(pds)})")
plt.show()