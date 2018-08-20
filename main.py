from PIL import Image, ImageFilter
import os
import numpy


IMAGE_DIR = "images"

def main():
    directory = os.fsencode(IMAGE_DIR)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        print("READING {}".format(filename))
        image = Image.open("{}/{}".format(IMAGE_DIR, filename)).convert('L')
        image.show(title="Original")

        # The following is only done in order to compare my method with the built-in methods.
        filtered = image.filter(ImageFilter.MedianFilter())
        filtered.show(title="3x3 Filter (PIL)")
        filtered = image.filter(ImageFilter.MedianFilter(5))
        filtered.show(title="5x5 Filter (PIL)")

if __name__ == '__main__':
    main()