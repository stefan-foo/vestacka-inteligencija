from queue import PriorityQueue
from pprint import pprint
from functools import reduce
import operator
import math
import heapq as heap
import time

State = list[int] | tuple[int]

def get_initial_state() -> State:
  return (1, 0, 0,
          0, 0, 0,
          0, 0, 3)

def state_is_goal(state: State) -> bool:
  n = int(math.sqrt(len(state)))
  sum = n * (n * n + 1) / 2
  for i in range(n):
    row_sum = col_sum = 0
    for j in range(n):
      row_sum += state[i * n + j]
      col_sum += state[n * j + i]
    if col_sum != sum or row_sum != sum:
      return False
  return True

def a_star(state: State) -> list[tuple[State]] | None:
    p_queue = PriorityQueue()
    
    p_queue.put( ( 0, state ) )
    came_from = { state: None }
    g = { state: 0 }

    # heap.heappush(state, 0)

    goal_found = False
    while not p_queue.empty():
      _, current = p_queue.get()

      if state_is_goal(current):
        goal_found = True
        break

      for child in children(current):
        cost_to_child = g[current] + 20
        if child not in g or g[child] < cost_to_child:
          g[child] = cost_to_child + 20
          priority = cost_to_child + heuristic_eval(child)
          came_from[child] = current
          p_queue.put((priority, child))

    if (goal_found):
      path = []
      prev = current
      while (prev):
        path.append(prev)
        prev = came_from[prev]
      path.reverse()
      return path
    else:
      return None


def derive_state(state: State, index: int, value: int) -> State:
  derived_state = list(state)
  derived_state[index] = value
  return tuple(derived_state)

def is_valid(state: State) -> bool:
  n = int(math.sqrt(len(state)))
  sum = n * (n * n + 1) / 2
  for i in range(n):
    row_sum = col_sum = 0
    for j in range(n):
      row_ind = i * n + j
      col_ind = n * j + i
      row_sum += state[row_ind]
      col_sum += state[col_ind]
    if col_sum > sum or row_sum > sum:
      return False
  return True

def children(state: State) -> list[State]:
  n = len(state)

  for num in set(range(1, n + 1)).difference(set(state)):
    # index = state.index(0)
    # child = derive_state(state, index, num)
    # yield child  
    for i in range(len(state)):

      if state[i] == 0:
        child_state = derive_state(state, i, num)
        if (is_valid(child_state)):
          yield child_state

def heuristic_eval(state: State) -> int:
  n = int(math.sqrt(len(state)))
  eval = (len(state) - len(set(state)) - 1) * 20
  # eval = 0
  for i in range(n):
    groups_rows = [0] * n
    groups_cols = [0] * n
    for j in range(n):
      row_i = i * n + j
      col_i = j * n + i
      if (state[row_i] != 0):
        groups_rows[(state[row_i]-1) // n] += 1
      if (state[col_i] != 0):
        groups_cols[(state[col_i]-1) // n] += 1
    eval = reduce(operator.add, filter(lambda x: x > 1, groups_rows + groups_cols), eval)
  return eval

result = a_star(get_initial_state())
if result:
  for node in result:
    print(f"{node[0:3]}\n{node[3:6]}\n{node[6:9]}\n========")
