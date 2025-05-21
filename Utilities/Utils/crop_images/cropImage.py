import sys
import platform
import os
from PIL import Image

STORAGE_FOLDER = "cropped"
SEP_CHAR = '/' if not "Windows" in platform.platform() else '\\'

def parseTuple(tupleAsString: str) -> tuple:
    return tuple(int(elem) for elem in tupleAsString.split(','))

def main(imagePath: str, upperLeft=(0,0), lowerRight=(0,0)):
    if not os.path.isdir(STORAGE_FOLDER):
        os.mkdir(STORAGE_FOLDER)

    inputImage = Image.open(imagePath).convert('RGB')
    # Rotation of iPhone images
    if "IMG" in imagePath:
        print("Warning: This is an image probably from an iPhone. It will be rotated by 90°")
        inputImage = inputImage.rotate(90)
    if upperLeft != lowerRight:
        inputImage = inputImage.crop([upperLeft[0], upperLeft[1], lowerRight[0], lowerRight[1]])

    STORAGE_FILENAME = STORAGE_FOLDER + SEP_CHAR + imagePath.split(SEP_CHAR)[-1] + "_cropped_" + ".jpg"

    inputImage.save(STORAGE_FILENAME, quality=100)


if __name__ == "__main__":
    try:
        if len(sys.argv) == 2:
            main(sys.argv[1], (0,0), (0,0))
        elif len(sys.argv) == 4:
            upperLeft = parseTuple(sys.argv[2])
            lowerRight = parseTuple(sys.argv[3])

            # Check if parsed coordinates follow the bayer pattern --> Always jump in "super pixels" (2x2)
            if upperLeft[0] % 2 != 0 or upperLeft[1] % 2 != 0 or \
               lowerRight[0] % 2 == 0 or lowerRight[1] % 2 == 0:
                print("The given coordinates do not match the Bayer pattern")
                sys.exit()
            main(sys.argv[1], upperLeft, lowerRight)
        else:
            print("Please use the following Syntax: python " + sys.argv[0] + " <image.jpg> [<x1,y1> <x2,y2>]")
    except KeyboardInterrupt:
        pass