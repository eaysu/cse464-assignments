from PIL import Image
import numpy as np

image = Image.open("istanbul.jpg")
width, height = image.size

zoom_factor = 1.6

new_width = int(width * zoom_factor)
new_height = int(height * zoom_factor)

scaled_image = Image.new("RGB", (new_width, new_height))

scaled_data = np.zeros((new_height, new_width, 3), dtype=np.uint8)

for y in range(height):
    for x in range(width):
        x_new = int(x * zoom_factor)
        y_new = int(y * zoom_factor)

        if 0 <= x_new < new_width and 0 <= y_new < new_height:
            scaled_data[y_new, x_new, :] = np.array(image.getpixel((x, y)))

scaled_image = Image.fromarray(scaled_data)
scaled_image.save("istanbul_zoomed.jpg")
scaled_image.show()
