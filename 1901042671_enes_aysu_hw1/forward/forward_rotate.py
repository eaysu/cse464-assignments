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

for y in range(height):
    for x in range(width):
        x_rel = x - width // 2
        y_rel = y - height // 2

        x_new = int(x_rel * np.cos(-radian) - y_rel * np.sin(-radian)) + center_x
        y_new = int(x_rel * np.sin(-radian) + y_rel * np.cos(-radian)) + center_y

        if 0 <= x_new < new_width and 0 <= y_new < new_height:
            rotated_data[y_new, x_new, :] = np.array(image.getpixel((x, y)))

rotated_image = Image.fromarray(rotated_data)
rotated_image.save("istanbul_rotated.jpg")
rotated_image.show()
