from typing import Dict
from pprint import pprint
import copy

def generate_graph(n: int) -> Dict[int, list[int]]:
  edges = set(range(n))
  return { key: list(set(edges) ^ set([key])) for key in range(n) }

def derive_new_domains(
  graph: Dict[int, list[int]], 
  domains: Dict[int, set[int]], 
  exclude: Dict[int, int], 
  variable: int, 
  val: int
) -> None | list[tuple[int, set[int]]]:

  domains = copy.deepcopy(domains)
  n = len(domains)

  for a_var in graph[variable]:
    if (a_var in exclude):
      continue
    dif = abs(a_var - variable)
    domains[a_var].discard(val)
    domains[a_var].discard(val + dif)
    domains[a_var].discard(val - dif)
    if (len(domains[a_var]) == 0):
      return None

  return domains

def backtracking_recursive_mrv_fc(
  graph: Dict[int, list[int]], 
  domains: Dict[int, set[int]], 
  assigned: Dict[int, int] = {}
) -> Dict[int, int]:
  n = len(domains)

  mrv_variable = None
  for variable in domains.keys():
    if (variable in assigned):
      continue
    if (mrv_variable == None or len(domains[mrv_variable]) > len(domains[variable])):
      mrv_variable = variable
      
  if (mrv_variable == None):
    return assigned

  values = domains[mrv_variable]
  for value in values:
    assigned[mrv_variable] = value

    new_domains = derive_new_domains(graph, domains, assigned, mrv_variable, value)
    
    if (new_domains):
      result = backtracking_recursive_mrv_fc(graph, new_domains, assigned)
      if (result):
        return result
  assigned.pop(mrv_variable)

  return None

n = 8
graph = generate_graph(n)

variable_domain = {i for i in range(n)}
domains = dict()
for key in graph.keys():
  domains[key] = copy.copy(variable_domain)

assignments = backtracking_recursive_mrv_fc(graph, domains)
for i in range(n):
  for j in range(n):
    print("[Q]" if assignments[i] == j else "[ ]", end="")
  print()