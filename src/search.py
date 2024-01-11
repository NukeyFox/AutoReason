from typing import TypeVar, Iterable, Generic, Callable, Dict, Any, Optional, Callable, List
from abc import ABC, abstractmethod
from priority_queue import FibonacciHeap, PairingHeap #type: ignore

T = TypeVar('T')
U = TypeVar('U')


class Node(Generic[T]):
    def __init__(self, value : Any, cost = Optional[float]):
        self._value = value
        self._cost = cost
    
    @abstractmethod
    def cost(self) -> float:
        if self._cost is None:
            raise NotImplementedError
        else:
            return self._cost
    
    @abstractmethod
    def expand(self) -> Iterable["Node[U]"]:
        raise NotImplementedError
    
    @abstractmethod
    def is_goal(self) -> bool:
        raise NotImplementedError

class Searcher(Generic[T]): 
    def __init__(self, start_state : T, 
                 next_state_func : Callable[[T], Iterable[T]], 
                 goal_test_func : Callable[[T],bool],
                 cost_func : Callable[[T],float | int],
                 edge_weights : Optional[Callable[[T,T],float|int]] = None):
        self._pq : PairingHeap[T] = PairingHeap()
        self.start_state = start_state
        self._pq.insert(start_state,cost_func(start_state))
        self._next_state_func = next_state_func
        self._goal_test_func = goal_test_func
        self._cost_func = cost_func
        self._curr_state = start_state
        self.visited = set()
        if edge_weights is None:
            self.edge_weights : Callable[[T,T],float|int] = lambda a, b : 1 #constant function
        else:
            self.edge_weights = edge_weights
        self.perform_backtracking = False
        self.backtrack_dict = {}
    
    def expand_state(self) -> None:
        next_states = self._next_state_func(self._curr_state)
        for s in next_states:
            successful = self.insert(s)
            if self.perform_backtracking and successful:
                self.backtrack_dict[s] = self._curr_state
    
    def at_goal_state(self) -> bool:
        if self._curr_state is None:
            return False
        else:
            return self._goal_test_func(self._curr_state)

    def insert(self, item : T) -> bool:
        return self._pq.insert(item, self._cost_func(item))
    
    def search_return_answer(self) -> bool:
        self.perform_backtracking = False
        self.visited.clear()
        while not self._pq.empty():
            state : Optional[T] = self._pq.get_min()
            if state is None:
                return False #Accessing empty queue
            self._curr_state = state

            if self.at_goal_state():
                return True
            
            if state not in self.visited:
                self.visited.add(state)
                self.expand_state()
                self._pq.delete_min()
        else: 
            return self.at_goal_state()
    
    def search_return_path(self) -> List[T]:
        self.backtrack_dict.clear() 
        self.perform_backtracking = True
        self.visited.clear()

        def backtrack():
            path = []
            state = self._curr_state
            while state is not self.start_state:
                path.insert(0, state)
                state = self.backtrack_dict[state]
            path.insert(0,self.start_state)
            return path

        while not self._pq.empty():
            state : Optional[T] = self._pq.get_min()

            if state is None:
                return [] #Accessing empty queue
            self._curr_state = state
            if self.at_goal_state():
                return backtrack()
            if state not in self.visited:
                self.visited.add(state)
                self.expand_state()
                self._pq.delete_min()
        else: 
            return []

if __name__ == "__main__":
    pass
    
            
    
    