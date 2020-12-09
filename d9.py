import sys
from d1 import find_n_values_that_sum_to

def find_value_that_doesnt_sum_from_prev(ints, candidates_length, n):
    for i in range(candidates_length, len(ints)):
        if find_n_values_that_sum_to(ints[i-candidates_length:i], n, ints_[i]) is None:
            return i, ints[i]

    return None

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        data_ = f.read().splitlines()
        
    ints_ = list(map(int, data_))

    if sys.argv[2] == '1':
        out_ = find_value_that_doesnt_sum_from_prev(ints_, int(sys.argv[3]), int(sys.argv[4]))
    elif sys.argv[2] == '2':
        idx_from_last_ = int(sys.argv[3])
        found_ = False

        for i in range(idx_from_last_-2):
            for j in range(i+2, idx_from_last_):
                candidates_ = ints_[i:j]
                if sum(candidates_) == ints_[idx_from_last_]:
                    out_ = min(candidates_) + max(candidates_)
                    found_ = True
                    break
            if found_: break

    print(out_)
    
