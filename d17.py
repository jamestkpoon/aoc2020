import sys
import numpy as np
from d3 import to_binary_map

def in_bounds(coord, shape):
    return np.all(np.logical_and(coord >= 0, coord < np.asarray(shape)))

def iterate(world):
    out_ = np.zeros(np.asarray(world.shape) + 2, dtype=np.bool)
    for world_coord in np.ndindex(*out_.shape):
        world_coord_old_ = np.asarray(world_coord) - 1
        active_neighbors_ = 0
        for neighbor_coord in np.ndindex(*([ 3 ] * len(world.shape))):
            neighbor_coord_ = np.asarray(neighbor_coord) - 1
            if np.all(neighbor_coord_ == 0): continue
            neighbor_world_coord_ = neighbor_coord_ + world_coord_old_
            if not in_bounds(neighbor_world_coord_, world.shape): continue
            if world[tuple(neighbor_world_coord_)]: active_neighbors_ += 1

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
        
    for i in range(6):
        world_ = iterate(world_)
    out_ = np.sum(world_)
        
    print(out_)
    