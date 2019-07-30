import tesserocr
import requests
from PIL import Image

# r = requests.get('http://my.cnki.net/elibregister/CheckCode.aspx')
# with open('favicon.ico', 'wb') as f:
#     f.write(r.content)
image = Image.open('favicon.ico')
print('直接识别结果：', tesserocr.image_to_text(image))
image = image.convert('L')
image.show()
# image = image.convert('1')
threshold = 127
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
image = image.point(table, '1')
image.show()
print('灰度、二值化处理识别结果：', tesserocr.image_to_text(image))
