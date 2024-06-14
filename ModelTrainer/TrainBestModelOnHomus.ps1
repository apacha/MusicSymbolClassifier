$pathToSourceRoot = "C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\"
$pathToTranscript = "$($pathToSourceRoot)"

# Allowing wider outputs https://stackoverflow.com/questions/7158142/prevent-powergui-from-truncating-the-output
$pshost = get-host
$pswindow = $pshost.ui.rawui
$newsize = $pswindow.buffersize
$newsize.height = 9999
$newsize.width = 1500
$pswindow.buffersize = $newsize

# Make sure that python finds all modules inside this directory
cd $pathToSourceRoot
echo "Appending source root $($pathToSourceRoot) to temporary PYTHONPATH"
$env:PYTHONPATH = $pathToSourceRoot

# Actually start the training with the default-values and without a fixed canvas for the HOMUS dataset
Start-Transcript -path "$($pathToTranscript)Training_best_model_transcript.txt" -append
python TrainModel.py --disable_fixed_canvas_size --datasets homus
Stop-Transcript