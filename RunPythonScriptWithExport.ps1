$pathToSourceRoot = "C:\Users\Alex\Repositories\MusicSymbolClassifier\HomusTrainer\"
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

#python C:\Users\Alex\Repositories\MusicSymbolClassifier\HomusTrainer\tests\Symbol_test.py
#cd "tests"
#pytest

Start-Transcript -path "$($pathToTranscript)2017-06-08_vgg_staff60-67-74-81_192x96_no_lr_reduction.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/HomusTrainer/TrainModel.py --model_name vgg -s 3 -offsets 60,67,74,81 --width 96 --height 192 --minibatch_size 64 --optimizer Adam --no_dynamic_learning_rate_reduction
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-06-08_vgg4_staff60-67-74-81_192x96_no_lr_reduction.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/HomusTrainer/TrainModel.py --model_name vgg4 -s 3 -offsets 60,67,74,81 --width 96 --height 192 --minibatch_size 64 --optimizer Adam --no_dynamic_learning_rate_reduction
Stop-Transcript

#Start-Transcript -path "$($pathToTranscript)output_3.txt" -append
#python C:/Users/Alex/Repositories/MusicSymbolClassifier/HomusTrainer/TrainModel.py --use_existing_dataset_directory --model_name vgg -s 3 -offsets 74,81,88,95 --width 96 --height 192 --minibatch_size 64 --optimizer SGD
#Stop-Transcript
#
#Start-Transcript -path "$($pathToTranscript)output_4.txt" -append
#python C:/Users/Alex/Repositories/MusicSymbolClassifier/HomusTrainer/TrainModel.py --model_name vgg4 -s 3 -offsets 74,81,88,95 --width 96 --height 192 --minibatch_size 64 --optimizer SGD
#Stop-Transcript
