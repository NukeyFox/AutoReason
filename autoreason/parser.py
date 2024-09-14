from typing import TypeVar, Iterable, Generic, Callable


T = TypeVar('T')
U = TypeVar('U')
    
class ParseNode(Generic[T]):
    def __init__(self, item : T, children : Iterable["ParseNode[T]"]):
        self.item = item 
        self.children = children
        
    def nodeApply(self, func : Callable[[T],U]) -> "ParseNode[U]":
        newChildren : Iterable["ParseNode[U]"] = [child.nodeApply(func) for child in self.children] 
        return ParseNode[U](func(self.item), newChildren)
    
    def __str__(self) -> str:
        o = str(self.item) + "\n"
        for child in self.children:
            lines = str(child).splitlines()
            for line in lines:
                o += "| " + line + "\n"
        return o
            
    
class ParseTree(Generic[T]):
    def __init__(self, root : ParseNode[T]):
        self.root = root
        
    def treeMap(self, func : Callable[[T],U] ) -> "ParseTree[U]":
        newRoot = self.root.nodeApply(func)
        return ParseTree[U](newRoot)
    
    def __str__(self) -> str:
        return str(self.root)
        
class Parser:
    pass 

class LLkParser(Parser):
    def __init__(self, k : int):
        #checks grammer is from from left recursion
        #grammer is not ambiguous
        #gammar is left factored
        pass 
                
    def first(self):
         pass 
     
    def follow(self):
         pass    
                      
        
if __name__ == "__main__":
    pn1 = ParseNode[int](3,[])
    pn4 = ParseNode[int](7,[])
    pn2 = ParseNode[int](4, [pn1])
    pn3 = ParseNode[int](11, [pn2, pn4])
    pt = ParseTree[int](pn3)
    pu = pt.treeMap(lambda x : x * x)
    print(str(pt))
    print(str(pu))
    