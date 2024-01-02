from PIL import Image
import numpy as np

image = Image.open("istanbul.jpg")
width, height = image.size

zoom_factor = 1.6

new_width = int(width * zoom_factor)
new_height = int(height * zoom_factor)

scaled_image = Image.new("RGB", (new_width, new_height))

scaled_data = np.zeros((new_height, new_width, 3), dtype=np.uint8)

for y in range(new_height):
    for x in range(new_width):
        x_old = int(x / zoom_factor)
        y_old = int(y / zoom_factor)

        if 0 <= x_old < width and 0 <= y_old < height:
            scaled_data[y, x, :] = np.array(image.getpixel((x_old, y_old)))

scaled_image = Image.fromarray(scaled_data)
scaled_image.save("istanbul_zoomed_2.jpg")
scaled_image.show()
