import sys
import platform
import os
import torch
from torchvision.models import resnet50, ResNet50_Weights
from torchvision.io.image import read_image
from torchvision.transforms.functional import crop
from torchvision import transforms
from torch.nn.functional import softmax
from PIL import Image

STORAGE_FOLDER = "classification"
SEP_CHAR = '/' if not "Windows" in platform.platform() else '\\'

def parseTuple(tupleAsString: str) -> tuple:
    return tuple(int(elem) for elem in tupleAsString.split(','))

def preprocess_tensor2(image_tensor):
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                           std=[0.229, 0.224, 0.225])

    preprocess = transforms.Compose([
        transforms.CenterCrop(224),
        normalize
    ])

    # Add batch dimension if not present
    if len(image_tensor.shape) == 3:  # [C, H, W]
        image_tensor = image_tensor.unsqueeze(0)  # Add batch dimension [1, C, H, W]

    image_tensor = preprocess(image_tensor)
    return image_tensor

def processToJpg(imageTensor, filename):
    if imageTensor.size(0) == 1:
        inv = NormalizeInverse(mean = [ 0.485, 0.456, 0.406 ], std = [ 0.229, 0.224, 0.225 ])   # Weights from ImageNet1K
        imageTensor = inv(imageTensor)
        imageTensor = imageTensor.squeeze(0)
    imageTensor = imageTensor.permute(1, 2, 0)  # Change dimensions to [H, W, C]
    imageTensor = imageTensor.mul(255).byte()   # Scale values to [0, 255] and convert to uint8

    imageTensor = Image.fromarray(imageTensor.cpu().numpy())
    imageTensor.save(filename)

# From: https://discuss.pytorch.org/t/simple-way-to-inverse-transform-normalization/4821
class NormalizeInverse(transforms.Normalize):
    """
    Undoes the normalization and returns the reconstructed images in the input domain.
    """

    def __init__(self, mean, std):
        mean = torch.as_tensor(mean)
        std = torch.as_tensor(std)
        std_inv = 1 / (std + 1e-7)
        mean_inv = -mean * std_inv
        super().__init__(mean=mean_inv, std=std_inv)

    def __call__(self, tensor):
        return super().__call__(tensor.clone())

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

    inputImage = Image.open(imagePath).convert('RGB')
    # Rotation of iPhone images
    if "IMG" in imagePath:
        inputImage = inputImage.rotate(90)
    if upperLeft != lowerRight:
        inputImage = inputImage.crop([upperLeft[0], upperLeft[1], lowerRight[0], lowerRight[1]])


    inputImageModification1 = inputImage.resize((256, 256), Image.BILINEAR)
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                           std=[0.229, 0.224, 0.225])
    transform1 = transforms.Compose([
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        normalize,
    ])
    inputImageModification1 = transform1(inputImageModification1).unsqueeze(0)

    # Load Pretrained version of the network
    weights = ResNet50_Weights.IMAGENET1K_V1    # Identified through reverse-engineering of the hash of the downloaded file
    model = resnet50(weights=weights).to(device)
    model.eval()

    # Perform detection
    prediction = model(inputImageModification1)

    probabilities = softmax(prediction[0], dim=0)
    top_prob, top_class = torch.max(probabilities, 0)

    predictionLabel = weights.meta["categories"][top_class]
    probabilityMax = top_prob
    print(f"Correct preparation: {predictionLabel}, {probabilityMax * 100:.2f}%")

    STORAGE_FILENAME = STORAGE_FOLDER + SEP_CHAR + imagePath.split(SEP_CHAR)[-1] + "__" + type(model).__name__ + "_corr.jpg"

    processToJpg(inputImageModification1, STORAGE_FILENAME)

    ########################################
    # Perform 2nd preparation + prediction #
    ########################################
    inputImageModification2 = inputImage.resize((224, 224), Image.BILINEAR)
    inputImageModification2 = transform1(inputImageModification2).unsqueeze(0)

    # Perform detection
    prediction = model(inputImageModification2)

    probabilities = softmax(prediction[0], dim=0)
    top_prob, top_class = torch.max(probabilities, 0)

    predictionLabel = weights.meta["categories"][top_class]
    probabilityMax = top_prob
    print(f"Wrong preparation: {predictionLabel}, {probabilityMax * 100:.2f}%")

    STORAGE_FILENAME = STORAGE_FOLDER + SEP_CHAR + imagePath.split(SEP_CHAR)[-1] + "__" + type(model).__name__ + "_wrong.jpg"

    processToJpg(inputImageModification2, STORAGE_FILENAME)


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