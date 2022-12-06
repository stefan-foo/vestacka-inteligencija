from functools import reduce
from typing import Dict
from queue import LifoQueue
from utils import visualize_graph

Node = str

graph = {
  'A': ['B', 'C'],
  'B': ['A', 'C', 'D'],
  'C': ['A', 'B', 'D'],
  'D': ['E', 'B', 'C'],
  'E': ['D']
}

graph_large = {
  'A': ['I', 'B', 'C'],
  'B': ['A', 'E', 'D'],
  'C': ['G', 'F'],
  'D': ['B', 'G', 'H'],
  'E': ['J', 'F', 'B'],
  'F': ['H', 'C', 'E'],
  'G': ['J', 'C', 'D'],
  'H': ['I', 'D', 'F'],
  'I': ['A', 'H', 'J'],
  'J': ['G', 'I', 'E']
}

domain = set({ 'R', 'G', 'B' })

def is_safe(graph, node, assigned: Dict[Node, str], assignment) -> bool:
  for adjecent in graph[node]:
    if (assigned.get(adjecent, None) == assignment):
      return False
  return True

def is_safe_fc(graph, assigned, constraints, node, value):
  return

def backtrack(graph: Dict[Node, list[Node]], node: Node, assigned = {}, domains = {}) -> Dict[Node, str]:
  print("recursed")
  for value in domain:
    if (is_safe(graph, node, assigned, value)):
      assigned[node] = value

      if (len(assigned) == len(graph)):
        return assigned
    
      for adjecent in graph[node]:
        if (adjecent in assigned):
          continue

        result = backtrack(graph, adjecent, assigned)
      
        if (result):
          return result
        else:
          break

      assigned.pop(node)
  
  return None

domains = {}
for node in graph.keys():
  domains[node] = set(domain)
result = backtrack(graph_large, 'A')

if not result:
  exit()

visualize_graph(graph_large, result)
