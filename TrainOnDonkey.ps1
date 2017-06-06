$pathToSourceRoot = "C:\Users\Alex\Repositories\MusicSymbolClassifier\HomusTrainer\"
$pathToTranscript = "$($pathToSourceRoot)output"

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

#python C:\Users\Alex\Repositories\MusicSymbolClassifier\HomusTrainer\tests\Symbol_test.py
#cd "tests"
#pytest

Start-Transcript -path "$($pathToTranscript)_1.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/HomusTrainer/TrainModel.py --delete_and_recreate_dataset_directory True --model_name vgg -s 2 -offsets 74,81,88,95 --width 224 --height 128 --minibatch_size 64 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)_2.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/HomusTrainer/TrainModel.py --delete_and_recreate_dataset_directory True --model_name vgg4 -s 2 -offsets 74,81,88,95 --width 224 --height 128 --minibatch_size 64 --optimizer Adadelta
Stop-Transcript
