import sys
import numpy as np
from d3 import to_binary_map

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
SIDES = [ UP, DOWN, LEFT, RIGHT ]

def get_opposite_direction(side):
    return (side + 2) % 4

class Tile:
    def __init__(self, data):
        self._data = data
            
    def flipud(self):
        self._data = np.flipud(self._data)
        
    def fliplr(self):
        self._data = np.fliplr(self._data)
        
    def rot90(self):
        self._data = np.rot90(self._data)
            
    def get_edge(self, side):
        if side is UP: return self._data[0,:]
        elif side is DOWN: return self._data[-1,:]
        elif side is LEFT: return self._data[:,0]
        elif side is RIGHT: return self._data[:,-1]
        
    def get_symmetrical_edge_hash(self, side):
        side_ = self.get_edge(side)
        hash_fwd_ = hash(str(side_))
        hash_rev_ = hash(str(side_[::-1]))
        
        return hash(str(sorted([ hash_fwd_, hash_rev_ ])))
        
    def get_transformations(self):
        for i in range(4):
            yield self._data
            self.fliplr()
            yield self._data
            self.flipud()
            yield self._data
            self.fliplr()
            yield self._data
                
            self.rot90()
        
    def try_transform_to_match(self, side, edge_to_match):
        for m in self.get_transformations():
            if np.array_equal(self.get_edge(side), edge_to_match):
                return True
                
        return False
        
def parse_input(strs):
    out_ = {}
    line_index_ = 0
    while line_index_ < len(strs):
        key_ = int(strs[line_index_][5:-1])
        line_index_ += 1
        
        sI_ = line_index_
        while line_index_ < len(strs) and len(strs[line_index_]) > 0:
            line_index_ += 1
            
        out_[key_] = Tile(to_binary_map(strs[sI_:line_index_]))
        line_index_ += 1
        
    return out_
    
def count_edge_instances(tiles):
    out_ = {}
    for tile in tiles.values():
        for side in SIDES:
            hash_ = tile.get_symmetrical_edge_hash(side)
            if hash_ not in out_.keys(): out_[hash_] = 1
            else: out_[hash_] += 1
    
    return out_
    
def typify_tiles(tiles, edge_instance_counts):
    corner_tile_keys_ = []
    edge_tile_keys_ = []
    interior_tile_keys_ = []
    for tile_id,tile in tiles.items():
        num_unique_sides_ = sum([ edge_instance_counts[tile.get_symmetrical_edge_hash(side)] == 1 for side in SIDES ])
        if num_unique_sides_ == 0: interior_tile_keys_.append(tile_id)
        elif num_unique_sides_ == 1: edge_tile_keys_.append(tile_id)
        else: corner_tile_keys_.append(tile_id)
        
    return interior_tile_keys_, edge_tile_keys_, corner_tile_keys_
    
def grow(tiles, start_idx, direction, candidates):
    out_ = [ start_idx ]
    opposite_direction_ = get_opposite_direction(direction)
    
    while len(candidates) > 0:
        matched_ = False
        for tile_id in candidates:
            edge_to_match_ = tiles_[out_[-1]].get_edge(opposite_direction_)
            if tiles[tile_id].try_transform_to_match(direction, edge_to_match_):
                out_.append(tile_id)
                candidates.remove(tile_id)
                matched_ = True
                break
        if not matched_: break
            
    return out_
    
if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        data_ = f.read().splitlines()
        
    tiles_ = parse_input(data_)
    edge_instance_counts_ = count_edge_instances(tiles_)
    interior_tile_keys_, edge_tile_keys_, corner_tile_keys_ = typify_tiles(tiles_, edge_instance_counts_)

    if sys.argv[2] == '1':
        out_ = 1
        for n in corner_tile_keys_: out_ *= n
    elif sys.argv[2] == '2':
        tl_id_ = corner_tile_keys_.pop()
        if edge_instance_counts_[tiles_[tl_id_].get_symmetrical_edge_hash(UP)] > 1: tiles_[tl_id_].flipud()
        if edge_instance_counts_[tiles_[tl_id_].get_symmetrical_edge_hash(LEFT)] > 1: tiles_[tl_id_].fliplr()
        
        tile_idx_map_size_ = int(np.sqrt(len(tiles_)))
        tile_idx_map_ = np.empty([ tile_idx_map_size_, tile_idx_map_size_ ], dtype=np.int)
        tile_idx_map_[:-1,0] = grow(tiles_, tl_id_, UP, edge_tile_keys_)
        for r in range(1, tile_idx_map_size_- 1):
            tile_idx_map_[r,:-1] = grow(tiles_, tile_idx_map_[r,0], LEFT, interior_tile_keys_)
            tile_idx_map_[r,-1] = grow(tiles_, tile_idx_map_[r,-2], LEFT, edge_tile_keys_)[1]
        for c in range(1, tile_idx_map_size_ - 1):
            tile_idx_map_[0,c]  = grow(tiles_, tile_idx_map_[1,c], DOWN, edge_tile_keys_)[1]
            tile_idx_map_[-1,c] = grow(tiles_, tile_idx_map_[-2,c], UP , edge_tile_keys_)[1]
        tile_idx_map_[0, -1] = grow(tiles_, tile_idx_map_[0 ,-2], LEFT, corner_tile_keys_)[1]
        tile_idx_map_[-1, 0] = grow(tiles_, tile_idx_map_[-2, 0], UP,   corner_tile_keys_)[1]
        tile_idx_map_[-1,-1] = grow(tiles_, tile_idx_map_[-2,-1], UP,   corner_tile_keys_)[1]
        
        borderless_tile_shape_ = np.asarray(tiles_[tl_id_]._data.shape) - 2
        img_shape_ = tile_idx_map_size_ * borderless_tile_shape_
        img_ = np.empty(tuple(img_shape_), dtype=np.bool)
        for c in range(tile_idx_map_size_):
            c_sI_ = c * borderless_tile_shape_[0]
            c_eI_ = c_sI_ + borderless_tile_shape_[0]
            for r in range(tile_idx_map_size_):
                r_sI_ = r * borderless_tile_shape_[1]
                r_eI_ = r_sI_ + borderless_tile_shape_[1]
                img_[c_sI_:c_eI_,r_sI_:r_eI_] = tiles_[tile_idx_map_[c,r]]._data[1:-1,1:-1]
                
        with open(sys.argv[3], 'r') as f:
            target_pattern_ = to_binary_map(f.read().splitlines())
            target_trues_ = np.where(target_pattern_.ravel())[0]
            
        out_ = None
        for img in Tile(img_).get_transformations():
            num_patterns_found_ = 0
            for c in range(img.shape[0] - target_pattern_.shape[0]):
                for r in range(img.shape[1] - target_pattern_.shape[1]):
                    roi_ravel_ = img[c:c+target_pattern_.shape[0], r:r+target_pattern_.shape[1]].ravel()
                    if np.all([ roi_ravel_[i] for i in target_trues_ ]): num_patterns_found_ += 1
        
            if num_patterns_found_ != 0:
                out_ = np.sum(img_) - (num_patterns_found_ * np.sum(target_pattern_))
                break
    
    print(out_)
    