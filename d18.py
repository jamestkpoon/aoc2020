import sys

def split_and_strip_sep(s, sep=' '):
    s_ = list(s)
    while sep in s_: s_.remove(sep)
    
    return s_
    
def calc_1(l):
    out_ = int(l[0])
    idx_ = 1
    while idx_ < len(l):
        next_int_ = int(l[idx_+1])
        if l[idx_] == '+': out_ += next_int_
        elif l[idx_] == '*': out_ *= next_int_
        else: print("  Got unrecognized operator symbol " + l[idx_])
            
        idx_ += 2
    
    return out_
    
def calc_2(l):
    while '+' in l:
        idx_ = l.index('+')
        l = l[:idx_-1] + [ str(int(l[idx_-1]) + int(l[idx_+1])) ] + l[idx_+2:]
        
    out_ = 1
    for i in l[::2]: out_ *= int(i)
        
    return out_
    
def parse(l, calc):
    while '(' in l:
        open_brace_idx_ = len(l) - 1 - l[::-1].index('(')
        close_brace_idx_ = open_brace_idx_ + 1
        while l[close_brace_idx_] != ')': close_brace_idx_ += 1
        ans_ = calc(l[open_brace_idx_+1:close_brace_idx_])
        l = l[:open_brace_idx_] + [ str(ans_) ] + l[close_brace_idx_+1:]
    
    return calc(l)

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        data_ = f.read().splitlines()
        
    split_lines_ = [ split_and_strip_sep(d) for d in data_ ]
    
    if sys.argv[2] == '1': calc_fn_ = calc_1
    elif sys.argv[2] == '2': calc_fn_ = calc_2
    
    out_ = 0
    for sl in split_lines_:
        out_ += parse(sl, calc_fn_)

    print(out_)
    