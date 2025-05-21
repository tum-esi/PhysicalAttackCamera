# Static Physical Adversarial Distortion - RP2

This document describes the steps performed to run the RP2 attack by Eykholt _et al._ (https://github.com/evtimovi/robust_physical_perturbations) as part of or reproducibility analysis.

**Please Note:** We are _not_ the original authors of RP2 but only provide instructions and utility tools to run the attack!

## Prerequisites:
* [Docker](https://docs.docker.com/get-started/get-docker/)

## Preparation
1. Get the original source code of the attack and make necessary adaptions to run it:
    * Open a terminal in this folder and run `git clone https://github.com/evtimovi/robust_physical_perturbations.git`
    * In the terminal, navigate into the newly created folder `cd robust_physical_perturbations`
    * Apply patches (e.g., folder names) with `git apply ../patch.patch`
2. Build the Docker container:
    * In the terminal, navigate into the newly created folder `cd robust_physical_perturbations`
    * Build the container with `docker build -t rp2_attack .`

## Run the attack
1. Start the Docker container
    * Inside the folder `robust_physical_perturbations`, open a terminal and run `docker run -it --rm -v $(pwd):/usr/src/app rp2_attack`
    * Inside the container, start the environment with `pipenv shell`
2. Run the **LISA-CNN attack** script
    * Inside the terminal with the configured environment, go the folder `lisa-cnn-attack` and run `./run_attack_many.sh`
3. Prepare for the **ImageNet attack** script (or Inception v3)
    * When executing the first time: Run `download_inception.sh` the folder `imagenet-attack` to download the InceptionV3 model weights
    * Inside the terminal with the configured environment, go the folder `lisa-cnn-attack` and create a new folder `data`. This new folder should contain three subfolders: `out`, `validation`, `victim`.
    * To run the attack, please refer to [Reproduce our ImageNet results](#reproduce-our-imagenet-results-or-inception-v3)

## Reproduce our LISA-CNN results
1. Download all the related data (https://os5.mycloud.com/action/share/46479ae7-0e05-44cf-b551-3fbdfc1a2d3a).
2. Unzip the folder and all its contents
3. Delete all existing images from `robust_physical_perturbations/lisa-cnn-attack/victim-set`
4. Copy the all images, starting with "01_benign" from `<related data>/02_StaticPhysicalAdversarialDistortion/01_Attack_Preparation/01_LISA_CNN` into `robust_physical_perturbations/lisa-cnn-attack/victim-set`
5. Inside the folder `robust_physical_perturbations`, open a terminal and run `docker run -it --rm -v $(pwd):/usr/src/app rp2_attack`
6. Inside the container, start the environment with `pipenv shell`
7. Inside the terminal with the configured environment, go the folder `lisa-cnn-attack` and run `./run_attack_many.sh`
8. The resulting images will be available in the folder `robust_physical_perturbations/lisa-cnn-attack/optimization_output/l1basedmask_uniformrectangles/noisy_images`
9. As specified in the [original documentation](https://github.com/evtimovi/robust_physical_perturbations/tree/master/lisa-cnn-attack), the adversarial images can be classified using `python manyclassify.py --attack_srcdir optimization_output/l1basedmask_uniformrectangles/noisy_images/`

## Reproduce our ImageNet results (or Inception v3)
1. Download all the related data [**ADD LINK**]. Example: Open a terminal and run `wget [ADD LINK]`
2. Unzip the folder and all its contents
3. Copy the scaled version of the LISA-CNN mask (00_mask.png) from `<related data>/02_StaticPhysicalAdversarialDistortion/01_Attack_Preparation/02_InceptionV3` into `robust_physical_perturbations/imagenet-attack/masks`
4. Copy the benign images, starting with "01_benign" from `<related data>/02_StaticPhysicalAdversarialDistortion/01_Attack_Preparation/02_InceptionV3` into `robust_physical_perturbations/imagenet-attack/data/<subfolder>`, following this assignment:

| **validation**      | **victim**           |
|---------------------|----------------------|
| 01_benign_bright_0  | 01_benign_bright_2   |
| 01_benign_bright_1  | ...                  |
| 01_benign_dark_0    | 01_benign_bright_13  |
| 01_benign_dark_1    | 01_benign_dark_2     |
| 01_benign_partial_0 | ...                  |
| 01_benign_partial_1 | 01_benign_dark_14    |
|                     | 01_benign_partial_2  |
|                     | ...                  |
|                     | 01_benign_partial_12 |

5. Inside the terminal (in the Docker container) with the configured environment, go the folder `imagenet-attack` and run `./run_attack.sh`
6. The resulting patches will be available in the folder `robust_physical_perturbations/imagenet-attack/optimization_output/l1basedmask_uniformrectangles/noisy_images`