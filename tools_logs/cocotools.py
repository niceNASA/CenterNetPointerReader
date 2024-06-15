from pycocotools.coco import COCO
import os

annFile = os.path.join("", f"Pointer512_val.json")
print(f'Annotation file: {annFile}')

coco = COCO(annFile)

ids = coco.getCatIds('meter')[0]
print(ids)

cats = coco.loadCats(ids)
print(cats)
