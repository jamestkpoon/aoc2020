import sys
import numpy as np
from d3 import to_binary_map

def in_bounds(coord, shape):
    return np.all(np.logical_and(coord >= 0, coord < np.asarray(shape)))
    
def gen_neighbors(nd):
    out_ = []
    for n in np.ndindex(*([ 3 ] * nd)):
        if n.count(1) < nd: out_.append(n)
    
    return np.asarray(out_) - 1

def iterate(world, local_neighbors):
    out_ = np.zeros(np.asarray(world.shape) + 2, dtype=np.bool)
    for world_coord in np.ndindex(*out_.shape):
        world_coord_old_ = np.asarray(world_coord) - 1
        
        active_neighbors_ = 0
        for n in filter(lambda c: in_bounds(c, world.shape), world_coord_old_ + local_neighbors):
            if world[tuple(n)]: active_neighbors_ += 1
            
        if in_bounds(world_coord_old_, world.shape):
            if world[tuple(world_coord_old_)]:
                if active_neighbors_ == 2 or active_neighbors_ == 3:
                    out_[world_coord] = True
            elif active_neighbors_ == 3: out_[world_coord] = True
        elif active_neighbors_ == 3: out_[world_coord] = True
        
    return out_

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        data_ = f.read().splitlines()

    if sys.argv[2] == '1':
        world_ = to_binary_map(data_)[np.newaxis,:,:]
    elif sys.argv[2] == '2':
        world_ = to_binary_map(data_)[np.newaxis,np.newaxis,:,:]
        
    local_neighbors_ = gen_neighbors(len(world_.shape))
        
    for i in range(6):
        world_ = iterate(world_, local_neighbors_)
    out_ = np.sum(world_)
        
    print(out_)
    