import networkx as nx
import matplotlib.pyplot as plt

colors = { 'R': 'red', 'G': 'green', 'B': 'blue'}

def visualize_graph(graph, assignment):
  edge_list = []
  for node in graph.keys():
    for edge in graph[node]:
      edge_list.append((node, edge))

  G = nx.DiGraph()
  G.add_nodes_from(graph.keys())
  G.add_edges_from(edge_list)

  color_map = []
  for node in G:
    color_map.append(colors[assignment[node]])

  nx.draw(G, node_color = color_map)
  plt.show()