import sys
import platform
import os
from PIL import Image

STORAGE_FOLDER = "pattern"
SEP_CHAR = '/' if not "Windows" in platform.platform() else '\\'

def parseTuple(tupleAsString: str) -> tuple:
    return tuple(int(elem) for elem in tupleAsString.split(','))

def main(maskPath: str, adversarialPath: str, destinationPath: str, upperLeft=(0,0), lowerRight=(0,0)):
    if not os.path.isdir(STORAGE_FOLDER):
        os.mkdir(STORAGE_FOLDER)

    maskImage = Image.open(maskPath).convert('RGBA')
    adversarialImage = Image.open(adversarialPath).convert('RGBA')
    destinationImage = Image.open(destinationPath).convert('RGBA')

    destinationImage = destinationImage.resize(maskImage.size, Image.BILINEAR)

    if upperLeft != lowerRight:
        maskImage = maskImage.crop([upperLeft[0], upperLeft[1], lowerRight[0], lowerRight[1]])
        adversarialImage = adversarialImage.crop([upperLeft[0], upperLeft[1], lowerRight[0], lowerRight[1]])
        destinationImage = destinationImage.crop([upperLeft[0], upperLeft[1], lowerRight[0], lowerRight[1]])

    resultImage = Image.new('RGBA', destinationImage.size)

    for x in range(maskImage.width):
        for y in range(maskImage.height):
            pixel1 = maskImage.getpixel((x, y))
            pixel2 = adversarialImage.getpixel((x, y))

            # If pixel1 is completely black (< 2 for any color component), make the result transparent
            if any(component < 2 for component in pixel1[:3]):
                resultImage.putpixel((x, y), (0, 0, 0, 0))
            else:
                resultImage.putpixel((x, y), pixel2)

    outputImage = Image.alpha_composite(destinationImage, resultImage)

    STORAGE_FILENAME = STORAGE_FOLDER + SEP_CHAR + destinationPath.split(SEP_CHAR)[-1] + "_pattern_" + ".jpg"

    outputImage.convert("RGB").save(STORAGE_FILENAME, quality=100)


if __name__ == "__main__":
    try:
        if len(sys.argv) == 4:
            main(sys.argv[1], sys.argv[2], sys.argv[3], (0,0), (0,0))
        elif len(sys.argv) == 6:
            upperLeft = parseTuple(sys.argv[4])
            lowerRight = parseTuple(sys.argv[5])

            # Check if parsed coordinates follow the bayer pattern --> Always jump in "super pixels" (2x2)
            if upperLeft[0] % 2 != 0 or upperLeft[1] % 2 != 0 or \
               lowerRight[0] % 2 == 0 or lowerRight[1] % 2 == 0:
                print("The given coordinates do not match the Bayer pattern")
                sys.exit()
            main(sys.argv[1], upperLeft, lowerRight)
        else:
            print("Please use the following Syntax: python " + sys.argv[0] + " <mask.png> <adversarialPattern.png> <destination.JPG> [<x1,y1> <x2,y2>]")
    except KeyboardInterrupt:
        pass