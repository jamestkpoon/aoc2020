import sys
import numpy as np
from copy import deepcopy

def parse_input(strs):
    idx_ = 0
    
    rules_ = {}
    while len(strs[idx_]) != 0:
        split_ = strs[idx_].split(' ')
        if split_[1] == '"a"': rule_ = [ 'a' ]
        elif split_[1] == '"b"': rule_ = [ 'b' ]
        elif '|' not in split_: rule_ = list(map(int, split_[1:]))
        else:
            pipe_index_ = split_.index('|')
            ruleA_ = list(map(int, split_[1:pipe_index_]))
            ruleB_ = list(map(int, split_[pipe_index_+1:]))
            rule_ = [ ruleA_ , ruleB_ ]
            
        rules_[int(split_[0][:-1])] = rule_
        idx_ += 1
    
    return rules_, strs[idx_+1:]

def accumulate_possible_messages(rules, rep_limit=1):
    covered_rules_ = {}
    for k,v in rules.items():
        covered_rules_[k] = {}
        if type(v[0]) is int:
            covered_rules_[k][hash(str(v))] = False if k not in v else 0
        elif type(v[0]) is list:
            for vv in v:
                covered_rules_[k][hash(str(vv))] = False if k not in vv else 0
                
    def all_rules_covered():
        for v in covered_rules_.values():
            for vv in v.values():
                if type(vv) is bool:
                    if vv is False: return False
                elif type(vv) is int: return False
                
        return True
            
    a_rule_, b_rule_ = None, None
    for k,v in rules.items():
        if v == [ 'a' ]:
            a_rule_ = k
            covered_rules_[k][hash(str([ 'a' ]))] = True
        elif v == [ 'b' ]:
            b_rule = k
            covered_rules_[k][hash(str([ 'b' ]))] = True
            
    out_ = { a_rule_: [ 'a' ], b_rule: [ 'b' ] }
 
    def try_accumulate(k, v):
        v_hash_ = hash(str(v))
        crv_type_ = type(covered_rules_[k][v_hash_])
        if crv_type_ is bool and covered_rules_[k][v_hash_] == True: return None
        
        if np.any([ vv not in out_.keys() for vv in v ]): return None
        else:
            for vv in v:
                for vvv in covered_rules_[vv].values():
                    if type(vvv) is bool and vvv == False: return None
        
        if crv_type_ is bool: covered_rules_[k][v   _hash_] = True
        elif crv_type_ is int:
            covered_rules_[k][v_hash_] += 1
            if covered_rules_[k][v_hash_] >= rep_limit: covered_rules_[k][v_hash_] = True
        
        combos_ = []
        for c in np.ndindex(*[ len(out_[vv]) for vv in v ]):
            combos_.append(''.join([ out_[v[i]][c[i]] for i in range(len(c)) ]))
                
        return combos_
    
    while not all_rules_covered():
        for k,v in rules.items():
            if type(v[0]) is int:
                strs_ = try_accumulate(k, v)
                if strs_ is not None: out_[k] = strs_
            elif type(v[0]) is list:
                for vv in v:
                    strs_ = try_accumulate(k, vv)
                    if strs_ is not None:
                        if k not in out_.keys(): out_[k] = strs_
                        else: out_[k] += strs_
            
    return out_
        
if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        data_ = f.read().splitlines()
        
    rules_, received_messages_ = parse_input(data_)
    possible_messages_ = accumulate_possible_messages(rules_)

    out_ = 0
    for m in received_messages_:
        if m in possible_messages_[0]: out_ += 1

    print(out_)
    