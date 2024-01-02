from PIL import Image
import numpy as np

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

        if 0 <= x_old < width and 0 <= y_old < height:
            rotated_data[y, x, :] = np.array(image.getpixel((x_old, y_old)))

rotated_image = Image.fromarray(rotated_data)
rotated_image.save("istanbul_rotated_2.jpg")
rotated_image.show()
