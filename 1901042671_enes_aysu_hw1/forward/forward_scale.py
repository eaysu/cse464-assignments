from PIL import Image
import numpy as np

image = Image.open("istanbul.jpg")
width, height = image.size

scale_factor_x = 2
scale_factor_y = 2

new_width = int(width * scale_factor_x)
new_height = int(height * scale_factor_y)

scaled_image = Image.new("RGB", (new_width, new_height))

scaled_data = np.zeros((new_height, new_width, 3), dtype=np.uint8)

for y in range(height):
    for x in range(width):
        x_new = int(x * scale_factor_x)
        y_new = int(y * scale_factor_y)

        if 0 <= x_new < new_width and 0 <= y_new < new_height:
            scaled_data[y_new, x_new, :] = np.array(image.getpixel((x, y)))

scaled_image = Image.fromarray(scaled_data)
scaled_image.save("istanbul_scaled.jpg")
scaled_image.show()
