import sys

def egcd(a, b):
	if a == 0:
		return (b, 0, 1)
	else:
		gcd, x, y = egcd(b % a, a)
		return (gcd, y - (b//a) * x, x)


def find_offset_lcm(a, b):
    b_offset_from_a_ = b[0] - a[0]
    gcd_ = np.gcd(a[1], b[1])
    
    

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        data_ = f.read().splitlines()

    if sys.argv[2] == '1':
        t0_ = int(data_[0])
        intervals_ = sorted([ int(x) for x in data_[1].split(',') if x != 'x' ])
        t_ = t0_
        while out_ == None:
            for i in intervals_:
                if t_ % i == 0:
                    out_ = i * (t_ - t0_)
                    break
            t_ += 1
    elif sys.argv[2] == '2':
        offsets_and_values_ = []
        split_ = data_[1].split(',')
        for i in range(len(split_)):
            if split_[i] != 'x':
                offsets_and_values_.append([ i, int(split_[i]) ])

        print(egcd(5, 13))
                
        #largest_value_idx_ = 0
        #for i in range(len(offsets_and_values_)):
        #    if offsets_and_values_[i][1] > offsets_and_values_[largest_value_idx_][1]:
        #        largest_value_idx_ = i
        #largest_offset_and_value_ = offsets_and_values_.pop(largest_value_idx_)
        
        #out_ = 100000000000000
        #while out_ % largest_offset_and_value_[1] != 0: out_ += 1
        #out_ -= largest_offset_and_value_[0]
        
        #order_ = np.argsort([ ov[1] for ov in offsets_and_values_ ])[::-1]
        
        #while True:
        #    ok_ = True
        #    for o in order_:
        #        if (out_ + offsets_and_values_[o][0]) % offsets_and_values_[o][1] != 0:
        #            ok_ = False
        #            break
        #    if ok_: break
        #    out_ += largest_offset_and_value_[1]            
        
    print(out_)
    