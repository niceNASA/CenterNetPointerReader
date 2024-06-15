from PIL import Image
from io import BytesIO
import os

path = "images/origin/"
savepath = "images/saved/"

filelist = os.listdir(path)
i = 0
for file in filelist:
    img = Image.open(path + filelist[i])
    if (len(img.split()) != 3) or (img.format != 'JPEG') or (img.mode !='RGB'):
        print(img.mode)
        img = img.convert('RGB')
        bytesIO = BytesIO()
        img.save(bytesIO, format='JPEG', quality=75)
        img = bytesIO.getvalue()
        # os.path.join(savepath, file)
        with open(os.path.join(savepath, file), 'wb') as f:
            f.write(img)
    i = i + 1
