import sys
import numpy as np
from copy import deepcopy

def generate_pows(length=36):
    out_ = []
    for i in range(length):
        out_.append(int(2**i))
    
    return out_[::-1]
    
def register_to_decimal(register, pows):
    out_ = 0
    for i in range(len(register)):
        if register[i]: out_ += pows[i]
    
    return out_
    
def decimal_to_register(decimal, pows):
    out_ = [ False ] * len(pows)
    n_ = decimal
    
    for i in range(len(pows)):
        if n_ >= pows[i]:
            out_[i] = True
            n_ -= pows[i]
            
    return out_
    
def apply_mask_1(register, mask):
    out_ = []
    for i in range(len(register)):
        if mask[i] == '1': out_.append(True)
        elif mask[i] == '0': out_.append(False)
        else: out_.append(register[i])
        
    return out_
    
def apply_mask_2(register, mask):
    out_raw_ = []
    x_indices_ = []
    for i in range(len(register)):
        if mask[i] == '1': out_raw_.append(True)
        elif mask[i] == '0': out_raw_.append(register[i])
        else:
            out_raw_.append('X')
            x_indices_.append(i)
            
    outs_ = []
    for n in np.ndindex(*([ 2 ] * len(x_indices_))):
        out_ = deepcopy(out_raw_)
        for i in range(len(x_indices_)):
            out_[x_indices_[i]] = True if n[i] == 1 else False
        outs_.append(out_)
        
    return outs_    

class Program:
    def __init__(self, strs):
        self._pows = generate_pows()
    
        self._cmds = []
        cmd_ = {}
        for s in strs:
            if s[:7] == 'mask = ':
                if cmd_ != {}:
                    self._cmds.append(cmd_)
                    cmd_ = {}
                cmd_['mask'] = s[7:]
                cmd_['operations'] = []
            else:
                address_ = int(s[s.find('[')+1:s.find(']')])
                value_ = int(s[s.rfind(' ')+1:])
                cmd_['operations'].append([ address_, value_ ])
                
        if cmd_ != {}: self._cmds.append(cmd_)
        
    def run_1(self):
        memory_ = {}
        for c in self._cmds:
            for op in c['operations']:
                value_register_ = decimal_to_register(op[1], self._pows)
                memory_[op[0]] = register_to_decimal(apply_mask_1(value_register_, c['mask']), self._pows)
                
        return sum(memory_.values())
        
    def run_2(self):
        memory_ = {}
        for c in self._cmds:
            for op in c['operations']:
                address_registers_ = apply_mask_2(decimal_to_register(op[0], self._pows), c['mask'])
                for address_register in address_registers_:
                    memory_[register_to_decimal(address_register, self._pows)] = op[1]
        
        return sum(memory_.values())

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        data_ = f.read().splitlines()
        
    program_ = Program(data_)

    if sys.argv[2] == '1':
        out_ = program_.run_1()
    elif sys.argv[2] == '2':
        out_ = program_.run_2()

    print(out_)
    
