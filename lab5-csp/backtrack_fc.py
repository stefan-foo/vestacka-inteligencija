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

def is_safe_fc(graph, assigned, domains, node, value):
  return

def backtrack(graph: Dict[Node, list[Node]], node: Node, domains: Dict[Node, set[str]] = {}, assigned = {}) -> Dict[Node, str]:
  for value in domains[node]:
    domains_copy = dict(domains)

    fc_failed = False
    for adjecent in graph[node]:
      if (adjecent in assigned):
        continue
      domains[adjecent].discard(value)
      if (len(domains[adjecent]) == 0):
        fc_failed = True
        break
    
    if (fc_failed):
      domains = domains_copy
    
    print("recursed")
    assigned[node] = value

    if (len(assigned) == len(graph)):
      return assigned

    for adjecent in graph[node]:
      if (adjecent in assigned):
        continue
      
      result = backtrack(graph, adjecent, domains, assigned)

      if (result):
        return result
      else:
        break

  return None

domains = {}
for node in graph_large.keys():
  domains[node] = set(domain)

assignment = backtrack(graph_large, 'A', domains)
visualize_graph(graph, assignment)