
#extend-protocol StructurePathComposer
  #Object
  #(comp-structure-paths* [sp]
    #sp)
  #java.util.List
  #(comp-structure-paths* [structure-paths]
    #(reduce (fn [sp-curr sp]
              #(reify StructurePath
                #(select* [this structure next-fn]
                  #(select* sp-curr structure
                           #(fn [structure-next]
                             #(select* sp structure-next next-fn)))
                  #)
                #(update* [this structure next-fn]
                  #(update* sp-curr structure
                           #(fn [structure-next]
                             #(update* sp structure-next next-fn))))
                #))
          #(-> structure-paths flatten))
    #))


def mapcat(f, seq):
    return reduce(lambda x,y: x+y, map(f, seq))

class BaseObject(object):
    pass
   

def compose_selectors(sp_curr, sp):
    o = BaseObject()
    o.select_path = lambda structure, next_fn: sp_curr.select_path(structure, lambda structure_next: sp.select_path(structure_next, next_fn))
    o.update_path = lambda structure, next_fn: sp_curr.update_path(structure, lambda structure_next: sp.update_path(structure_next, next_fn))
    print o
    print o.select_path
    return o

    

def comp_paths(selector):
    if isinstance(selector, list):
        print selector
        return reduce(compose_selectors, selector) 
    else:
        return selector
        
def select(selector, structure):
    s = comp_paths(selector).select_path(structure, lambda x: [x])
    return s

def update(selector, update_fn, structure):
    return comp_paths(selector).update_path(structure, update_fn)



class KeyPath:
    def __init__(self, key):
        self.key = key
    
    def select_path(self, structure, next_fn):
        return next_fn(structure[self.key]) 

    def update_path(self, structure, update_fn):
        # TODO immutable data structures
        structure_copy = structure.copy()
        structure_copy[self.key] = update_fn(structure[self.key])
        return structure_copy
        

class AllPath:
    def select_path(self, structure, next_fn):
        return mapcat(next_fn, structure) 

    def update_path(self, structure, update_fn):
        return map(update_fn, structure)

class FilterPath:
    def __init__(self, function):
        self.function = function

    def select_path(self, structure, next_fn):
        if self.function(structure):
            return next_fn(structure) 
        else:
            return []

    def update_path(self, structure, update_fn):
        if self.function(structure):
            return update_fn(structure)
        else:
            return structure 

    
ALL = AllPath()

def is_even(x):
    return x%2==0

def main():
    #structure = {"A": {"B": {"C": 1}}}
    structure = {"A": [1,2,3,4]}

    #print select([KeyPath("A"), KeyPath("B"), KeyPath("C")], structure)
    print select([KeyPath("A"), ALL, FilterPath(is_even)], structure) 
    print update([KeyPath("A"), ALL, FilterPath(is_even)], lambda x: x+1, structure)

    
if __name__ == '__main__':
    main()

#["A" ALL even?]

#["A" even?]

#structure = {"A": [1, 2, 3, 4]}

#mapcat(lambda x: if x%2==0: [x] else: [], structure["A"])










