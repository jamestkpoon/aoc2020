import sys
from collections import Counter
import numpy as np

FLOORSPACE_VALUE = 0
EMPTY_SEAT_VALUE = 1
OCCUPIED_SEAT_VALUE = 2

def parse_seats(strs, floorspace='.', empty_seat='L', occupied_seat='#'):
    out_ = np.empty([ len(strs), len(strs[0]) ], dtype=np.uint8)
    for r in range(out_.shape[0]):
        for c in range(out_.shape[1]):
            if strs[r][c] == floorspace: out_[r,c] = FLOORSPACE_VALUE
            elif strs[r][c] == empty_seat: out_[r,c] = EMPTY_SEAT_VALUE
            elif strs[r][c] == occupied_seat: out_[r,c] = OCCUPIED_SEAT_VALUE
            else: print("Got unrecognized character " + strs[r][c])

    return out_

def get_immediate_neighbors(map_, _r,_c):
    out_ = []
    for r in range(_r-1, _r+2):
        if r < 0 or r >= map_.shape[0]: continue
        for c in range(_c-1, _c+2):
            if c < 0 or c >= map_.shape[1] or (r == _r and c == _c): continue
            out_.append(map_[r,c])

    return out_

def get_raycast_neighbors(map_, _r,_c):
    def within_bounds(coord):
        if np.any(coord < 0): return False
        elif not np.all(coord < map_.shape): return False
        else: return True

    out_ = []
    origin_ = [ _r, _c ]
    for n in np.ndindex(3,3):
        if n == (1,1): continue
        step_ = np.asarray(n) - 1
        pos_ = np.array(origin_, copy=True)
        while True:
            pos_ += step_
            if not within_bounds(pos_): break
            if map_[pos_[0], pos_[1]] != FLOORSPACE_VALUE:
                out_.append(map_[pos_[0], pos_[1]])
                break
        
    return out_

def iterate(map_, get_neighbors_fn, occupied_seat_threshold):
    out_ = map_.copy()
    for r in range(map_.shape[0]):
        for c in range(map_.shape[1]):
            if map_[r,c] == FLOORSPACE_VALUE: continue
            neighbors_ = get_neighbors_fn(map_, r,c)
            counter_ = Counter(neighbors_)
            if map_[r,c] == EMPTY_SEAT_VALUE:
                if counter_[OCCUPIED_SEAT_VALUE] == 0:
                    out_[r,c] = OCCUPIED_SEAT_VALUE
            elif map_[r,c] == OCCUPIED_SEAT_VALUE:
                if counter_[OCCUPIED_SEAT_VALUE] >= occupied_seat_threshold:
                    out_[r,c] = EMPTY_SEAT_VALUE

    return out_

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        data_ = f.read().splitlines()

    initial_seating_map_ = parse_seats(data_)
    neighbors_fn_ = get_immediate_neighbors if sys.argv[2] == '1' else get_raycast_neighbors
    occupied_seat_threshold_ = int(sys.argv[3])

    out_ = None
    last_map_ = initial_seating_map_
    while True:
        map_ = iterate(last_map_, neighbors_fn_, occupied_seat_threshold_)
        if np.array_equal(map_, last_map_):
            out_ = sum(map_.ravel() == OCCUPIED_SEAT_VALUE)
            break
        last_map_ = map_

    print(out_)
    