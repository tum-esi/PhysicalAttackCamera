
# ResNet50

This tool represents the functionality of a object classification algorithm in the application layer. Addtionally, it allows cropping to investigate only the region of interest (ROI). It runs inference twice on the given input image:

1. Correct input image preparation as given in the [PyTorch documentation](https://pytorch.org/get-started/locally/)
2. Wrong input image preparation as performed in the [Adversarial Laser Beams](https://github.com/RjDuan/Advlight/blob/main/test.py)

## Dependencies
* Python 3.12
* [Pillow](https://pypi.org/project/pillow/)
* [PyTorch (inkl. Torchvision)](https://pytorch.org/get-started/locally/)


## Run
General syntax of the tool:

```bash
python resnet.py <image> [<x1,y1> <x2,y2>]
```

* `image` is a file path to the image to analyze. Example: `image1.jpg`
* _Optionally_ the tool can directly analyze only the ROI
    * `<x1,y1>` is the upper left corner for the ROI. Example: `100,100`
    * `<x2,y2>` is the lower right corner for the ROI. Example: `201,201`

## FAQ
* The tool complains, that my ROI is not working
    * Make sure, that the ROI follows the [Bayer pattern](https://en.wikipedia.org/wiki/Bayer_filter), e.g., the upper left corner will have only even coordinates and the lower right corner will have only odd coordinates.