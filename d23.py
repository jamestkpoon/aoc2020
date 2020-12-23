import sys

class LinkedListItem:
    def __init__(self, data):
        self._data = data
        self._prev = None
        self._next = None
        
    def get_data(self):
        return self._data
        
    def set_prev(self, x):
        self._prev = x
    
    def set_next(self, x):
        self._next = x
        
    def get_prev(self):
        return self._prev
        
    def get_next(self):
        return self._next

class CircularLinkedListOfInts:
    def __init__(self, ints):
        self._items = [ LinkedListItem(i) for i in range(max(ints) + 1) ]
        
        for i in range(len(ints) - 1):
            self._items[ints[i]].set_next(self._items[ints[i+1]])
        for i in range(1, len(ints)):
            self._items[ints[i]].set_prev(self._items[ints[i-1]])
         
        self._items[ints[0]].set_prev(self._items[ints[-1]])
        self._items[ints[-1]].set_next(self._items[ints[0]])
            
    def shift_chunk(self, chunk_start, chunk_size, new_previous_idx):
        new_previous_ = self._items[new_previous_idx]
        new_previous_next_old_ = new_previous_.get_next()
    
        chunk_end_ = chunk_start
        for i in range(1, chunk_size): chunk_end_ = chunk_end_.get_next()
        
        chunk_start.get_prev().set_next(chunk_end_.get_next())
        chunk_end_.get_next().set_prev(chunk_start.get_prev())
  
        chunk_start.set_prev(new_previous_)
        new_previous_.set_next(chunk_start)
        
        chunk_end_.set_next(new_previous_next_old_)
        new_previous_next_old_.set_prev(chunk_end_)
            
    def __getitem__(self, i):
        return self._items[i]
            
def play(ints, num_turns, chunk_size):
    ll_ = CircularLinkedListOfInts(ints)
    active_item_ = ll_[ints[0]]
    min_, max_ = min(ints), max(ints)    
    next_values_ = [ 0 ] * chunk_size
    
    for turn_count in range(num_turns):
        target_ = active_item_.get_data() - 1
        item_ = active_item_        
        for i in range(chunk_size):
            item_ = item_.get_next()
            next_values_[i] = item_.get_data()
            
        while target_ in next_values_: target_ -= 1
        if target_ < min_:
            target_ = max_
            while target_ in next_values_: target_ -= 1
            
        ll_.shift_chunk(active_item_.get_next(), chunk_size, target_)
        active_item_ = active_item_.get_next()
        
    return ll_
        
def gather_data_after(ll, start, n):
    out_ = []
    item_ = ll[start].get_next()
    for i in range(n):
        out_.append(item_.get_data())
        item_ = item_.get_next()
        
    return out_

if __name__ == '__main__':
    input_ = list(map(int, list(sys.argv[1])))
    
    if sys.argv[2] == '1':
        ints_after_1_ = gather_data_after(play(input_, 100, 3), 1, len(input_) - 1)
        out_ = ''.join(map(str, ints_after_1_))
    elif sys.argv[2] == '2':
        input_ += list(range(len(input_) + 1, 1000001))
        ints_after_1_ = gather_data_after(play(input_, 10000000, 3), 1, 2)
        out_ = ints_after_1_[0] * ints_after_1_[1]

    print(out_)
    