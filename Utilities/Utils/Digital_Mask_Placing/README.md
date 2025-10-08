# Digital placement of adversarial patterns

This tool allows to digitally place adversarial patches onto benign images (used for Figures 7b and 7c of our work).

## Dependencies
* Python 3.12
* [Pillow](https://pypi.org/project/pillow/)

## Run
General syntax of the tool:

```bash
python digitalMaskPlacing.py <mask.png> <adversarialPattern.png> <destination.JPG> [<x1,y1> <x2,y2>]
```

* `mask` is a png mask file, containing only black and white pixels: The patch will later only be applied at white pixels.
* `adversarialPattern` is a png image file that contains the adversarial pattern. It will later only be applied on white pixels of the mask
* `destination` is a (benign) JPG image file on which the adversarial patches will be digitally applied.
* _Optionally_ the tool can directly analyze only the ROI
    * `<x1,y1>` is the upper left corner for the ROI. Example: `100,100`
    * `<x2,y2>` is the lower right corner for the ROI. Example: `201,201`

## FAQ
* The tool complains, that my ROI is not working
    * Make sure, that the ROI follows the [Bayer pattern](https://en.wikipedia.org/wiki/Bayer_filter), e.g., the upper left corner will have only even coordinates and the lower right corner will have only odd coordinates.