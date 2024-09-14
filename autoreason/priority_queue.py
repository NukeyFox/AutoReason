from __future__ import annotations 
from typing import TypeVar, Iterable, Generic, Callable, Any, Optional, Callable, List, Union
from typing_extensions import Self
from abc import ABC, abstractmethod
T = TypeVar('T')

class EmptyPriorityQueue(Exception):
    def __init__(self):
        super.__init__("Trying to extract from empty priority queue.")

class ItemNotExists(Exception):
    def __init__(self):
        super.__init__("Item doesn't exist in priority queue.")

class PriorityQueueAbstract(Generic[T]):
    @abstractmethod
    def __init__(self, max_size : Optional[int] = None):
        pass 
    
    @abstractmethod
    def insert(self, item : T, priority : float | int ) -> bool:
        pass 
    
    @abstractmethod
    def get_min(self) -> Optional[T]:
        pass 
    
    @abstractmethod
    def delete_min(self) -> None:
        pass 
    
    @abstractmethod
    def change_priority(self, item : T, new_priority : float | int) ->  bool:
        pass 
    
    @abstractmethod
    def empty(self) -> bool:
        pass 
    
    @abstractmethod
    def __contains__(self, item : T) -> bool:
        pass
    
    
class PQNode(Generic[T]):
    @abstractmethod
    def __init__(self, val : T, priority : float, children : set[Self]):
        self._children = children
        self._val = val
        self._priority = priority
        
    def __str__(self):
        return self._val.__str__()
    
    def __repr__(self):
        return self._val.__repr__() + str([child for child in self._children]) 
    
class FibNode(PQNode[T]):
    def __init__(self, val, priority : float, children : set[FibNode[T]]):
        super().__init__(val, priority, children )
        self._marked : bool = False
        self._parent : Optional[FibNode[T]] = None
    
  
class FibonacciHeap(PriorityQueueAbstract[T]):
   
    def __init__(self, max_size : Optional[int] = None):
        self._tree_list : List[FibNode[T]]= []
        self._hash : dict[T,FibNode[T]] = {}
        self._min_priority : Optional[int | float] = None
        self._min : Optional[T] = None
        
    def insert(self, item : T, priority : float | int) -> bool:
        if self._min_priority is None or priority < self._min_priority:
            self._min_priority = priority
            self._min = item 
    
        if item not in self._hash:
            node : FibNode[T] = FibNode(item, priority, set())
            self._hash[item] = node
            self._tree_list.append(node)
            return True
        else:
            return self.change_priority(item, priority)
    
    def get_min(self) -> Optional[T]:
        return self._min
    
    def delete_min(self) -> None:
        if self._min is not None:
            min_node = self._hash[self._min]
            for child in min_node._children:
                self._tree_list.append(child)
            self._tree_list.remove(min_node)
            del self._hash[self._min] 
            self._min_priority = None
            self._min = None
            
            if self.empty():
                return 
            
            node_hash : dict[int, Optional[FibNode[T]]]= {}
            for node in self._tree_list:
                curr_node : FibNode[T] = node
                degree = len(curr_node._children)
                
                while degree in node_hash and node_hash[degree] is not None: 
                    curr_node = self._merge(node_hash[degree], node) # type: ignore
                    node_hash[degree] = None
                    degree = len(curr_node._children)
                else:
                    node_hash[degree] = curr_node
                    
            for node in self._tree_list:
                if self._min_priority is None or node._priority < self._min_priority:
                    self._min_priority = node._priority
                    self._min = node._val
        else:
            raise EmptyPriorityQueue()

    def _pop(self, node : FibNode[T]) -> None:
        parent = node._parent
        if parent is not None:
            node._parent = None
            self._tree_list.append(node)
            if not parent._marked:
                    parent._marked = True 
            else:
                self._pop(parent)

    def change_priority(self, item : T, new_priority : float) -> bool:
        if item not in self._hash:
            raise Exception("Item doesn't exist")
        node = self._hash[item]
        node._priority = new_priority
        self._pop(node)      
        if self._min_priority is None or node._priority < self._min_priority:
                self._min_priority = node._priority
                self._min = node._val  
                return True 
        return False
    
    def empty(self) -> bool:
        return len(self._tree_list) == 0 
    
    def _merge(self, node1 : FibNode[T], node2 : FibNode[T]) -> FibNode:
        if node1._priority < node2._priority:
            node1._children.add(node2)
            self._tree_list.remove(node2)
            node2._parent = node1
            return node1
        else:
            node2._children.add(node1)
            self._tree_list.remove(node1)
            node1._parent = node2
            return node2
 
    def __contains__(self, item : T) -> bool:
        return item in self._hash
    
class PairNode(PQNode[T]):
    def __init__(self, val : T, priority : float, children : set[PairNode[T]]):
        super().__init__(val, priority, children)
        self._parent : Optional[PairNode[T]] = None

class PairingHeap(PriorityQueueAbstract[T]):
    def __init__(self, max_size : Optional[int] = None):
        self._root : Optional[PairNode[T]] = None
        self._hash : dict[T,PairNode[T]] = {}
        

    def insert(self, item : T, priority : float | int ) -> bool:
        if item not in self._hash:
             node = PairNode(item, priority, set())
             self._root = self._merge(node, self._root)
             self._hash[item] = node
             return True
        else:
            return self.change_priority(item, priority)
       
    
    def get_min(self) -> Optional[T]:
        if self._root is None:
            raise EmptyPriorityQueue()
        else:
            return self._root._val
    
    def _merge(self, heap1 : Optional[PairNode[T]], heap2 : Optional[PairNode[T]]) -> Optional[PairNode[T]]:
        if heap1 is None:
            return heap2 
        elif heap2 is None:
            return heap1
        elif heap1._priority < heap2._priority:
            heap1._children.add(heap2)
            heap2._parent = heap1
            return heap1 
        else:
            heap2._children.add(heap1)
            heap1._parent = heap2
            return heap2

    def delete_min(self) -> None:
        if self._root is None:
            raise EmptyPriorityQueue()
        else:
            children = self._root._children
            del self._hash[self._root._val]
            self._root = self._merge_pair(children)
        
    def _merge_pair(self, children : set[PairNode[T]]) -> Optional[PairNode[T]]:
        if len(children) == 0:
            return None
        elif len(children) == 1:
            n = children.pop()
            n._parent = None
            return n
        else:
            n0 = children.pop()
            n1 = children.pop()
            n0._parent = None
            n1._parent = None
            return self._merge(self._merge(n0,n1), self._merge_pair(children))
    
    def change_priority(self, item : T, new_priority : float | int) ->  bool:
        node = self._hash[item]
        parent = node._parent
        old_priority = node._priority
        node._priority = new_priority
        if parent is not None:
            parent._children.remove(node)
        self._root = self._merge(node, self._root)
        return old_priority > new_priority
            
    def empty(self) -> bool:
        return self._root is None
    
    def __contains__(self, item : T) -> bool:
        return item in self._hash
    
if __name__ == "__main__":
    pq : PairingHeap[str] = PairingHeap()
    pq.insert("hello", 5)
    pq.insert("world",3)
    pq.insert("this",2)
    pq.insert("twist",1)
    print(pq.get_min())
    pq.change_priority("hello", 10)
    print(pq.get_min())
    pq.delete_min()
    print(pq.get_min())