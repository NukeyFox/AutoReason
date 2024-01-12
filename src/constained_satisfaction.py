from __future__ import annotations 
from typing import TypeVar, Iterable, Mapping, Generic, Collection, Callable, FrozenSet, Any, Set, Dict, Optional, Callable, List, Union
from typing_extensions import Self
from collections.abc import Collection
from abc import ABC, abstractmethod
from search import Searcher #type: ignore
T = TypeVar('T')
U = TypeVar('U')
State = FrozenSet[Dict[U,T]]
# Uniform constraint solving
# Forward propagation
# Arc consistency

class NoSolutionError(Exception):
    pass 


class ConstraintSolverBase(Generic[T,U]):
    def __init__(self, 
                variables   : Collection[U],
                domains     : Mapping[U, Collection[T]],
                constraints : Callable[[U, T, U, T], bool]):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.count = len(variables)
       
    def find_solution(self) -> Dict[U,T] | None:
        return self.backtrack({})   

    def backtrack(self, assignment):
            #Code copied from Geeks for Geeks: https://www.geeksforgeeks.org/constraint-satisfaction-problems-csp-in-artificial-intelligence/
        if len(assignment) == len(self.variables): 
            return assignment 

        var = self.select_unassigned_variable(assignment) 
        for value in self.order_domain_values(var, assignment): 
            if self.is_consistent(var, value, assignment): 
                assignment[var] = value 
                result = self.backtrack(assignment) 
                if result is not None: 
                    return result 
                del assignment[var] 
        return None
       
        
    def select_unassigned_variable(self, assignment : Dict[U,T]) -> U:
        unassigned_vars = [var for var in self.variables if var not in assignment] 
        return min(unassigned_vars, key=lambda var: len(self.domains[var])) 

    def order_domain_values(self, var : U, assignment : Dict[U,T]) -> Collection[T]:
        return self.domains[var] 
    
    def is_complete(self, assignment : Dict[U,T]) -> bool:
        return len(assignment) == len(self.variables)

    def is_consistent(self, var, value, assignment): 
        #Code copied from Geeks for Geeks
        for var1 in assignment: 
            if not self.constraints(var, value, var1, assignment[var1]):
                return False
        return True



if __name__ == "__main__":
    puzzle = [[5, 3, 0, 0, 7, 0, 0, 0, 0], 
          [6, 0, 0, 1, 9, 5, 0, 0, 0], 
          [0, 9, 8, 0, 0, 0, 0, 6, 0], 
          [8, 0, 0, 0, 6, 0, 0, 0, 3], 
          [4, 0, 0, 8, 0, 3, 0, 0, 1], 
          [7, 0, 0, 0, 2, 0, 0, 0, 6], 
          [0, 6, 0, 0, 0, 0, 2, 8, 0], 
          [0, 0, 0, 4, 1, 9, 0, 0, 5], 
          [0, 0, 0, 0, 8, 0, 0, 0, 0] 
          ] 
  
    def print_sudoku(puzzle): 
        for i in range(9): 
            if i % 3 == 0 and i != 0: 
                print("- - - - - - - - - - - ") 
            for j in range(9): 
                if j % 3 == 0 and j != 0: 
                    print(" | ", end="") 
                print(puzzle[i][j], end=" ") 
            print() 
  
    print_sudoku(puzzle) 
    variables = [(i, j) for i in range(9) for j in range(9)] 
    # Domains 
    Domains   = {var: set(range(1, 10)) if puzzle[var[0]][var[1]] == 0 
                            else {puzzle[var[0]][var[1]]} for var in variables} 
    
    constraints = {}
    def add_constraint(var): 
        constraints[var] = [] 
        for i in range(9): 
            if i != var[0]: 
                constraints[var].append((i, var[1])) 
            if i != var[1]: 
                constraints[var].append((var[0], i)) 
        sub_i, sub_j = var[0] // 3, var[1] // 3
        for i in range(sub_i * 3, (sub_i + 1) * 3): 
            for j in range(sub_j * 3, (sub_j + 1) * 3): 
                if (i, j) != var: 
                    constraints[var].append((i, j)) 
    for i in range(9): 
        for j in range(9): 
            add_constraint((i, j))
    def consr(p1, v1, p2, v2):
        return (not p2 in constraints[p1]) and (v1 != v2)

    csp = ConstraintSolverBase(
        variables,
        Domains,
        consr
    )
    print(csp.find_solution())