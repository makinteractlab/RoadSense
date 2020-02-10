# RoadSense
Kickboard terrain recognizer

## Software

## How to run final model
### prerequisites
- you need Bitscope connected and working(on windows, prompt should be opened with Administrator)
- tensorflow and keras should be installed (on Surface, open anaconda prompt as Administrator and run : conda activate run)
- 2-way: python eightlayerprediction_gui.py
- 3-way: python eightlayerprediction_tri_gui.py

## code description
### inference
#### eightlayerprediction_tri_gui.py
- inferencing code + gui for 3way classification

#### eightlayerprediction_gui.py
- inferencing code + gui for 2way classification

#### py_bsvml.py
- python library for Bitscope, needs to be in the same directory with the code that uses Bitscope(or append to path if in different location)

#### sample60.py
- for sampling data, 60 samples
- python sample60.py -> click one of the road type -> click start

#### plot.ipynb
- testing code for plotting the data

### model
#### cnn8layer.py
- model file for 8 layer CNN. Directory to this file should be added for those who use this architecture(train & inference)
- when doing training on colab, the training code should be able to locate the file by adding python path(one option is uploading this file to google drive and mounting drive on colab)

#### cnn5layer.py
- model file for 5 layer CNN; same above

### train
#### train_eightlayer_tri.ipynb
- for training, run on colab or jupyter notebook

### checkpoint
- directory for checkpoints

## data
Indoor Data - https://drive.google.com/open?id=101RC0a9M88mY0WIPf8Cyz7w_RYm-u2A2

Indoor Bitscope Data - https://drive.google.com/open?id=101RC0a9M88mY0WIPf8Cyz7w_RYm-u2A2

Real Data - https://drive.google.com/open?id=101RC0a9M88mY0WIPf8Cyz7w_RYm-u2A2
