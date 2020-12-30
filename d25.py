import sys

def get_loop_size(target, subject_number=7, mod=20201227):
    v_, num_loops_ = 1, 0
    while v_ != target:
        v_ = (v_ * subject_number) % mod
        num_loops_ += 1
        
    return num_loops_
    
def transform(subject_number, num_loops, mod=20201227):
    out_ = 1
    for loop_count in range(num_loops):
       out_ = (out_ * subject_number) % mod

    return out_

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        data_ = f.read().splitlines()
        
    public_keys_ = list(map(int, data_))
    secret_loop_sizes_ = list(map(get_loop_size, public_keys_))
    
    if sys.argv[2] == '1':
        out_ = transform(public_keys_[0], secret_loop_sizes_[1])        
    #elif sys.argv[2] == '2':
        

    print(out_)
    