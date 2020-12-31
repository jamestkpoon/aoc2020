import sys
from functools import reduce

def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod
 
def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        data_ = f.read().splitlines()

    if sys.argv[2] == '1':
        t0_ = int(data_[0])
        intervals_ = sorted([ int(x) for x in data_[1].split(',') if x != 'x' ])
        t_ = t0_
        out_ = None
        while out_ == None:
            for i in intervals_:
                if t_ % i == 0:
                    out_ = i * (t_ - t0_)
                    break
            t_ += 1
    elif sys.argv[2] == '2':
        offsets_, values_ = [], []
        split_ = data_[1].split(',')
        for i in range(len(split_)):
            if split_[i] != 'x':
                offsets_.append(-i)
                values_.append(int(split_[i]))
                
        out_ = chinese_remainder(values_, offsets_)
        
    print(out_)
    