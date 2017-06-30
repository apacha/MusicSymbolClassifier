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

Start-Transcript -path "$($pathToTranscript)2017-06-30_vgg4_with_localization_test.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/HomusTrainer/TestModel.py --model vgg4_with_localization --classifier 2017-06-29_vgg4_with_localization_192x96_multistaff.h5 --images C:\Users\Alex\Desktop\15-40_3_offset_67_1.png C:\Users\Alex\Desktop\15-40_3_offset_67_2.png C:\Users\Alex\Desktop\15-40_3_offset_67_3.png C:\Users\Alex\Desktop\15-40_3_offset_67_4.png C:\Users\Alex\Desktop\15-40_3_offset_67_5.png C:\Users\Alex\Desktop\15-40_3_offset_67_6.png
Stop-Transcript
