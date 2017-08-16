# Music Symbol Classifier

This repository is the model trainer part of the Music Symbol Classifier, which classifies handwritten Music Symbols into 32 different classes using Deep Learning and the HOMUS dataset of handwritten music symbols. It is part of a set of three tools:

|[Model Trainer](https://github.com/apacha/MusicSymbolClassifier)|[Mobile App](https://github.com/apacha/MobileMusicSymbolClassifier)|[Manual Classifier](https://github.com/apacha/ManualMusicSymbolClassifier)|
|:----:|:-----:|:-----:|
|Trains a deep network to automatically classify images of handwritten music symbols into 32 different classes.|Mobile Android application that uses a trained model to perform real-time classification on a mobile device.|A small C#/WPF application that can be used manually classify images, used during evaluation|
|[![Build Status](https://travis-ci.org/apacha/MusicSymbolClassifier.svg?branch=master)](https://travis-ci.org/apacha/MusicSymbolClassifier)|TBD|[![Build status](https://ci.appveyor.com/api/projects/status/2lxb6eg6qnfj9jq5?svg=true)](https://ci.appveyor.com/project/apacha/manualmusicsymbolclassifier)|
|[![codecov](https://codecov.io/gh/apacha/MusicSymbolClassifier/branch/master/graph/badge.svg)](https://codecov.io/gh/apacha/MusicSymbolClassifier)|||

Note my previous project which classifies images into Music scores or something else which can be found in [this](https://github.com/apacha/MusicScoreClassifier) repository on Github.

An extensive overview of the results of different parameters is documented in this [Google Spreadsheet](https://docs.google.com/spreadsheets/d/1D9kHRhrOBogcrr5ko1DleCnHVKGGNkwbBc6_mnfA6XE/edit?usp=sharing)


# Running the application
This repository contains several scripts that can be used independently of each other. 
Before running them, make sure that you have the necessary requirements installed. 

## Requirements

- Python 3.6
- Keras 2.0.6
- Tensorflow 1.2.1 (or optionally tensorflow-gpu 1.2.1)

Optional: If you want to print the graph of the model being trained, install GraphViz on Windows via http://www.graphviz.org/Download_windows.php and add /bin to the PATH or run `sudo apt-get install graphviz` on Ubuntu (see https://github.com/fchollet/keras/issues/3210)

For installing Tensorflow and Keras we recommend using [Anaconda](https://www.continuum.io/downloads) or 
[Miniconda](https://conda.io/miniconda.html) as Python distribution (we did so for preparing Travis-CI and it worked).

To accelerate training even further, you can make use of your GPU, by installing tensorflow-gpu instead of tensorflow
via pip (note that you can only have one of them) and the required Nvidia drivers. For Windows, we recommend the
[excellent tutorial by Phil Ferriere](https://github.com/philferriere/dlwin). For Linux, we recommend using the
 official tutorials by [Tensorflow](https://www.tensorflow.org/install/) and [Keras](https://keras.io/#installation).

## Training the model

Run `python ModelTrainer/TrainModel.py` or `ModelTrainer/TrainBestModel.ps1` for automatically training a neural network with the best available configuration. It will automatically download and extract the HOMUS dataset.

The result of this training is a .h5 (e.g. res_net_4.h5) file that contains the trained model and when running via the PowerShell-script a transcript of the entire training is also created for later investigation.

# License

Published under MIT License,

Copyright (c) 2017 [Alexander Pacha](http://alexanderpacha.com), [TU Wien](https://www.ims.tuwien.ac.at/people/alexander-pacha)

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
