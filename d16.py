import sys

def parse(strs):
    rules_ = {}
    
    line_idx_ = 0
    while(len(strs[line_idx_]) != 0):
        line_ = strs[line_idx_]
        line_idx_ += 1
        
        key_ = line_[:line_.find(':')]
        lb1_ = int(line_[line_.find(': ')+2:line_.find('-')])
        ub1_ = int(line_[line_.find('-')+1:line_.find(' or')])
        lb2_ = int(line_[line_.rfind(' ')+1:line_.rfind('-')])
        ub2_ = int(line_[line_.rfind('-')+1:])
        
        rules_[key_] = [ lb1_, ub1_, lb2_, ub2_ ]
        
    line_idx_ += 2
    own_ticket_ = list(map(int, strs[line_idx_].split(',')))
    
    line_idx_ += 3
    other_tickets_ = []    
    for line in strs[line_idx_:]:
        other_tickets_.append(list(map(int, line.split(','))))
    
    return rules_, own_ticket_, other_tickets_
    
def rule_check(v, rule):
    if v >= rule[0] and v <= rule[1]: return True
    elif v >= rule[2] and v <= rule[3]: return True
    else: return False
    
def ticket_check(ticket, rules):
    out_ = None
    for v in ticket:
        valid_ = False
        for rule in rules_.values():
            rule_valid_ = rule_check(v, rule)
            if rule_valid_:
                valid_ = True
                break
        if not valid_:
            out_ = out_ + v if out_ is not None else v
        
    return out_

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        data_ = f.read().splitlines()
        
    rules_, own_ticket_, other_tickets_ = parse(data_)

    if sys.argv[2] == '1':
        out_ = 0
        for other_ticket in other_tickets_:
            res_ = ticket_check(other_ticket, rules_)
            if res_ is not None: out_ += res_
    elif sys.argv[2] == '2':
        other_tickets_ = list(filter(lambda t: ticket_check(t, rules_) is None, other_tickets_))
        valid_keys_dict_ = {}
        for c in range(len(own_ticket_)):
            valid_keys_ = []
            for key, rule in rules_.items():
                valid_ = True
                for other_ticket in other_tickets_:
                    if not rule_check(other_ticket[c], rule):
                        valid_ = False
                        break
                if valid_: valid_keys_.append(key)
                
            valid_keys_dict_[c] = valid_keys_
            
        ordered_keys_ = [ '' ] * len(own_ticket_)
        unidentified_columns_ = list(range(len(own_ticket_)))
        while len(unidentified_columns_) > 0:
            for c in unidentified_columns_:
                if len(valid_keys_dict_[c]) == 1:
                    key_ =  valid_keys_dict_[c][0]
                    ordered_keys_[c] = key_                    
                    unidentified_columns_.remove(c)
                    for v in valid_keys_dict_.values():
                        if key_ in v: v.remove(key_)                    
                    break
                    
        out_ = 1
        for i in range(len(ordered_keys_)):
            if 'departure' in ordered_keys_[i]:
                out_ *= own_ticket_[i]

    print(out_)
    
