
# ConvNeXt L

This tool represents the functionality of a object classification algorithm ([ConvNeXt L](https://docs.pytorch.org/vision/main/models/generated/torchvision.models.convnext_large.html#torchvision.models.convnext_large)) in the application layer. Addtionally, it allows cropping to investigate only the region of interest (ROI)

## Dependencies
* Python 3.12
* [Pillow](https://pypi.org/project/pillow/)
* [RawPy](https://pypi.org/project/rawpy/)
* [PyTorch (inkl. Torchvision)](https://pytorch.org/get-started/locally/)


## Run
General syntax of the tool:

```bash
python convnext.py <image> [<x1,y1> <x2,y2>]
```

* `image` is a file path to the image to analyze. Example: `image1.jpg`
* _Optionally_ the tool can directly analyze only the ROI
    * `<x1,y1>` is the upper left corner for the ROI. Example: `100,100`
    * `<x2,y2>` is the lower right corner for the ROI. Example: `201,201`

## FAQ
* The tool complains, that my ROI is not working
    * Make sure, that the ROI follows the [Bayer pattern](https://en.wikipedia.org/wiki/Bayer_filter), e.g., the upper left corner will have only even coordinates and the lower right corner will have only odd coordinates.
* Since ConvNeXt requires input images of 224 x 224 px, there is a pre-process step part of the image classification.