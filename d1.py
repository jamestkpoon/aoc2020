import sys
import numpy as np

def filter_let(l, let):
    return list(filter(lambda x: x <= let, l))
    
def get_unique_index_sets(l, n):
    # full axis sets
    ranges_ = [ range(l) for i in range(n) ]
    axes_ = np.mgrid[ranges_].T.reshape(-1,n)
    # only keep sets with all unique values
    axes_ = np.asarray(list(filter(lambda r: len(set(r)) == n, axes_)))
    # sort columns and then keep unique rows
    axes_ = np.unique(np.sort(axes_, axis=1), axis=0)
    
    return axes_
    
def find_n_values_that_sum_to(l, n, v):
    for I in get_unique_index_sets(len(l), n):
        l_ = [ l[i] for i in I ]
        if sum(l_) == v: return l_
        
    return None
        
if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        ints_ = list(map(int, f.readlines()))
    
    n_ = int(sys.argv[2])
    sum_target_ = int(sys.argv[3])
    
    ints_filtered_ = filter_let(ints_, sum_target_)
    v_ = find_n_values_that_sum_to(ints_filtered_, n_, sum_target_)
    print([ v_, np.prod(v_) ])
