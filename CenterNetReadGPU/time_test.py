#encoding='utf-8' 
from datetime import datetime

now = datetime.now()
print(now)

path = "D:\\FFOutput\\compare\\images\\240_03.jpg"
index1 = path.rfind('\\') + 1
index2 = path.rfind('.')
print(path[index1:index2])