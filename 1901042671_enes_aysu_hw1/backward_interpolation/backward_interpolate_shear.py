from PIL import Image
import numpy as np

def bilinear_interpolation(image, x, y):
    x0, y0 = int(np.floor(x)), int(np.floor(y))
    x1, y1 = x0 + 1, y0 + 1

    if x0 < 0 or y0 < 0 or x1 >= image.width or y1 >= image.height:
        return np.zeros(3, dtype=np.uint8)

    q11 = np.array(image.getpixel((x0, y0)))
    q21 = np.array(image.getpixel((x1, y0)))
    q12 = np.array(image.getpixel((x0, y1)))
    q22 = np.array(image.getpixel((x1, y1)))

    f_x1 = x - x0
    f_x0 = 1 - f_x1
    f_y1 = y - y0
    f_y0 = 1 - f_y1

    pixel_value = f_x0 * (f_y0 * q11 + f_y1 * q12) + f_x1 * (f_y0 * q21 + f_y1 * q22)

    return np.clip(pixel_value, 0, 255).astype(np.uint8)

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

        sheared_data[y, x, :] = bilinear_interpolation(image, x_old, y_old)

sheared_image = Image.fromarray(sheared_data)
sheared_image.save("istanbul_sheared_3.jpg")
sheared_image.show()
