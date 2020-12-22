import sys
import numpy as np

class Food:
    def __init__(self, string):
        self._ingredients = []
        self._allergens = []
        
        split_ = string.split(' ')
        idx_ = 0
        while idx_ < len(split_) and split_[idx_] != '(contains':
            self._ingredients.append(split_[idx_])
            idx_ += 1
            
        idx_ += 1
        while idx_ < len(split_):
            self._allergens.append(split_[idx_][:-1])
            idx_ += 1
            
def list_all_ingredients_and_allergens(foods):
    ingredients_set_, allergens_set_ = set(), set()    
    for food in foods:
        for ingredient in food._ingredients: ingredients_set_.add(ingredient)
        for allergen in food._allergens: allergens_set_.add(allergen)
        
    return list(ingredients_set_), list(allergens_set_)
    
def find_safe_ingredients(ingredients, allergens, foods):
    safe_ingredients_ = []
    for ingredient in ingredients:
        foods_without_ = filter(lambda f: ingredient not in f._ingredients, foods)
        allergens_in_foods_without_ = list_all_ingredients_and_allergens(foods_without_)[1]
        if len(allergens_in_foods_without_) == len(allergens): safe_ingredients_.append(ingredient)
            
    return safe_ingredients_

def match_allergens_to_ingredients(ingredients, allergens, foods):
    foods_without_ingredient_ = [ [ ingredient not in f._ingredients for f in foods ] for ingredient in ingredients ]
    foods_with_allergen_ = [ [ allergen in f._allergens for f in foods ] for allergen in allergens ]
    m_ = np.empty([ len(ingredients), len(allergens) ], dtype=np.bool)
    for r in range(m_.shape[0]):
        for c in range(m_.shape[1]):
            m_[r,c] = not np.any(np.logical_and(foods_without_ingredient_[r], foods_with_allergen_[c]))
    
    dict_ = {}
    while len(dict_) < len(allergens):
        for r in range(m_.shape[0]):
            hits_ = np.where(m_[r,:])[0]
            if len(hits_) == 1:
                dict_[allergens[hits_[0]]] = ingredients[r]
                m_[r,:] = False
                m_[:,hits_[0]] = False
            
    return dict_

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        data_ = f.read().splitlines()
        
    foods_ = [ Food(d) for d in data_ ]
    ingredients_, allergens_ = list_all_ingredients_and_allergens(foods_)
    safe_ingredients_ = find_safe_ingredients(ingredients_, allergens_, foods_)

    if sys.argv[2] == '1':
        out_ = 0
        for food in foods_:
            for ingredient in safe_ingredients_:
                if ingredient in food._ingredients: out_ += 1
    elif sys.argv[2] == '2':
        dangerous_ingredients_ = list(filter(lambda i: i not in safe_ingredients_, ingredients_))
        allergens_dict_ = match_allergens_to_ingredients(dangerous_ingredients_, allergens_, foods_)
        out_ = ','.join([ allergens_dict_[allergen] for allergen in sorted(allergens_) ])

    print(out_)
    