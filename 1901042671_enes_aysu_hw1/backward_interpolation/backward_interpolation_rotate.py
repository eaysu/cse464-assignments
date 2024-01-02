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

angle_degrees = 30
radian = np.radians(angle_degrees)

new_width = int(abs(np.cos(radian) * width) + abs(np.sin(radian) * height))
new_height = int(abs(np.sin(radian) * width) + abs(np.cos(radian) * height))

rotated_image = Image.new("RGB", (new_width, new_height))

center_x = new_width // 2
center_y = new_height // 2

rotated_data = np.zeros((new_height, new_width, 3), dtype=np.uint8)

for y in range(new_height):
    for x in range(new_width):
        x_rel = x - center_x
        y_rel = y - center_y

        x_old = int(x_rel * np.cos(radian) - y_rel * np.sin(radian)) + width // 2
        y_old = int(x_rel * np.sin(radian) + y_rel * np.cos(radian)) + height // 2

        rotated_data[y, x, :] = bilinear_interpolation(image, x_old, y_old)

rotated_image = Image.fromarray(rotated_data)
rotated_image.save("istanbul_rotated_3.jpg")
rotated_image.show()
