#!/bin/zsh
pathToSourceRoot="/Users/rosskuehl/Development/MusicSymbolClassifier/ModelTrainer/"
pathToTranscript="$pathToSourceRoot"

# Allowing wider outputs
stty cols 1500

# Make sure that python finds all modules inside this directory
cd "$pathToSourceRoot"
echo "Appending source root $pathToSourceRoot to temporary PYTHONPATH"
export PYTHONPATH="$pathToSourceRoot"

# Actually start the training with the default-values and without a fixed canvas for the HOMUS dataset
python TrainModel.py --disable_fixed_canvas_size --datasets homus >> "$pathToTranscript/Training_best_model_transcript.txt"
