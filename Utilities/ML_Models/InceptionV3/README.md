
# Inception V3

This tool represents the functionality of a object classification algorithm ([Inception V3](https://docs.pytorch.org/vision/main/models/generated/torchvision.models.inception_v3.html#torchvision.models.inception_v3)) in the application layer. Addtionally, it allows cropping to investigate only the region of interest (ROI)

## Dependencies
* Python 3.12
* [Pillow](https://pypi.org/project/pillow/)
* [RawPy](https://pypi.org/project/rawpy/)
* [PyTorch (inkl. Torchvision)](https://pytorch.org/get-started/locally/)


## Run
General syntax of the tool:

```bash
python inceptionV3.py <image> [<x1,y1> <x2,y2>]
```

* `image` is a file path to the image to analyze. Example: `image1.jpg`
* _Optionally_ the tool can directly analyze only the ROI
    * `<x1,y1>` is the upper left corner for the ROI. Example: `100,100`
    * `<x2,y2>` is the lower right corner for the ROI. Example: `201,201`

## FAQ
* The tool complains, that my ROI is not working
    * Make sure, that the ROI follows the [Bayer pattern](https://en.wikipedia.org/wiki/Bayer_filter), e.g., the upper left corner will have only even coordinates and the lower right corner will have only odd coordinates.
* Since Inception v3 requires input images of [299 x 299 px](https://arxiv.org/pdf/1512.00567), there is a pre-process step part of the image classification.