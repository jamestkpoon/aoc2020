import sys
from collections import Counter

def parse_list_to_dict_based_on_leap(sorted_list, max_leap=3):
    out_ = {}
    for i in range(len(sorted_list)):
        out_[sorted_list[i]] = {}
        for j in range(i+1, len(sorted_list)):
            if sorted_list[j] - sorted_list[i] <= max_leap:
                out_[sorted_list[i]][sorted_list[j]] = 1

    return out_

def cumulative_sum_down_tree_with_numerical_keys(dicto):
    out_ = {}
    desc_keys_ = sorted(dicto.keys())[::-1]
    out_[desc_keys_[0]] = 1
    for desc_key in desc_keys_[1:]:
        out_[desc_key] = 0
        for k in dicto[desc_key].keys():
            out_[desc_key] += out_[k]

    return out_

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        data_ = f.read().splitlines()

    ints_ = list(map(int, data_))

    if sys.argv[2] == '1':
        ints_.append(0)
        sorted_ = sorted(ints_)
        diffs_ = [ sorted_[i] - sorted_[i-1] for i in range(1,len(sorted_)) ]
        counter_ = Counter(diffs_)
        out_ = counter_[1] * (counter_[3] + 1)
    elif sys.argv[2] == '2':
        max_leap_ = int(sys.argv[3])
        ints_sorted_ = sorted(ints_)
        dict_ = parse_list_to_dict_based_on_leap(ints_sorted_, max_leap_)
        cumsum_dict_ = cumulative_sum_down_tree_with_numerical_keys(dict_)

        out_ = 0
        for i in ints_sorted_:
            if i <= max_leap_: out_ += cumsum_dict_[i]
            else: break

    print(out_)
    