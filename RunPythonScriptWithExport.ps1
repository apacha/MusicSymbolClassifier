$pathToSourceRoot = "C:\Users\Alex\Repositories\MusicSymbolClassifier\HomusTrainer\"
$pathToTranscript = $pathToSourceRoot + "output.txt"

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



Start-Transcript -path $pathToTranscript -append

cd $pathToSourceRoot
echo "Appending source root $($pathToSourceRoot) to temporary PYTHONPATH"
$env:PYTHONPATH = $pathToSourceRoot

#python C:\Users\Alex\Repositories\MusicSymbolClassifier\HomusTrainer\tests\Symbol_test.py
#cd "tests"
#pytest

python C:/Users/Alex/Repositories/MusicSymbolClassifier/HomusTrainer/TrainModel.py --delete_and_recreate_dataset_directory True --model_name vgg -s 3 -offsets 88

Stop-Transcript