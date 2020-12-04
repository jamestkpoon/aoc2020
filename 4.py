import sys

def separate_passports(lines):
    passports_ = []
    
    passport_ = {}
    for l in lines:
        if len(l) == 0 and len(passport_.keys()) != 0:
            passports_.append(passport_)
            passport_ = {}
        else:
            while len(l) != 0:
                last_space_idx_ = l.rfind(' ')
                chunk_ = l[last_space_idx_+1:] if last_space_idx_ != -1 else l
                colon_pos_ = chunk_.find(':')
                passport_[chunk_[:colon_pos_]] = chunk_[colon_pos_+1:]
                l = l[:last_space_idx_] if last_space_idx_ != -1 else ""
    
    if len(passport_.keys()) != 0:
        passports_.append(passport_)
    
    return passports_
    
def passport_has_all_keys(passport, keys):
    for key in keys:
        if key not in passport.keys():
            return False
            
    return True
    
def cast_year_and_check_inclusive_range(s, l,u):
    if len(s) != 4: return False
    
    try: 
        s_ = int(s)
        return s_ >= l and s_ <= u
    except: return False
    
def is_valid_passport_id(s, length=9):
    if len(s) != length: return False
    
    try:
        int(s)
        return True
    except: return False
    
def is_valid_hair_color(s, length=7, header='#'):
    if len(s) != length: return False
    if s[:len(header)] != header: return False
    
    for c in map(ord, s[1:]):
        if not ((c >= ord('0') and c <= ord('9')) or (c >= ord('a') and c <= ord('f'))):
            return False
        
    return True

def is_valid_height(s, range_dict):
    for k,v in range_dict.items():
        neg_key_length_ = -len(k)
        if s[neg_key_length_:] == k:
            try:
                h_ = int(s[:neg_key_length_])
                return h_ >= v[0] and h_ <= v[1]
            except: return False
            
    return False

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        data_ = f.read().splitlines()
        
    passports_ = separate_passports(data_)
    keys_ = [ 'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid' ]
    valid_ = 0
    
    if sys.argv[2] == '1':
        for passport in passports_:
            if passport_has_all_keys(passport, keys_): valid_ += 1
    elif sys.argv[2] == '2':
        for passport in passports_:
            if not passport_has_all_keys(passport, keys_): continue
            
            if not cast_year_and_check_inclusive_range(passport['byr'], 1920,2002): continue
            if not cast_year_and_check_inclusive_range(passport['iyr'], 2010,2020): continue
            if not cast_year_and_check_inclusive_range(passport['eyr'], 2020,2030): continue
            if passport['ecl'] not in [ 'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth' ]: continue
            if not is_valid_passport_id(passport['pid']): continue
            if not is_valid_hair_color(passport['hcl']): continue
            if not is_valid_height(passport['hgt'], { 'cm': [150,193], 'in': [59,76] }): continue
            
            valid_ += 1
    
    print(valid_)
    
