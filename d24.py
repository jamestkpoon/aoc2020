import sys
import numpy as np

def parse_input(strs):
    outs_ = []
    for s in strs:
        out_ = []
        idx_ = 0
        while idx_ < len(s):
            l_ = 1 if s[idx_] == 'e' or s[idx_] == 'w' else 2
            out_.append(s[idx_:idx_+l_])
            idx_ += l_
        outs_.append(out_)
        
    return outs_
    
def navigate_hex_grid(sequence):
    pos_ = [ 0, 0 ]
    for step in sequence:
        if step == 'w': pos_[1] += 2
        elif step == 'e': pos_[1] -= 2
        else:
            if step[0] == 'n': pos_[0] += 1
            else: pos_[0] -= 1
            if step[1] == 'w': pos_[1] += 1
            else: pos_[1] -= 1
    
    return pos_
    
def get_list_of_tiles_to_flip(sequences):
    out_ = []
    for s in sequences:
        pos_ = navigate_hex_grid(s)
        if pos_ not in out_: out_.append(pos_)
        else: out_.remove(pos_)
        
    return out_
    
def get_neighbors(pos):
    return [ 
        [ pos[0] + 0, pos[1] + 2 ],
        [ pos[0] + 0, pos[1] - 2 ],
        [ pos[0] + 1, pos[1] + 1 ],
        [ pos[0] + 1, pos[1] - 1 ],
        [ pos[0] - 1, pos[1] + 1 ],
        [ pos[0] - 1, pos[1] - 1 ],
    ]
    
def is_valid_coord(pos):
    abs_ = np.abs(pos)
    if abs_[0]%2 != 0 and abs_[1]%2 == 0: return False
    elif abs_[0]%2 == 0 and abs_[1]%2 != 0: return False 
    else: return True
    
if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        data_ = f.read().splitlines()
    
    sequences_ = parse_input(data_)
    flip_list_ = get_list_of_tiles_to_flip(sequences_)

    if sys.argv[2] == '1':
        out_ = len(flip_list_)
    elif sys.argv[2] == '2':
        black_tiles_ = flip_list_
        for day in range(100):
            min_, max_ = np.min(black_tiles_, axis=0) - 1, np.max(black_tiles_, axis=0) + 2
            new_black_tiles_ = [ t for t in black_tiles_ ]
            for r in range(min_[0], max_[0]):
                for c in range(min_[1], max_[1]):
                    coord_ = [ r, c ]
                    if not is_valid_coord(coord_): continue
                    num_black_neighbors_ = np.sum([ n in black_tiles_ for n in get_neighbors(coord_) ])
                    if coord_ in black_tiles_ and (num_black_neighbors_ == 0 or num_black_neighbors_ > 2) and coord_ in new_black_tiles_: new_black_tiles_.remove(coord_)
                    elif coord_ not in black_tiles_ and num_black_neighbors_ == 2 and coord_ not in new_black_tiles_: new_black_tiles_.append(coord_)
                    
            black_tiles_ = new_black_tiles_
            
        out_ = len(black_tiles_)

    print(out_)
    