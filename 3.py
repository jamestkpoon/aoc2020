import sys
import numpy as np

def to_binary_map(strs, key='#'):
    out_ = np.empty([ len(strs), len(strs[0]) ])
    for i in range(out_.shape[0]):
        for j in range(out_.shape[1]):
            out_[i,j] = 1 if strs[i][j] == key else 0
    
    return out_.astype(np.bool) 

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        data_ = f.read().splitlines()
        
    map_ = to_binary_map(data_)
    
    out_ = 1
    for s in sys.argv[2:]:
        step_ = list(map(int, s.split(',')))
        pos_ = [0,0]
        count_ = 0
        while pos_[0] < map_.shape[0]:
            if map_[pos_[0], pos_[1]]: count_ += 1
            pos_[0] += step_[0]
            pos_[1] = (pos_[1]+step_[1]) % map_.shape[1]
        
        out_ *= count_
            
    print(out_)
