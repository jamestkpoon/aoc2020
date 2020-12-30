import sys
from collections import Counter

def parse_input(strs):
    idx_ = 0
    
    rules_ = {}
    while len(strs[idx_]) != 0:
        split_ = strs[idx_].split(' ')
        if split_[1] == '"a"': rule_ = 'a'
        elif split_[1] == '"b"': rule_ = 'b'
        elif '|' not in split_: rule_ = [ list(map(int, split_[1:])) ]
        else:
            pipe_index_ = split_.index('|')
            ruleA_ = list(map(int, split_[1:pipe_index_]))
            ruleB_ = list(map(int, split_[pipe_index_+1:]))
            rule_ = [ ruleA_ , ruleB_ ]
            
        rules_[int(split_[0][:-1])] = rule_
        idx_ += 1
    
    return rules_, strs[idx_+1:]
    
def find_terminal_keys(rules):
    t_, nt_ = [], []
    for k,v in rules.items():
        if type(v) is str: t_.append(k)
        else: nt_.append(k)
        
    return t_, nt_
    
def cyk(input_string, rules, terminal_keys, non_terminal_keys, target_check_fn):
    if input_string in [ rules[k] for k in terminal_keys ]: return True

    input_string_length_ = len(input_string)
    keys_and_strides_ = [ None ] * input_string_length_    
    for i in range(input_string_length_):
        for k in terminal_keys:
            if rules[k][0] == input_string[i]:
                keys_and_strides_[i] = [ [ k, 1 ] ]
                break
                
    def get_rule_stride(c, rule):
        c_ = c
        for rule_key in rule:
            ok_ = False
            if c_ >= input_string_length_: return None
            for key, stride in keys_and_strides_[c_]:
                if key == rule_key:
                    ok_ = True
                    c_ += stride
                    break
            if not ok_: return None
            
        return c_ - c

    while True:
        new_accumulations_ = False        
        for c in range(input_string_length_):
            for k in non_terminal_keys:
                if k in [ key_and_stride[0] for key_and_stride in keys_and_strides_[c] ]: continue                
                for rule in rules[k]:
                    stride_ = get_rule_stride(c, rule)
                    if stride_ is not None:
                        keys_and_strides_[c].append([ k, stride_ ])
                        new_accumulations_ = True
                        break        
        if target_check_fn(keys_and_strides_): return True
        elif not new_accumulations_: return False
        
if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        data_ = f.read().splitlines()
        
    rules_, received_messages_ = parse_input(data_)
    terminal_keys_, non_terminal_keys_ = find_terminal_keys(rules_)
    
    if sys.argv[2] == '1':
        def target_check_fn(keys_and_strides):
            for key, stride in keys_and_strides[0]:
                if key == 0 and stride == len(keys_and_strides): return True
            return False
    elif sys.argv[2] == '2':
        def target_check_fn(keys_and_strides):
            c_, keys_str_ = 0, ''
            while c_ < len(keys_and_strides):
                hit_ = False
                for key, stride in keys_and_strides[c_]:
                    if key == 42 or key == 31:
                        c_ += stride
                        keys_str_ += chr(key)
                        hit_ = True
                        break
                if not hit_: return False
            counter_ = Counter(keys_str_)
            return c_ == len(keys_and_strides) and counter_[chr(42)] > counter_[chr(31)] and keys_str_.find(chr(31)) > keys_str_.rfind(chr(42))
    
    print(sum([ cyk(m, rules_, terminal_keys_, non_terminal_keys_, target_check_fn) for m in received_messages_ ]))