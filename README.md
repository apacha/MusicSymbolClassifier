# Music Symbol Classifier

This repository is the model trainer part of the Music Symbol Classifier, which classifies handwritten Music Symbols into 32 different classes using Deep Learning and the HOMUS dataset of handwritten music symbols.

Note my previous project which classifies images into Music scores or something else which can be found in [this](https://github.com/apacha/MusicScoreClassifier) repository on Github.

[![Build Status](https://travis-ci.org/apacha/MusicSymbolClassifier.svg?branch=master)](https://travis-ci.org/apacha/MusicSymbolClassifier)
[![codecov](https://codecov.io/gh/apacha/MusicSymbolClassifier/branch/master/graph/badge.svg)](https://codecov.io/gh/apacha/MusicSymbolClassifier)

An extensive overview of the results of different parameters is documented in this [Google Spreadsheet](https://docs.google.com/spreadsheets/d/1D9kHRhrOBogcrr5ko1DleCnHVKGGNkwbBc6_mnfA6XE/edit?usp=sharing)

# Running the application
This repository contains several scripts that can be used independently of each other. 
Before running them, make sure that you have the necessary requirements installed. 

## Requirements

- Python 3.5 (3.6 can be tricky, as of May 2017 [tensorflow does not yet officially support it](https://github.com/tensorflow/tensorflow/issues/6999))
- Keras 2.0.4
- Tensorflow 1.1.0 (or optionally tensorflow-gpu 1.1.0)

Optional: If you want to print the graph of the model being trained, install GraphViz on Windows via http://www.graphviz.org/Download_windows.php and add /bin to the PATH or run `sudo apt-get install graphviz` on Ubuntu (see https://github.com/fchollet/keras/issues/3210)

Note that installing Tensorflow and Keras can be quite a hassle, so we recommend using [Anaconda](https://www.continuum.io/downloads) or 
[Miniconda](https://conda.io/miniconda.html) as Python distribution (we did so for preparing Travis-CI and it worked).

To accelerate training even further, you can make use of your GPU, by installing tensorflow-gpu instead of tensorflow
via pip (note that you can only have one of them) and the required Nvidia drivers. For Windows, we recommend the
[excellent tutorial by Phil Ferriere](https://github.com/philferriere/dlwin). For Linux, we recommend using the
 official tutorials by [Tensorflow](https://www.tensorflow.org/install/) and [Keras](https://keras.io/#installation).

## Training the model

`python TrainModel.py` can be used to training the convolutional neural network. 
It will automatically download and extract the HOMUS dataset.

The result of this training is a .h5 (e.g. vgg.h5) file that contains the trained model.

_Troubleshooting_: If for some reason the download of any of the datasets fails, stop the script, remove the partially
downloaded file and restart the script.

# License

Published under MIT License,

Copyright (c) 2017 [Alexander Pacha](http://my-it.at), [TU Wien](https://www.ims.tuwien.ac.at/people/alexander-pacha)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
