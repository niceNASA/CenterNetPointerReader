import os
import matplotlib.pyplot as plt
from PIL import Image

x = [159, 250]
y = [159, 0]

img = Image.open("multi_pose.png")
plt.imshow(img)
plt.plot(x, y)
plt.axis('on')
plt.title('meter')
plt.show()