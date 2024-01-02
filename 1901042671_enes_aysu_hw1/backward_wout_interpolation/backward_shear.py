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

for y in range(new_height):
    for x in range(new_width):
        x_old = x - int(y * sx)
        y_old = y - int(x * sy)

        if 0 <= x_old < width and 0 <= y_old < height:
            sheared_data[y, x, :] = np.array(image.getpixel((x_old, y_old)))

sheared_image = Image.fromarray(sheared_data)
sheared_image.save("istanbul_sheared_2.jpg")
sheared_image.show()
