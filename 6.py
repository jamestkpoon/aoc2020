import sys

def split_input_into_groups(s):
    chunks_ = []
    chunk_ = []
    
    for l in s:
        if len(l) != 0: chunk_.append(l)
        elif len(chunk_) != 0:
            chunks_.append(chunk_)
            chunk_ = []
            
    if len(chunk_) != 0: chunks_.append(chunk_)
    
    return chunks_
    
def find_common_answers(answers_group):
    common_answers_ = []
    for answer in answers_group:
        for c in answer:
            if c not in common_answers_:
                common_answers_.append(c)
                
    return common_answers_    

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        data_ = f.read().splitlines()
    
    answers_groups_ = split_input_into_groups(data_)
    out_ = 0
    
    if sys.argv[2] == '1':
        for answers_group in answers_groups_:
            out_ += len(find_common_answers(answers_group))
            
    if sys.argv[2] == '2':
        for answers_group in answers_groups_:
            common_answers_ = find_common_answers(answers_group)
            for c in common_answers_:
                common_ = True
                for answer in answers_group:
                    if c not in answer:
                        common_ = False
                        break
                if common_: out_ += 1
        
    print(out_)