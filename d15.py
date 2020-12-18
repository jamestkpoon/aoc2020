import sys
from copy import deepcopy

def play(seed, stopN):
    series_ = deepcopy(list(seed))
    
    dict_ = {}
    for i in range(len(series_)):
        dict_[series_[i]] = [ i ]
        
    turn_idx_ = len(series_) - 1
    while len(series_) != stopN:
        turn_idx_ += 1
        prev_number_ = series_[-1]
        if prev_number_ not in dict_.keys(): series_.append(0)
        elif len(dict_[prev_number_]) < 2: series_.append((turn_idx_ -1) - dict_[prev_number_][-1])
        else: series_.append(dict_[prev_number_][-1] - dict_[prev_number_][-2])
        
        if series_[-1] in dict_.keys(): dict_[series_[-1]].append(turn_idx_)
        else: dict_[series_[-1]] = [ turn_idx_ ]

    return series_[-1]
    

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        data_ = f.read().splitlines()
        
    input_ = list(map(int, data_[0].split(',')))
    out_ = play(input_, int(sys.argv[3]))

    print(out_)
    
