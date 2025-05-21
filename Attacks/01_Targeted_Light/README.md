# Targeted Light Attacks - Adversarial Laser Beams

This document describes the steps performed to run the adversarial laser beams attack by Duan _et al._ (https://github.com/RjDuan/Advlight) as part of or reproducibility analysis.

**Please Note:** We are _not_ the original authors of the adversarial laser beams but only provide instructions and utility tools to run the attack!

## Prerequisites:
* [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) (tested with version 24.1.2)
* [Git](https://git-scm.com/)

## Preparation

1. Prepare the conda environment that includes all Python dependencies:
    * Open a terminal in this folder and run `conda env create -f environment.yml`
2. Get the original source code of the attack and make necessary adaptions to run it:
    * Open a terminal in this folder and run `git clone https://github.com/RjDuan/Advlight`
    * In the terminal, navigate into the newly created folder `cd Advlight`
    * Apply patches (e.g., wavelength constraint) with `git apply ../patch.patch`

## Run the attack
1. Prepare your data
    * Inside the folder `Advlight`, create a folder called `tests`
    * Copy your benign image into this folder
    * Rename the benign file to its benign label (from [ImageNet labels](https://deeplearning.cms.waikato.ac.nz/user-guide/class-maps/IMAGENET/)). E.g., `919.jpg` should depict a "street sign"
2. Open a terminal inside the `Advlight` folder and run `conda activate adversarial_laser_beam`
3. Run `python test.py` to craft adversarial laser beams
4. The results are stored in a subfolder `results` inside `Advlight`

## Reproduce our results
1. Download all the related data [**ADD LINK**]. Example: Open a terminal and run `wget [ADD LINK]`
2. Unzip the folder and all its contents
3. Copy the image `<related data>/01_TargetedLight/01_Attack_Preparation/01_benign.jpg` into `Advlight/tests`
4. Rename the copied file inside `Advlight/tests` into `919.jpg`
5. Open a terminal inside the `Advlight` folder and run `conda activate adversarial_laser_beam`
6. Run `python test.py` to craft adversarial laser beams
7. The results are stored in a subfolder `results` inside `Advlight`