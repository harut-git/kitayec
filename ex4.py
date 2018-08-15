import json
from collections import OrderedDict

with open('clean.json', 'r') as input_file:
    input_data = input_file.read()
data = json.loads(input_data.decode('utf-8'), object_pairs_hook=OrderedDict)
print type(data)
for i in data:
    keyorder = ['pName', 'pId', 'pRating', 'pPicUrl', 'pAbout', 'pBrand', 'pIsGlobalBestSeller', 'pIsKultPick',
                'pVariant', 'pFilter', 'quantity', 'shopOption', 'shopOptionCategory', 'shopOptionCategorySub']
    my_list = sorted(i.items(), key=lambda k: keyorder.index(k[0]))
    i = OrderedDict(my_list)
    check = i['pVariant']
    arr = check.keys()
    for j in arr:
        if 'swatchImgUrl' in check[j]:
            pass
        else:
            check[j]['swatchImgUrl'] = ""

with open('new.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)
