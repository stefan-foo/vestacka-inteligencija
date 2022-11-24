from queue import Queue
from pprint import pprint
import typing
import math

# 17. Napisati funkciju koja na osnovu zadatog težinskog neusmerenog grafa i zadatog (ciljnog) čvora G
# formira neusmereni težinski graf sa heuristikom. Heuristika proizvoljnog čvora C se određuje kao
# dužina puta od čvora C do čvora G. 

def gen_heuristics(
  graph: typing.Dict[str, list[tuple[str, int]]], 
  relative_node: str
) -> typing.Dict[str, tuple[int, list[tuple[str, int]]]]:

  queue = Queue()
  queue.put(relative_node)
  visited = { relative_node: 0 }

  while not queue.empty():
    cur = queue.get()
    for child, _ in graph[cur]:
      if child not in visited:
        visited[child] = visited[cur] + 1
        queue.put(child)
  
  output_graph = {}
  for node in graph.keys():
    output_graph[node] = (visited.get(node, math.inf), list(graph[node]))

  return output_graph
  
def gen_heuristics_with_weight(
  graph: typing.Dict[str, list[tuple[str, int]]], 
  relative_node: str
) -> typing.Dict[str, tuple[int, list[tuple[str, int]]]]:

  queue = Queue()
  queue.put(relative_node)
  weights = { relative_node: 0 }

  while not queue.empty():
    cur = queue.get()
    cur_weight = weights[cur]

    for child, edge_weight in graph[cur]:
      weight_to_child = cur_weight + edge_weight
      if child not in weights or (child in weights and weight_to_child < weights[child]):
        weights[child] = weight_to_child
        queue.put(child)
  
  output_graph = {}
  for node in graph.keys():
    output_graph[node] = (weights.get(node, math.inf), list(graph[node]))

  return output_graph

def is_undirected(
  graph: typing.Dict[str, list[tuple[str, int]]], 
  convert_to_undirected = False
) -> bool:

  for node, edges in graph.items():
    for child, weight in edges:
      equivalent_node = list(filter(lambda x: x[0] == node and x[1] == weight, graph[child]))
      if not equivalent_node:
        print(f"Edge ({child}, {weight}) of node {node} unmatched")
        if convert_to_undirected:
          graph[child].append((node, weight))
          print(f"Edge from {child} to {node} with weight {weight} added")
        else:
          return False
  return True

initial_graph = {
  'A': [('B', 2), ('C', 5), ('I', 4)],
  'B': [('A', 2), ('E', 3)],
  'C': [('A', 5), ('F', 1), ('G', 3)],
  'D': [('F', 1)],
  'E': [('B', 3), ('G', 4)],
  'F': [('C', 1), ('D', 1), ('G', 5)],
  'G': [('E', 4), ('F', 5), ('C', 3)],
  'H': [],
  'I': [('A', 4)]
}

is_undirected(initial_graph, convert_to_undirected=True)

heuristics_graph = gen_heuristics(initial_graph, 'G')
pprint(heuristics_graph)