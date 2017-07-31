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

Start-Transcript -path "$($pathToTranscript)TrainingDatasetProvider-Journal.txt" -append
python datasets/TrainingDatasetProvider.py --dataset_directory="data" --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr
Stop-Transcript