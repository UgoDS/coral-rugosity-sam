# Rugosity estimator
Welcome to the Rugosity tool.

This tool is designed to help you find the rugosity out of coral landscapes images.

It relies on 2 steps:
- Background identification using [Segment Anything Model](https://github.com/facebookresearch/segment-anything)
- Landscape skyline comparison with ruler size using [OpenCV](https://opencv.org/)

## Process
### 1. Access Google Colab
The user need to run this notebook on [Google Colab](https://colab.research.google.com/?hl=fr).

### 2. Enabling and testing the GPU

First, you'll need to enable GPUs for the notebook:

- Navigate to Edit (Modifier)→Notebook Settings
- select GPU from the Hardware Accelerator drop-down

### 3. Upload your data
Load the images you need to analyse.

### 4. Point several background points
To identify the background, the user needs to give several examples. **Use your mouse to few (3 to 10) points**.

### 5. Pick a rugosity method
There are several ways to compute rugosity, pick one among the several available.

### 6. Save the results on your laptop

## Basic command for the notebook
- Type Cmd/Ctrl+Enter to run the cell in place;