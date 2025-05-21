import sys
import platform
import os
import torch
import rawpy
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights
from torchvision.io.image import read_image
from torchvision.utils import draw_bounding_boxes
from torchvision.transforms.functional import to_pil_image, crop

STORAGE_FOLDER = "detection"
SEP_CHAR = '/' if not "Windows" in platform.platform() else '\\'

def parseTuple(tupleAsString: str) -> tuple:
    return tuple(int(elem) for elem in tupleAsString.split(','))

def main(imagePath: str, upperLeft=(0,0), lowerRight=(0,0)):
    if not os.path.isdir(STORAGE_FOLDER):
        os.mkdir(STORAGE_FOLDER)
    
    device = (
        "cuda"
        if torch.cuda.is_available()
        else "mps"
        if torch.backends.mps.is_available()
        else "cpu"
    )
    print(f"Using {device} device\n")

    inputImage = None

    # Read raw files with rawpy and others with built-in methods
    if imagePath.endswith(".dng") or imagePath.endswith(".ARW"):
        inputImage = rawpy.imread(imagePath)

        # Convert raw to jpg using default parameter of rawpy
        # For custom parameters: https://letmaik.github.io/rawpy/api/rawpy.Params.html
        inputImage = inputImage.postprocess()
        inputImage = torch.from_numpy(inputImage)
        inputImage = inputImage.permute(2, 0, 1)
    else:
        inputImage = read_image(imagePath)

    # Crop image using builtin Torch functions
    if upperLeft != lowerRight:
        inputImage = crop(inputImage, upperLeft[1], upperLeft[0], lowerRight[1]-upperLeft[1]+1, lowerRight[0]-upperLeft[0]+1)

    # Load Pretrained version of the network
    weights = FasterRCNN_ResNet50_FPN_V2_Weights.COCO_V1
    model = fasterrcnn_resnet50_fpn_v2(weights=weights, box_score_thresh=0.9).to(device)
    model.eval()

    # Perform detection
    preprocess = weights.transforms()
    inputImage = inputImage.to(device)
    batch = [preprocess(inputImage)]
    prediction = model(batch)

    # Prepare labels for box overlay
    labels = []
    for i in range(len(prediction[0]["labels"])):
        # Add label consisting of category and percentage
        labels.append(weights.meta["categories"][prediction[0]["labels"][i].item()] + \
                      ", " + str(round(prediction[0]["scores"][i].item() * 100, 2)) + "%")
    
    # Export image with bounding boxes
    box = draw_bounding_boxes(inputImage, boxes=prediction[0]["boxes"], labels=labels, colors="red", width=4)
    outputImage = to_pil_image(box.detach())

    STORAGE_FILENAME = STORAGE_FOLDER + SEP_CHAR + imagePath.split(SEP_CHAR)[-1] + "__" + type(model).__name__ + ".jpg"
    outputImage.save(STORAGE_FILENAME, quality=100)

    # Print details of the detected objects (label, score and coordinates)
    for i in range(len(labels)):
        print(labels[i] + ": (" + str(int(round(prediction[0]["boxes"][i][0].item(), 0))) + "|" + \
              str(int(round(prediction[0]["boxes"][i][1].item(), 0))) + ") (" + \
              str(int(round(prediction[0]["boxes"][i][2].item(), 0))) + "|" + \
              str(int(round(prediction[0]["boxes"][i][3].item(), 0))) + ")")


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