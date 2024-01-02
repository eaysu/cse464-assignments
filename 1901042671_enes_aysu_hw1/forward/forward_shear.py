from PIL import Image
import numpy as np

image = Image.open("istanbul.jpg")
width, height = image.size

sx = 0.5  
sy = 0.0

new_width = width + int(height * sx)
new_height = height + int(width * sy)

sheared_image = Image.new("RGB", (new_width, new_height))

sheared_data = np.zeros((new_height, new_width, 3), dtype=np.uint8)

for y in range(height):
    for x in range(width):
        x_new = x + int(y * sx)
        y_new = y + int(x * sy)

        if 0 <= x_new < new_width and 0 <= y_new < new_height:
            sheared_data[y_new, x_new, :] = np.array(image.getpixel((x, y)))

sheared_image = Image.fromarray(sheared_data)
sheared_image.save("istanbul_sheared.jpg")
sheared_image.show()
