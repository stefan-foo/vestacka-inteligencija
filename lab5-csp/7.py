from typing import Dict
from pprint import pprint
import copy

directions = [(1, 0), (1, 1), (1, -1), (-1, 1), (-1, 0), (-1, -1)]

def generate_graph(n: int) -> Dict[int, list[int]]:
  edges = set(range(n))
  return { key: list(set(edges) ^ set([key])) for key in range(n) }

def derive_new_domains(domains: list[tuple[int, set[int]]], exclude: Dict[int, int], variable: int, val: int) -> None | list[tuple[int, set[int]]]:
  domains = copy.deepcopy(domains)
  n = len(domains)

  for cx, cy in directions:
    row = variable + cx
    column = val + cy

    while (0 <= row < n and 0 <= column < n):
      if row not in exclude:
        domains[row][1].discard(column)
      if (len(domains[row][1]) == 0):
        return None
      row += cx
      column += cy

  return domains

def backtracking_recursive_mrv_fc(
  graph: Dict[int, list[int]], 
  domains: list[tuple[int, set[int]]], 
  assigned: Dict[int, int] = {}
) -> Dict[int, int]:
  n = len(domains)

  mrv_domain = None
  for domain in domains:
    if (domain[0] in assigned):
      continue
    if (mrv_domain == None or len(domain[1]) < len(mrv_domain[1])):
      mrv_domain = domain

  if (mrv_domain == None):
    return assigned

  variable, values = mrv_domain

  for value in values:
    assigned[variable] = value

    new_domains = derive_new_domains(domains, assigned, variable, value)
    
    if (new_domains):
      result = backtracking_recursive_mrv_fc(graph, new_domains, assigned)
      if (result):
        return result

  assigned.pop(variable)

  return None

n = 8
graph = generate_graph(n)
variable_domain = [i for i in range(n)]

domains = []
for key in graph.keys():
  domains.append((key, set(variable_domain)))

assignments = backtracking_recursive_mrv_fc(graph, domains)
if (assignments):
  for i in range(n):
    for j in range(n):
      print("[Q]" if assignments[i] == j else "[ ]", end="")
    print()