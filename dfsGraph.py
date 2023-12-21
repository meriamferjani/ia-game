import networkx as nx
import matplotlib.pyplot as plt
import mplcursors

# Define the graph
graph = dict()
graph["E0"] = ["E1", "E2", "E3", "E4"]
graph["E1"] = ["N1"]
graph["E2"] = ["N3"]
graph["E3"] = ["N4"]
graph["E4"] = ["N8"]
graph["N1"] = ["E1", "N2"]
graph["N2"] = ["N1", "N3"]
graph["N3"] = ["E2", "N2"]
graph["N4"] = ["E3", "N5"]
graph["N5"] = ["N4", "N6"]
graph["N6"] = ["N5", "N7"]
graph["N7"] = ["N6", "N8", "N9"]
graph["N8"] = ["E4", "N7"]
graph["N9"] = ["N7", "N10"]
graph["N10"] = ["N11", "N12"]
graph["N11"] = ["N10", "N13"]
graph["N12"] = ["N10", "N13", "T"]
graph["N13"] = ["N11", "N12"]
graph["T"] = ["N12"]

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges to the graph
for node, neighbors in graph.items():
    G.add_node(node)
    for neighbor in neighbors:
        G.add_edge(node, neighbor)

# Plot the graph
pos = nx.spring_layout(G, seed=500)  # Layout algorithm
nx.draw(G, pos, with_labels=True, node_size=800, node_color='skyblue', alpha=0.8, font_size=10, font_weight='bold')
nx.draw_networkx_edges(G, pos, arrows=True, edge_color='black')


# Display the plot
plt.title("Graph")
plt.show()
