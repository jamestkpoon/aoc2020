import sys

def parse_bag_dict(lines):
    out_ = {}
    for line in lines:
        key_ = line[:line.find(' bags')]
        children_ = {}

        if 'no other' not in line:
            for content in line[line.find('contain ')+8:].split(', '):
                first_space_idx_ = content.find(' ')
                last_space_idx_ = content.rfind(' ')
                quantity_ = int(content[:first_space_idx_])
                color_ = content[first_space_idx_+1:last_space_idx_]
                children_[color_] = quantity_

        out_[key_] = children_

    return out_

def check_if_key_leads_down_to(dict, start_key, desired_key):
    frontier_keys_ = dict[start_key].keys()
    if desired_key in frontier_keys_: return True

    while len(frontier_keys_) != 0:
        frontier_keys_new_ = set()
        for frontier_key in frontier_keys_:
            child_keys_ = dict[frontier_key].keys()
            if desired_key in child_keys_: return True
            frontier_keys_new_ = frontier_keys_new_.union(child_keys_)
        frontier_keys_ = frontier_keys_new_

    return False

def count_child_values(dicto, start_key, multiplier=1):
    out_ = multiplier * sum([ v for v in dicto[start_key].values() ])
    for k,v in dicto[start_key].items():
        out_ += count_child_values(dicto, k, v*multiplier)

    return out_

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        data_ = f.read().splitlines()

    bag_dict_ = parse_bag_dict(data_)

    if sys.argv[2] == '1':
        out_ = 0
        for key in bag_dict_.keys():
            if key == sys.argv[3]: continue
            if check_if_key_leads_down_to(bag_dict_, key, sys.argv[3]): out_ += 1
    elif sys.argv[2] == '2':
        out_ = count_child_values(bag_dict_, sys.argv[3])

    print(out_)