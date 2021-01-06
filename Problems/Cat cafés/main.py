cat_cafe_dict = dict()
while True:
    cat_cafe = input()
    if cat_cafe == 'MEOW':
        break
    cat_cafe_split = cat_cafe.split()
    cat_cafe_dict[cat_cafe_split[0]] = int(cat_cafe_split[1])

max_key = max(cat_cafe_dict, key=cat_cafe_dict.get)
print(max_key)
