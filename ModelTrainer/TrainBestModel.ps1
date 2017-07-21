$pathToSourceRoot = "C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\"
$pathToTranscript = "$($pathToSourceRoot)"

# Allowing wider outputs https://stackoverflow.com/questions/7158142/prevent-powergui-from-truncating-the-output
$pshost = get-host
$pswindow = $pshost.ui.rawui
$newsize = $pswindow.buffersize
$newsize.height = 9999
$newsize.width = 1500
$pswindow.buffersize = $newsize
#$newsize = $pswindow.windowsize
#$newsize.height = 50
#$newsize.width = 150
#$pswindow.windowsize = $newsize

cd $pathToSourceRoot
echo "Appending source root $($pathToSourceRoot) to temporary PYTHONPATH"
$env:PYTHONPATH = $pathToSourceRoot

Start-Transcript -path "$($pathToTranscript)Training_best_model_transcript.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --disable_fixed_canvas_size
Stop-Transcript