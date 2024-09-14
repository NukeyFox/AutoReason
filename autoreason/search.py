from typing import TypeVar, Iterable, Generic, Callable, Dict, Set, Any, Optional, Callable, List
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
                 goal_test_func  : Callable[[T],bool],
                 cost_func       : Optional[Callable[[T],float | int]] = None,
                 skip_condition  : Optional[Callable[[T], bool]] = None, 
                 edge_weights    : Optional[Callable[[T,T],float|int]] = None):
        self._pq : PairingHeap[T] = PairingHeap()
        self.start_state = start_state
        self._next_state_func = next_state_func
        self._goal_test_func = goal_test_func
        self._cost_func = lambda x : 0 if cost_func is None else cost_func
        self._pq.insert(start_state,self._cost_func(start_state))
        self._curr_state = start_state
        self.visited : Set[T] = set()
        self.edge_weights   : Callable[[T,T],float|int] = (lambda a, b : 1) if edge_weights is None else edge_weights
        self.skip_condition : Callable[[T], bool] 
        if skip_condition is None:
            self.skip_condition = (lambda x : False)
        else:
            self.skip_condition = skip_condition
        self.perform_backtracking = False
        self.backtrack_dict : Dict[T,T] = {}
    
    def expand_state(self) -> None:
        next_states = self._next_state_func(self._curr_state)
        for s in next_states:
            if s not in self.visited:
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
    
    def search_return_answer(self, verbose = False) -> Optional[T]:
        self.perform_backtracking = False
        self.visited.clear()
        
        while not self._pq.empty():
            
            state : Optional[T] = self._pq.get_min()
            if verbose: print(state)
            if state is None:
                return None #Accessing empty queue
            self._curr_state = state

            if self.at_goal_state():
                return self._curr_state
            
            skip = self.skip_condition(self._curr_state)
            if skip:
                self._pq.delete_min()
                continue

            
            if state not in self.visited:
                
                self.visited.add(state)
                self.expand_state()
                self._pq.delete_min()
        else: 
            return self._curr_state if self.at_goal_state() else None
        
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
            
            if self.skip_condition(self._curr_state):
                continue
            
            if state not in self.visited:
                self.visited.add(state)
                self.expand_state()
                self._pq.delete_min()
        else: 
            return []

if __name__ == "__main__":
    def next_state_func(n):
        match n:
            case 0: return [1,3]
            case 1: return [0,2]
            case 2: return [1]
            case 3: return [2] 
        
    def goal_test(n):
        return n == 2
    s = Searcher(0,
                 next_state_func,
                 goal_test,
                 lambda x : 1)
    k = 3
    print(k)
   
    
            
    
    