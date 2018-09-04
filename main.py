from PIL import Image, ImageFilter
import os
import statistics
import math


IMAGE_DIR = "images"
KERNEL_SIZE = 3
BUFFER_SIZE = math.floor(KERNEL_SIZE/2)
TEMPLATE = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0],
]
CENTER = (1, 1)
print("Center point: {}".format(CENTER))
INDICES = [(y, x) for x in range(len(TEMPLATE)) for y in range(len(TEMPLATE[x])) if TEMPLATE[x][y] and (y, x) != CENTER]
print("Mask: {}".format(INDICES))
GRAY_LEVELS = [-1 for _ in range(len(TEMPLATE[0]))]
for idx, i in enumerate(TEMPLATE):
    for j in range(len(i)):
        GRAY_LEVELS[j] += TEMPLATE[idx][j]
print("Gray levels: {}".format(GRAY_LEVELS))


def minkowski_erosion(image):
    maxw = image.width
    maxh = image.height
    result = image.copy()
    for y in range(len(TEMPLATE), maxw - len(TEMPLATE)):
        for x in range(len(TEMPLATE[0]), maxh - len(TEMPLATE[0])):
            box = (x - len(TEMPLATE[0]), y - len(TEMPLATE), x, y)
            cropped = image.crop(box)
            new_gray_value = max(0, min(cropped.getpixel(i) - GRAY_LEVELS[i[0]] for i in INDICES))
            result.putpixel((x, y), new_gray_value)
    return result


def minkowski_dilation(image):
    maxw = image.width
    maxh = image.height
    result = image.copy()
    for y in range(len(TEMPLATE), maxw - len(TEMPLATE)):
        for x in range(len(TEMPLATE[0]), maxh - len(TEMPLATE[0])):
            box = (x - len(TEMPLATE[0]), y - len(TEMPLATE), x, y)
            cropped = image.crop(box)
            new_gray_value = min(255, max(cropped.getpixel(i) + GRAY_LEVELS[i[0]] for i in INDICES))
            result.putpixel((x, y), new_gray_value)
    return result


def median_filter(image):
    # The following is only done in order to compare my method with the built-in methods.
    filtered = image.filter(ImageFilter.MedianFilter(KERNEL_SIZE))
    # filtered.convert('RGB').save("median_{}".format(filename))

    # This is the start of the manual implementation
    maxw = image.width
    maxh = image.height
    result = image.copy()
    for x in range(BUFFER_SIZE, maxw - BUFFER_SIZE):
        for y in range(BUFFER_SIZE, maxh - BUFFER_SIZE):
            # Define the box used to get the pixels from the image.
            box = (x - BUFFER_SIZE, y - BUFFER_SIZE, x + BUFFER_SIZE + 1, y + BUFFER_SIZE + 1)
            # Get the pixels.
            cropped = image.crop(box)
            # Get the median.
            medianvalue = int(statistics.median(cropped.getdata()))
            # Write the resulting pixels to the resulting image.
            result.putpixel((x, y), medianvalue)
    print('Original image: ', end='')
    print([image.getpixel((BUFFER_SIZE, BUFFER_SIZE)), image.getpixel((255 - BUFFER_SIZE, BUFFER_SIZE)),
           image.getpixel((BUFFER_SIZE, 255 - BUFFER_SIZE)), image.getpixel((255 - BUFFER_SIZE, 255 - BUFFER_SIZE))])
    print('Built-in function: ', end='')
    print([filtered.getpixel((BUFFER_SIZE, BUFFER_SIZE)), filtered.getpixel((255 - BUFFER_SIZE, BUFFER_SIZE)),
           filtered.getpixel((BUFFER_SIZE, 255 - BUFFER_SIZE)),
           filtered.getpixel((255 - BUFFER_SIZE, 255 - BUFFER_SIZE))])
    print('Mine: ', end='')
    print([result.getpixel((BUFFER_SIZE, BUFFER_SIZE)), result.getpixel((255 - BUFFER_SIZE, BUFFER_SIZE)),
           result.getpixel((BUFFER_SIZE, 255 - BUFFER_SIZE)), result.getpixel((255 - BUFFER_SIZE, 255 - BUFFER_SIZE))])
    return result


if __name__ == '__main__':
    directory = os.fsencode(IMAGE_DIR)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        print("READING {}".format(filename))
        image = Image.open("{}/{}".format(IMAGE_DIR, filename)).convert('L')
        result = median_filter(image)
        eroded = minkowski_erosion(result)
        dilated = minkowski_dilation(result)
        result.convert('RGB').save('results_{}'.format(filename))
        eroded.convert('RGB').save('eroded_{}'.format(filename))
        dilated.convert('RGB').save('dilated_{}'.format(filename))
