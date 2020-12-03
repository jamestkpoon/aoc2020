import sys

def separate_string(s):
    first_hyphen_idx_ = s.find('-')
    first_space_idx_ = s.find(' ')
    first_colon_idx_ = s.find(':')
    last_space_idx_ = s.rfind(' ')
    
    a_ = int(s[:first_hyphen_idx_])
    b_ = int(s[first_hyphen_idx_+1:first_space_idx_])
    c_ = s[first_space_idx_+1:first_colon_idx_]
    d_ = s[last_space_idx_+1:]
    if d_[-1] == '\n': d_ = d_[:-1]
    
    return [ a_, b_, c_, d_ ]

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        data_ = f.readlines()
        
    total_valid_ = 0
    if sys.argv[2] == '1':
        for d in data_:
            [ min_, max_, target_, seq_ ] = separate_string(d)
            count_ = seq_.count(target_)
            if count_ >= min_ and count_ <= max_: total_valid_ += 1
    elif sys.argv[2] == '2':
        for d in data_:
            [ pos1_, pos2_, target_, seq_ ] = separate_string(d)
            sseq_ = [ seq_[pos1_-1], seq_[pos2_-1] ]
            if sseq_.count(target_) == 1: total_valid_ += 1                
            
    print(total_valid_)
