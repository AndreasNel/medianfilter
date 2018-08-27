from PIL import Image, ImageFilter
import os
import statistics


IMAGE_DIR = "images"

if __name__ == '__main__':
    directory = os.fsencode(IMAGE_DIR)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        print("READING {}".format(filename))
        image = Image.open("{}/{}".format(IMAGE_DIR, filename)).convert('L')

        # The following is only done in order to compare my method with the built-in methods.
        filtered = image.filter(ImageFilter.MedianFilter(3))
        filtered.convert('RGB').save("median_{}".format(filename))

        maxw = image.width
        maxh = image.height
        result = image.copy()
        for x in range(1, maxw - 1):
            for y in range(1, maxh - 1):
                # Define the box used to get the pixels from the image.
                box = (x - 1, y - 1, x + 2, y + 2)
                # Get the pixels.
                cropped = image.crop(box)
                # Get the median.
                medianvalue = int(statistics.median(cropped.getdata()))
                # Write the resulting pixels to the resulting image.
                result.putpixel((x,y), medianvalue)
        print('Original image: ', end='')
        print([image.getpixel((1,1)), image.getpixel((254,1)), image.getpixel((1,254)), image.getpixel((254,254))])
        print('Built-in function: ', end='')
        print([filtered.getpixel((1,1)), filtered.getpixel((254,1)), filtered.getpixel((1,254)), filtered.getpixel((254,254))])
        print('Mine: ', end='')
        print([result.getpixel((1,1)), result.getpixel((254,1)), result.getpixel((1,254)), result.getpixel((254,254))])
        result.convert('RGB').save('results_{}'.format(filename))
