from PIL import Image, ImageFilter
import os
import statistics
import math


IMAGE_DIR = "images"
KERNEL_SIZE = 3
BUFFER_SIZE = math.floor(KERNEL_SIZE/2)


def median_filter(image):
    # The following is only done in order to compare my method with the built-in methods.
    filtered = image.filter(ImageFilter.MedianFilter(KERNEL_SIZE))
    filtered.convert('RGB').save("median_{}".format(filename))

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
    result.convert('RGB').save('results_{}'.format(filename))


if __name__ == '__main__':
    directory = os.fsencode(IMAGE_DIR)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        print("READING {}".format(filename))
        image = Image.open("{}/{}".format(IMAGE_DIR, filename)).convert('L')
        median_filter(image)

