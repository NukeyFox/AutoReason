from typing import TypeVar, Iterable, Generic, Callable, Any, Self, Optional, Callable, List
from abc import ABC, abstractmethod
from src.priority_queue import FibonacciHeap

T = TypeVar('T')
U = TypeVar('U')

from typing import Protocol, TypeVar

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
        self._pq : FibonacciHeap[T] = FibonacciHeap()
        self.start_state = start_state
        self._pq.insert(start_state,cost_func(start_state))
        self._next_state_func = next_state_func
        self._goal_test_func = goal_test_func
        self._cost_func = cost_func
        self._curr_state = start_state
        self.distance : dict[T,int | float] = {}
        self.distance[self.start_state] = float("inf")
        if edge_weights is None:
            self.edge_weights : Callable[[T,T],float|int] = lambda a, b : 1 #constant function
        else:
            self.edge_weights = edge_weights
    
    def expand_state(self) -> None:
        next_states = self._next_state_func(self._curr_state)
        for s in next_states:
            self.insert(s)
    
    def at_goal_state(self) -> bool:
        if self._curr_state is None:
            return False
        else:
            return self._goal_test_func(self._curr_state)
        
    def insert(self, item : T) -> None:
        self._pq.insert(item, self._cost_func(item))
    
    def search_return_answer(self) -> bool:
        while not self._pq.empty():
            if self.at_goal_state():
                return True
            else:
                state : Optional[T] = self._pq.get_min()
                if state is None:
                    return False #Accessing empty queue
                if state not in self.distance:
                    self._curr_state = state
                    self.expand_state()
                    self._pq.delete_min()
        else: 
            return False
    
    def search_return_path(self) -> List[T]:
        pass 

if __name__ == "__main__":
    edge_weights = {}
    edge_weights[(0,1)] = 1
    edge_weights[(1,2)] = 1
    edge_weights[(0,2)] = 2
    def next_state_func(n):
        match n:
            case 0: return [1,2]
            case 1: return [2]
            case 2: return []
    def goal_test(n):
        return n == 2
    
            
    
    