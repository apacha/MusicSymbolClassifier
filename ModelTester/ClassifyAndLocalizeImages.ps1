$pathToSourceRoot = "C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTester\"
$pathToTranscript = "$($pathToSourceRoot)"

# Allowing wider outputs https://stackoverflow.com/questions/7158142/prevent-powergui-from-truncating-the-output
$pshost = get-host
$pswindow = $pshost.ui.rawui
$newsize = $pswindow.buffersize
$newsize.height = 9999
$newsize.width = 1500
$pswindow.buffersize = $newsize

cd $pathToSourceRoot
echo "Appending source root $($pathToSourceRoot) to temporary PYTHONPATH"
$env:PYTHONPATH = $pathToSourceRoot


#Start-Transcript -path "$($pathToTranscript)2017-08-17_vgg4_with_localization.txt" -append
#python "$($pathToSourceRoot)ClassifyAndLocalizeImages.py" --classifier 2017-08-17_vgg4_with_localization.h5 --images C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\3-4-Time\1-13_3.png C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\3-4-Time\1-14_3.png C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\3-4-Time\1-15_3.png C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\3-4-Time\1-16_3.png C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\2-4-Time\1-9_3.png C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\2-4-Time\1-10_3.png C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\2-4-Time\1-11_3.png C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\Barline\1-33_3.png C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\Barline\1-34_3.png C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\Barline\4-35_3.png C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\C-Clef\1-37_3.png C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\C-Clef\1-39_3.png C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\C-Clef\5-38_3.png C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\C-Clef\6-38_3.png C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\C-Clef\8-38_3.png C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\Quarter-Note\1-93_3.png C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\Quarter-Note\1-94_3.png C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\Quarter-Note\1-96_3.png C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\Quarter-Note\2-94_3.png C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\Quarter-Note\3-93_3.png C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\Quarter-Note\6-94_3.png C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\Dot\1-49_3.png C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\Dot\1-50_3.png C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\Dot\1-51_3.png C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\Dot\1-52_3.png C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\Dot\2-49_3.png C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\Whole-Half-Rest\1-145_3.png C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\Whole-Half-Rest\1-146_3.png C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\Whole-Half-Rest\4-145_3.png C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\Whole-Half-Rest\7-145_3.png C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\Whole-Half-Rest\11-145_3.png
#Stop-Transcript


Start-Transcript -path "$($pathToTranscript)2017-08-17_vgg4_with_localization.txt" -append
python "$($pathToSourceRoot)ClassifyAndLocalizeImages.py" --classifier 2017-08-17_vgg4_with_localization.h5 --images C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\data\images\3-4-Time\1-13_3_2.png
Stop-Transcript
