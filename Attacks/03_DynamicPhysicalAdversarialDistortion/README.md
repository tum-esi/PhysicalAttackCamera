# Dynamic Physical Adversarial Distortion - SLAP

This document describes the steps performed to run the SLAP attack by Lovisotto _et al._ (https://github.com/ssloxford/short-lived-adversarial-perturbations) as part of or reproducibility analysis.

**Please Note:** We are _not_ the original authors of SLAP but only provide instructions and utility tools to run the attack!

## Prerequisites:
* [Docker](https://docs.docker.com/get-started/get-docker/)
* Computer with a connected webcam (for profiling step)
* Projector connected to the computer (for profiling step)

## Preparation and Attack Execution

_Hint:_ Since this attack requires hardware access to a functional webcam for initial preparation steps, the preparation steps might be slightly different, especially with necessary patches in [patch.patch](./patch.patch).

1. Get the original source code of the attack and make necessary adaptions to run it:
    * Open a terminal in this folder and run `git clone https://github.com/ssloxford/short-lived-adversarial-perturbations.git`
    * In the terminal, navigate into the newly created folder `cd short-lived-adversarial-perturbations`
    * Apply patches (e.g., USB and display access) with `git apply ../patch.patch`
2. Build and run the Docker container:
    * In the terminal, navigate into the newly created folder `cd short-lived-adversarial-perturbations`
    * Build and start the container with `docker compose up -d`
    * Attach to the container with `docker attach slap_container`
3. Run the profiling:
    * Refer to [Step 1](https://github.com/ssloxford/short-lived-adversarial-perturbations/tree/main/code#1-setup) and [Step 2](https://github.com/ssloxford/short-lived-adversarial-perturbations/tree/main/code#2-run-profiling) of the [original code](https://github.com/ssloxford/short-lived-adversarial-perturbations/blob/main/code/README.md)
4. Run further steps of the attack by following the [original instructions](https://github.com/ssloxford/short-lived-adversarial-perturbations/blob/main/code/README.md)


## Reproduce our results

_Hint:_ Since this attack requires hardware access to a functional webcam for preparation steps, we provide as many data as possible, but the preparation steps must be performed physically.

1. Download all the related data (https://os5.mycloud.com/action/share/46479ae7-0e05-44cf-b551-3fbdfc1a2d3a).
2. Unzip the folder and all its contents
3. Download the related original data from https://github.com/ssloxford/short-lived-adversarial-perturbations/releases/download/usenix21/data.zip. Example: Open a terminal and run `https://github.com/ssloxford/short-lived-adversarial-perturbations/releases/download/usenix21/data.zip`
4. Unzip the folder and all its contents
5. Create a new subfolder `attack_example` inside the folder `short-lived-adversarial-perturbations/data`
6. Copy the `backgrounds` folder (and all its data) from `short-lived-adversarial-perturbations/data/test_run` to `short-lived-adversarial-perturbations/data/attack_example`
7. Create a new folder `objects` in `short-lived-adversarial-perturbations/data/attack_example`
8. Copy the benign stop sign from `<related data>/03_DynamicPhysicalAdversarialDistortion/01_Attack_Preparation/<your target model>/00_benign_stop_sign.png` into `short-lived-adversarial-perturbations/data/attack_example/objects` and rename it to `stop_sign.png`
9. Perform the actual attack as specified in [Preparation and Attack Execution](#preparation-and-attack-execution)
10. The resulting patches will be available in the folder `short-lived-adversarial-perturbations/data/attack_example/optimize/<LUX>/stop_sign/<target model>/_best_projection.png`