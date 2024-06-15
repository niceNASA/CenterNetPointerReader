import json
import os
from unicodedata import category

annFile = 'Pointer512_test.json'     #需要调整的文件路径
newFile = 'new_'+annFile
newId = 1                       #新id

with open(annFile, encoding='utf-8') as f:
    line = f.readline()
    d = json.loads(line)

    images = d['images']
    for i in images:
        i['category_ids'] = newId

    cat = d['categories']
    cat[0]['id'] = newId

    ann = d['annotations']
    for i in ann:
        i['category_id'] = newId

    newjson = json.dumps(d)
    new = open(newFile, 'x')
    new.write(newjson)
    new.close()
    f.close()

print('done')