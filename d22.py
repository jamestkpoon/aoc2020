import sys

def parse_input(strs):
    outs_ = []
    
    line_idx_ = 0
    while line_idx_ < len(strs):
        line_idx_ += 1
        out_ = []
        
        while line_idx_ < len(strs) and len(strs[line_idx_]) != 0:
            out_.append(int(strs[line_idx_]))
            line_idx_ += 1
            
        outs_.append(out_)
        line_idx_ += 1
        
    return outs_
    
def combat(h1, h2):
    while len(h1) > 0 and len(h2) > 0:
        c1_, c2_ = h1.pop(0), h2.pop(0)
        if c1_ > c2_: h1 += [ c1_, c2_ ]
        else: h2 += [ c2_, c1_ ]
        
    return h1 if len(h1) > 0 else h2
    
def combat_evolved(h1, h2):
    history_ = []
    while len(h1) > 0 and len(h2) > 0:
        hash_ = hash(str([ h1 , h2 ]))
        if hash_ in history_: return [ h1, 1 ]
        else: history_.append(hash_)
    
        c1_, c2_ = h1.pop(0), h2.pop(0)
        
        if len(h1) >= c1_ and len(h2) >= c2_:
            h1_ = [ h1[i] for i in range(c1_) ]
            h2_ = [ h2[i] for i in range(c2_) ]
            winner_ = combat_evolved(h1_, h2_)
            if winner_[1] == 1: h1 += [ c1_, c2_ ]
            else: h2 += [ c2_, c1_ ]
        else:
            if c1_ > c2_: h1 += [ c1_, c2_ ]
            else: h2 += [ c2_, c1_ ]
        
    return [ h1, 1 ] if len(h1) > 0 else [ h2, 2 ]
    
def score(h):
    out_ = 0
    for i in range(1, len(h)+1):
        out_ += i * h[-i]
        
    return out_
        
if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        data_ = f.read().splitlines()

    hand0_, hand1_ = parse_input(data_)

    if sys.argv[2] == '1':
        out_ = score(combat(hand0_, hand1_))
    elif sys.argv[2] == '2':
        out_ = score(combat_evolved(hand0_, hand1_)[0])

    print(out_)
    