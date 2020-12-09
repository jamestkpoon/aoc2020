import sys

def binary_split(lb_inclusive, ub_exclusive, splitting_seq, splitting_keys):
    bounds_ = [ lb_inclusive, ub_exclusive ]
    for c in splitting_seq:
        half_diff_ = int((bounds_[1] - bounds_[0]) / 2)
        if c == splitting_keys[0]:
            bounds_[1] -= half_diff_
        elif c == splitting_keys[1]:
            bounds_[0] += half_diff_
    
    return bounds_[0] if bounds_[1] - bounds_[0] == 1 else None     
    
def get_seat_id(splitting_seq):
    r_ = binary_split(0, 128, splitting_seq[:-3], [ 'F', 'B' ])
    c_ = binary_split(0, 8, splitting_seq[-3:], [ 'L', 'R' ])
    if r_ is not None and c_ is not None:
        return r_*8 + c_
    else: return None

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        data_ = f.read().splitlines()
 
    if sys.argv[2] == '1':
        out_ = 0
        for d in data_:
            id_ = get_seat_id(d)
            if id_ is not None: out_ = max(out_, id_)
    elif sys.argv[2] == '2':
        id_all_ = []
        for d in data_:
            id_ = get_seat_id(d)
            if id_ is not None: id_all_.append(id_)
                
        out_ = None
        for i in range(8, 127*8):
            if i not in id_all_:
                out_ = i
                break
            
    print(out_)