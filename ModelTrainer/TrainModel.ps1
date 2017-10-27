$pathToSourceRoot = "C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\"
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

#python C:\Users\Alex\Repositories\MusicSymbolClassifier\ModelTrainer\tests\Symbol_test.py
#cd "tests"
#pytest


################################################
# Upcoming Trainings 
################################################

##########################################################
# Models that performed best exclusively on HOMUS dataset
##########################################################
exit
# Best Models for 96x96 images without fixed canvas size
Start-Transcript -path "$($pathToTranscript)2017-07-19_vgg4_96x96_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-19_res_net_4_96x96_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_4 -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

# Best Model for 192x96 images with fixed canvas size
Start-Transcript -path "$($pathToTranscript)2017-07-19_res_net_3_4_small_192x96_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 3 --width 96 --height 192 --minibatch_size 16 --optimizer Adadelta
Stop-Transcript

##########################################################
# Models that performed best on joint datasets
##########################################################
Start-Transcript -path "$($pathToTranscript)2017-08-07_res_net_3_small_48x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr
Stop-Transcript

#######################################################
# Below are configurations that already were 
# started on a machine and should not run again, 
# so we will terminate this PS-script here
# but retain those configurations for documentation
#######################################################
exit


# Started on Donkey, 19.10.2017
Start-Transcript -path "$($pathToTranscript)2017-10-19_res_net_3_skBalance_96x96_no_fixed_canvas_Adadelta_mb16_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3 -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr --class_weights_balancing_method skBalance
Stop-Transcript

# Started on Donkey, 18.10.2017
Start-Transcript -path "$($pathToTranscript)2017-10-17_vgg4_simpleBalance_96x96_no_fixed_canvas_Adadelta_mb16_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr --class_weights_balancing_method simple
Stop-Transcript

# Started on Donkey, 17.10.2017
Start-Transcript -path "$($pathToTranscript)2017-10-17_vgg4_skBalance_96x96_no_fixed_canvas_Adadelta_mb16_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr --class_weights_balancing_method skBalance
Stop-Transcript

# Started on Monsti, 17.10.2017
Start-Transcript -path "$($pathToTranscript)2017-10-17_res_net_3_small_simpleBalance_96x96_no_fixed_canvas_Adadelta_mb16_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr --class_weights_balancing_method simple
Stop-Transcript

# Started on Donkey, 16.10.2017
Start-Transcript -path "$($pathToTranscript)2017-10-16_res_net_3_small_skBalance_96x96_no_fixed_canvas_Adadelta_mb16_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr --class_weights_balancing_method skBalance
Stop-Transcript

# Started on Donkey, 28.08.2017
Start-Transcript -path "$($pathToTranscript)2017-08-28_res_net_3_small_with_localization_112x112_Adadelta_mb32_loss-weights-0.998-0.002.txt" -append
python "$($pathToTranscript)TrainModel.py" --model_name res_net_3_small_with_localization -s 3 --width 112 --height 112 --minibatch_size 32 --optimizer Adadelta --random_position_on_canvas -offsets 28
Stop-Transcript


# Started on Donkey, 28.08.2017
Start-Transcript -path "$($pathToTranscript)2017-08-28_res_net_3_small_with_localization_112x112_Adadelta_mb32_loss-weights-0.8-0.2.txt" -append
python "$($pathToTranscript)TrainModel.py" --model_name res_net_3_small_with_localization -s 3 --width 112 --height 112 --minibatch_size 32 --optimizer Adadelta --random_position_on_canvas -offsets 28
Stop-Transcript

# Started on Monsti, 20.08.2017
Start-Transcript -path "$($pathToTranscript)2017-08-20_res_net_3_small_with_localization_112x112_Adadelta_mb16.txt" -append
python "$($pathToTranscript)TrainModel.py" --model_name res_net_3_small_with_localization -s 3 --width 112 --height 112 --minibatch_size 16 --optimizer Adadelta --random_position_on_canvas -offsets 28
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-08-20_vgg4_with_localization_112x112_Adadelta_mb16.txt" -append
python "$($pathToTranscript)TrainModel.py" --model_name vgg4_with_localization -s 3 --width 112 --height 112 --minibatch_size 16 --optimizer Adadelta --random_position_on_canvas -offsets 28
Stop-Transcript

# Started on Monsti, 19.08.2017
Start-Transcript -path "$($pathToTranscript)2017-08-19_res_net_3_small_with_localization_112x112_Adadelta_mb32.txt" -append
python "$($pathToTranscript)TrainModel.py" --model_name res_net_3_small_with_localization -s 3 --width 112 --height 112 --minibatch_size 32 --optimizer Adadelta --random_position_on_canvas -offsets 28
Stop-Transcript

# Started on Monsti, 19.08.2017
Start-Transcript -path "$($pathToTranscript)2017-08-19_vgg4_with_localization_112x112_Adadelta_mb32.txt" -append
python "$($pathToTranscript)TrainModel.py" --model_name vgg4_with_localization -s 3 --width 112 --height 112 --minibatch_size 32 --optimizer Adadelta --random_position_on_canvas -offsets 28
Stop-Transcript

# Started on Donkey, 17.08.2017
Start-Transcript -path "$($pathToTranscript)2017-08-17_vgg4_with_localization_112x112_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4_with_localization -s 3 --width 112 --height 112 --minibatch_size 32 --optimizer Adadelta --random_position_on_canvas
Stop-Transcript


# Started on Donkey, 07.08.2017

# rerun failed scripts
Start-Transcript -path "$($pathToTranscript)2017-08-07_res_net_5_48x48_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5 -s 3 --width 48 --height 48 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-08-07_vgg_48x48_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 3 --width 48 --height 48 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-08-07_vgg4_48x48_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 3 --width 48 --height 48 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr
Stop-Transcript

# 48x96, mb-32

Start-Transcript -path "$($pathToTranscript)2017-08-07_res_net_1_48x48_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_1 -s 3 --width 48 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-08-07_res_net_2_48x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_2 -s 3 --width 48 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-08-07_res_net_3_48x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3 -s 3 --width 48 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-08-07_res_net_3_small_48x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 3 --width 48 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-08-07_res_net_4_48x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_4 -s 3 --width 48 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-08-07_res_net_5_48x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5 -s 3 --width 48 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-08-07_res_net_5_small_48x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5_small -s 3 --width 48 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-08-07_vgg_48x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 3 --width 48 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-08-07_vgg4_48x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 3 --width 48 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr
Stop-Transcript


# Started on Donkey, 05.08.2017
# rerun failed scripts
Start-Transcript -path "$($pathToTranscript)2017-08-05_res_net_5_small_96x96_no_fixed_canvas_Adadelta_mb16_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5_small -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-08-05_res_net_3_small_96x96_no_fixed_canvas_Adadelta_mb16_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr
Stop-Transcript

# 48x48, mb-32
Start-Transcript -path "$($pathToTranscript)2017-08-05_res_net_1_48x48_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_1 -s 3 --width 48 --height 48 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-08-05_res_net_3_48x48_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3 -s 3 --width 48 --height 48 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-08-05_res_net_3_small_48x48_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 3 --width 48 --height 48 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-08-05_res_net_5_48x48_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5 -s 3 --width 48 --height 48 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-08-05_res_net_5_small_48x48_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5_small -s 3 --width 48 --height 48 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr
Stop-Transcript


# Started on Donkey, 03.08.2017
Start-Transcript -path "$($pathToTranscript)2017-08-03_res_net_5_small_96x96_no_fixed_canvas_Adadelta_mb16_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5_small -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-08-03_vgg_96x96_no_fixed_canvas_Adadelta_mb16_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-08-03_vgg4_96x96_no_fixed_canvas_Adadelta_mb16_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-08-03_res_net_1_96x96_no_fixed_canvas_Adadelta_mb16_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_1 -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-08-03_res_net_2_96x96_no_fixed_canvas_Adadelta_mb16_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_2 -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr
Stop-Transcript

# Started on Donkey, 31.07.2017
Start-Transcript -path "$($pathToTranscript)2017-07-31_res_net_3_96x96_no_fixed_canvas_Adadelta_mb16_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3 -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-31_res_net_3_small_96x96_no_fixed_canvas_Adadelta_mb16_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-31_res_net_4_96x96_no_fixed_canvas_Adadelta_mb16_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_4 -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-31_res_net_5_96x96_no_fixed_canvas_Adadelta_mb16_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes_openomr.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5 -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes,openomr
Stop-Transcript

# Started on Donkey, 30.07.2017
Start-Transcript -path "$($pathToTranscript)2017-07-30_res_net_5_96x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5 -s 3 --width 96 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-30_res_net_1_96x96_no_fixed_canvas_Adadelta_mb16_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_1 -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-30_res_net_2_96x96_no_fixed_canvas_Adadelta_mb16_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_2 -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes
Stop-Transcript

# Started on Donkey, 28.07.2017
Start-Transcript -path "$($pathToTranscript)2017-07-28_res_net_2_96x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_2 -s 3 --width 96 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-28_res_net_3_96x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3 -s 3 --width 96 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-28_res_net_3_small_96x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 3 --width 96 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-28_vgg4_96x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 3 --width 96 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-28_res_net_4_96x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_4 -s 3 --width 96 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-28_res_net_5_small_96x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5_small -s 3 --width 96 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-28_res_net_1_96x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_1 -s 3 --width 96 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-26_vgg_96x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp_fornes.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 3 --width 96 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp,fornes
Stop-Transcript

# Started on Monsti, 27.07.2017
Start-Transcript -path "$($pathToTranscript)2017-07-27_vgg_96x96_no_fixed_canvas_Adadelta_mb16_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp
Stop-Transcript

# Started on Donkey, 27.07.2017
Start-Transcript -path "$($pathToTranscript)2017-07-27_vgg4_96x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 3 --width 96 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-27_res_net_1_96x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_1 -s 3 --width 96 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp
Stop-Transcript

# Started on Donkey, 26.07.2017
Start-Transcript -path "$($pathToTranscript)2017-07-26_vgg_96x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed_audiveris_muscima_pp.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 3 --width 96 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed,audiveris,muscima_pp
Stop-Transcript

# Started on Donkey, 23.07.2017
Start-Transcript -path "$($pathToTranscript)2017-07-23_vgg_96x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 3 --width 96 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-23_vgg4_96x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 3 --width 96 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-23_res_net_1_96x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_1 -s 3 --width 96 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-23_res_net_2_96x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_2 -s 3 --width 96 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-23_res_net_3_96x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3 -s 3 --width 96 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-23_res_net_3_small_96x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 3 --width 96 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-23_res_net_4_96x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_4 -s 3 --width 96 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-23_res_net_5_96x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5 -s 3 --width 96 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-23_res_net_5_small_96x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5_small_reduced -s 3 --width 96 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed
Stop-Transcript

# Started on Donkey, 21.07.2017
Start-Transcript -path "$($pathToTranscript)2017-07-21_res_net_4_96x96_no_fixed_canvas_Adadelta_mb16_homus_rebelo1_rebelo2_printed.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_4 -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-22_res_net_4_96x96_no_fixed_canvas_Adadelta_mb32_homus_rebelo1_rebelo2_printed.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_4 -s 3 --width 96 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-22_res_net_4_96x96_no_fixed_canvas_Adadelta_mb64_homus_rebelo1_rebelo2_printed.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_4 -s 3 --width 96 --height 96 --minibatch_size 64 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-22_vgg_96x96_no_fixed_canvas_Adadelta_mb16_homus_rebelo1_rebelo2_printed.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-22_vgg4_96x96_no_fixed_canvas_Adadelta_mb16_homus_rebelo1_rebelo2_printed.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-22_res_net_1_96x96_no_fixed_canvas_Adadelta_mb16_homus_rebelo1_rebelo2_printed.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_1 -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-22_res_net_2_96x96_no_fixed_canvas_Adadelta_mb16_homus_rebelo1_rebelo2_printed.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_2 -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-22_res_net_3_96x96_no_fixed_canvas_Adadelta_mb16_homus_rebelo1_rebelo2_printed.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3 -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-22_res_net_3_small_96x96_no_fixed_canvas_Adadelta_mb16_homus_rebelo1_rebelo2_printed.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-22_res_net_4_96x96_no_fixed_canvas_Adadelta_mb16_homus_rebelo1_rebelo2_printed.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_4 -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-22_res_net_5_96x96_no_fixed_canvas_Adadelta_mb16_homus_rebelo1_rebelo2_printed.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5 -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-22_res_net_5_small_96x96_no_fixed_canvas_Adadelta_mb16_homus_rebelo1_rebelo2_printed.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5_small_reduced -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size --datasets homus,rebelo1,rebelo2,printed
Stop-Transcript


# Started on Donkey, 19.07.2017
Start-Transcript -path "$($pathToTranscript)2017-07-19_res_net_3_5_small_192x96_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 3 --width 96 --height 192 --minibatch_size 16 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-19_res_net_3_96x96_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3 -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-19_res_net_3_2_96x96_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3 -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-20_res_net_4_2_96x96_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_4 -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-19_vgg_96x96_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-19_vgg_2_96x96_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

# Started on Donkey, 13.07.2017
Start-Transcript -path "$($pathToTranscript)2017-07-13_vgg_reduced_24x24_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg_reduced -s 3 --width 24 --height 24 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-13_vgg4_reduced_24x24_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4_reduced -s 3 --width 24 --height 24 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-13_res_net_1_reduced_24x24_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_1_reduced -s 3 --width 24 --height 24 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-13_res_net_2_reduced_24x24_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_2_reduced -s 3 --width 24 --height 24 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-13_res_net_3_reduced_24x24_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_reduced -s 3 --width 24 --height 24 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-13_res_net_3_small_reduced_24x24_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small_reduced -s 3 --width 24 --height 24 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-13_res_net_4_reduced_24x24_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_4_reduced -s 3 --width 24 --height 24 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-13_res_net_5_reduced_24x24_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5_reduced -s 3 --width 24 --height 24 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-13_res_net_5_small_reduced_24x24_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5_small_reduced -s 3 --width 24 --height 24 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

# Started on Monsti, 11.07.2017
Start-Transcript -path "$($pathToTranscript)2017-07-11_vgg_small_48x48_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 3 --width 48 --height 48 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-11_vgg_small_96x48_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 3 --width 48 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-11_vgg_small_96x96_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-11_vgg_small_192x96_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 3 --width 96 --height 192 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-11_vgg4_small_48x48_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 3 --width 48 --height 48 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-11_vgg4_small_96x48_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 3 --width 48 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-11_vgg4_small_96x96_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-11_vgg4_small_192x96_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 3 --width 96 --height 192 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

# Started on Donkey, 11.07.2017
Start-Transcript -path "$($pathToTranscript)2017-07-11_res_net_5_small_48x48_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5_small -s 3 --width 48 --height 48 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-11_res_net_5_small_96x48_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5_small -s 3 --width 48 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-11_res_net_3_small_stroke_1_48x48_no_fixed_canvas_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 1 --width 48 --height 48 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-11_res_net_3_small_stroke_2_48x48_no_fixed_canvas_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 2 --width 48 --height 48 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-11_res_net_3_small_stroke_3_48x48_no_fixed_canvas_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 3 --width 48 --height 48 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-11_res_net_1_48x48_no_fixed_canvas_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_1 -s 3 --width 48 --height 48 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-11_res_net_1_96x48_no_fixed_canvas_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_1 -s 3 --width 48 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-11_res_net_2_96x96_no_fixed_canvas_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_2 -s 3 --width 96 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-11_res_net_2_192x96_no_fixed_canvas_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_2 -s 3 --width 96 --height 192 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-11_res_net_3_48x48_no_fixed_canvas_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3 -s 3 --width 48 --height 48 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-11_res_net_3_96x48_no_fixed_canvas_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3 -s 3 --width 48 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-11_res_net_4_96x96_no_fixed_canvas_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_4 -s 3 --width 96 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-11_res_net_4_192x96_no_fixed_canvas_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_4 -s 3 --width 96 --height 192 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-11_res_net_5_48x48_no_fixed_canvas_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5 -s 3 --width 48 --height 48 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-11_res_net_5_96x48_no_fixed_canvas_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5 -s 3 --width 48 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-11_res_net_5_small_48x48_no_fixed_canvas_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5_small -s 3 --width 48 --height 48 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-11_res_net_5_small_96x48_no_fixed_canvas_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5_small -s 3 --width 48 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript


# Started on Donkey, 10.07.2017
Start-Transcript -path "$($pathToTranscript)2017-07-10_res_net_3_small_stroke_1_48x48_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 1 --width 48 --height 48 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-10_res_net_3_small_stroke_2_48x48_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 2 --width 48 --height 48 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-10_res_net_3_small_stroke_3_48x48_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 3 --width 48 --height 48 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-10_res_net_1_48x48_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_1 -s 3 --width 48 --height 48 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-10_res_net_1_96x48_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_1 -s 3 --width 48 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-10_res_net_2_96x96_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_2 -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-10_res_net_2_192x96_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_2 -s 3 --width 96 --height 192 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-10_res_net_3_48x48_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3 -s 3 --width 48 --height 48 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-10_res_net_3_96x48_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3 -s 3 --width 48 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-10_res_net_4_96x96_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_4 -s 3 --width 96 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-10_res_net_4_192x96_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_4 -s 3 --width 96 --height 192 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-10_res_net_5_48x48_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5 -s 3 --width 48 --height 48 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-10_res_net_5_96x48_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5 -s 3 --width 48 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript


# Started on Monsti, 10.07.2017
Start-Transcript -path "$($pathToTranscript)2017-07-10_vgg4_48x48_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 3 --width 48 --height 48 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-10_res_net_3_small_48x48_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 3 --width 48 --height 48 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-10_res_net_3_small_48x96_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 3 --width 48 --height 96 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-10_res_net_3_small_192x96_no_fixed_canvas_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 3 --width 96 --height 192 --minibatch_size 16 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

# Started on Donkey, 10.07.2017
Start-Transcript -path "$($pathToTranscript)2017-07-10_res_net_3_small_192x96_no_fixed_canvas_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 3 --width 96 --height 192 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-10_res_net_3_small_96x48_no_fixed_canvas_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 3 --width 48 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-10_res_net_3_small_48x48_no_fixed_canvas_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 3 --width 48 --height 96 --minibatch_size 32 --optimizer Adadelta --disable_fixed_canvas_size
Stop-Transcript

# Started on Donkey, 07.07.2017
Start-Transcript -path "$($pathToTranscript)2017-07-07_res_net_3_small_192x96_Adam_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 3 --width 96 --height 192 --minibatch_size 32 --optimizer Adam
Stop-Transcript

# Started on Donkey, 06.07.2017
Start-Transcript -path "$($pathToTranscript)2017-07-06_res_net_5_staff74_192x96_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5 -s 3 -offsets 74 --width 96 --height 192 --minibatch_size 16 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-06_res_net_3_small_staff74_192x96_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 3 -offsets 74 --width 96 --height 192 --minibatch_size 16 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-06_res_net_3_small_staff74_192x96_Adam_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 3 -offsets 74 --width 96 --height 192 --minibatch_size 32 --optimizer Adam
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-06_res_net_3_small_staff74_192x96_Adam_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 3 -offsets 74 --width 96 --height 192 --minibatch_size 16 --optimizer Adam
Stop-Transcript

# Started on Donkey, 05.07.2017
Start-Transcript -path "$($pathToTranscript)2017-07-05_res_net_3_small_staff74_192x96_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 3 -offsets 74 --width 96 --height 192 --minibatch_size 32 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-05_res_net_3_staff74_192x96_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3 -s 3 -offsets 74 --width 96 --height 192 --minibatch_size 32 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-05_res_net_4_staff74_192x96_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_4 -s 3 -offsets 74 --width 96 --height 192 --minibatch_size 32 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-05_res_net_5_small_staff74_192x96_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5_small -s 3 -offsets 74 --width 96 --height 192 --minibatch_size 32 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-05_res_net_5_staff74_192x96_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5 -s 3 -offsets 74 --width 96 --height 192 --minibatch_size 32 --optimizer Adadelta
Stop-Transcript

# Started on Monsti, 03.07.2017
Start-Transcript -path "$($pathToTranscript)2017-07-03_res_net_5_small_192x96_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5_small -s 3 --width 96 --height 192 --minibatch_size 16 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-03_res_net_5_192x96_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5 -s 3 --width 96 --height 192 --minibatch_size 16 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-03_res_net_4_192x96_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_4 -s 3 --width 96 --height 192 --minibatch_size 16 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-03_res_net_3_small_192x96_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 3 --width 96 --height 192 --minibatch_size 16 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-03_res_net_3_192x96_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3 -s 3 --width 96 --height 192 --minibatch_size 16 --optimizer Adadelta
Stop-Transcript

# Started on Donkey, 04.07.2017
Start-Transcript -path "$($pathToTranscript)2017-07-04_res_net_3_small_192x96_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 3 --width 96 --height 192 --minibatch_size 16 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-04_res_net_3_small_192x96_Adadelta_mb8.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 3 --width 96 --height 192 --minibatch_size 8 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-04_res_net_3_small_stroke2_192x96_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 2 --width 96 --height 192 --minibatch_size 16 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-04_res_net_3_small_stroke1_192x96_Adadelta_mb16.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 1 --width 96 --height 192 --minibatch_size 16 --optimizer Adadelta
Stop-Transcript

# Started on Donkey, 03.07.2017
Start-Transcript -path "$($pathToTranscript)2017-07-03_vgg_192x96_Adadelta_mb64.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 3 --width 96 --height 192 --minibatch_size 64 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-03_vgg_192x96_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 3 --width 96 --height 192 --minibatch_size 32 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-03_vgg4_192x96_Adadelta_mb64.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 3 --width 96 --height 192 --minibatch_size 64 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-03_vgg4_192x96_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 3 --width 96 --height 192 --minibatch_size 32 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-03_res_net_3_192x96_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3 -s 3 --width 96 --height 192 --minibatch_size 32 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-03_res_net_3_small_192x96_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_3_small -s 3 --width 96 --height 192 --minibatch_size 32 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-03_res_net_4_192x96_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_4 -s 3 --width 96 --height 192 --minibatch_size 32 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-03_res_net_5_192x96_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5 -s 3 --width 96 --height 192 --minibatch_size 32 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-07-03_res_net_5_small_192x96_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_5_small -s 3 --width 96 --height 192 --minibatch_size 32 --optimizer Adadelta
Stop-Transcript

# Started on Donkey, 30.06.2017
Start-Transcript -path "$($pathToTranscript)2017-06-30_res_net_192x96_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net -s 3 --width 96 --height 192 --minibatch_size 32 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-06-30_res_net_192x96_Adadelta_mb64.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net -s 3 --width 96 --height 192 --minibatch_size 64 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-06-30_res_net_2_192x96_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_2 -s 3 --width 96 --height 192 --minibatch_size 32 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-06-30_res_net_2_192x96_Adadelta_mb64.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name res_net_2 -s 3 --width 96 --height 192 --minibatch_size 64 --optimizer Adadelta
Stop-Transcript

# Started on Donkey, 28.06.2017
Start-Transcript -path "$($pathToTranscript)2017-06-28_vgg4_with_localization_192x96_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4_with_localization -s 3 --width 96 --height 192 --minibatch_size 32 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-06-28_vgg4_with_localization_staff74_192x96_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4_with_localization -s 3 -offsets 74 --width 96 --height 192 --minibatch_size 32 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-06-28_vgg4_with_localization_staff60-67-74-81_192x96_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4_with_localization -s 3 -offsets 60,67,74,81 --width 96 --height 192 --minibatch_size 32 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-06-28_vgg4_with_localization_224x128_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4_with_localization -s 3 --width 128 --height 224 --minibatch_size 32 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-06-28_vgg4_with_localization_staff88_224x128_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4_with_localization -s 3 -offsets 74 --width 128 --height 224 --minibatch_size 32 --optimizer Adadelta
Stop-Transcript

Start-Transcript -path "$($pathToTranscript)2017-06-28_vgg4_with_localization_staff74-81-88-95_224x128_Adadelta_mb32.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4_with_localization -s 3 -offsets 60,67,74,81 --width 128 --height 224 --minibatch_size 32 --optimizer Adadelta
Stop-Transcript

# Started on Donkey, 21.06.2017, 15:30
Start-Transcript -path "$($pathToTranscript)2017-06-21_vgg_staff74_192x96_Adadelta.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 3 -offsets 74 --width 96 --height 192 --minibatch_size 64 --optimizer Adadelta
Stop-Transcript

# Started on Donkey, 21.06.2017, 15:30
Start-Transcript -path "$($pathToTranscript)2017-06-21_vgg_staff60-67-74-81_192x96_Adadelta.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 3 -offsets 60,67,74,81 --width 96 --height 192 --minibatch_size 64 --optimizer Adadelta
Stop-Transcript

# Started on Donkey, 21.06.2017, 15:30
Start-Transcript -path "$($pathToTranscript)2017-06-21_vgg_staff60-67-74-81_192x96_Adam.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 3 -offsets 60,67,74,81 --width 96 --height 192 --minibatch_size 64 --optimizer Adam
Stop-Transcript

# Started on Donkey, 21.06.2017, 15:30
Start-Transcript -path "$($pathToTranscript)2017-06-21_vgg4_staff60-67-74-81_192x96_Adam.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 3 -offsets 60,67,74,81 --width 96 --height 192 --minibatch_size 64 --optimizer Adam
Stop-Transcript

# Started on Donkey, 11.06.2017, 23:00
Start-Transcript -path "$($pathToTranscript)2017-06-12_vgg4_staff74_192x96_Adam.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 3 -offsets 74 --width 96 --height 192 --minibatch_size 64 --optimizer Adam
Stop-Transcript

# Started on Donkey, 11.06.2017, 23:00
Start-Transcript -path "$($pathToTranscript)2017-06-12_vgg4_staff74_192x96_Adam2.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 3 -offsets 74 --width 96 --height 192 --minibatch_size 64 --optimizer Adam
Stop-Transcript

# Started on Donkey, 11.06.2017, 23:00
Start-Transcript -path "$($pathToTranscript)2017-06-12_vgg4_staff74_192x96_Adam_mb128.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 3 -offsets 74 --width 96 --height 192 --minibatch_size 128 --optimizer Adam
Stop-Transcript

# Started on Donkey, 11.06.2017, 23:00
Start-Transcript -path "$($pathToTranscript)2017-06-12_vgg4_staff74_192x96_Adadelta_mb128.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 3 -offsets 74 --width 96 --height 192 --minibatch_size 128 --optimizer Adadelta
Stop-Transcript

# Started on Donkey, 11.06.2017, 23:00
Start-Transcript -path "$($pathToTranscript)2017-06-12_vgg4_staff74_192x96_Adadelta2_mb128.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 3 -offsets 74 --width 96 --height 192 --minibatch_size 128 --optimizer Adadelta
Stop-Transcript

# Started on Donkey, 12.06.2017, 10:00
Start-Transcript -path "$($pathToTranscript)2017-06-12_vgg4_stroke1-2-3_staff74-81-88-95_192x96_Adadelta.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 1,2,3 -offsets 60,67,74,81 --width 96 --height 192 --minibatch_size 64 --optimizer Adadelta
Stop-Transcript

# Started on Donkey, 11.06.2017, 10:00
Start-Transcript -path "$($pathToTranscript)2017-06-11_vgg4_staff74_192x96_Adadelta.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 3 -offsets 74 --width 96 --height 192 --minibatch_size 64 --optimizer Adadelta
Stop-Transcript

# Started on Donkey, 11.06.2017, 10:00
Start-Transcript -path "$($pathToTranscript)2017-06-11_vgg4_staff74_192x96_Adadelta2.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 3 -offsets 74 --width 96 --height 192 --minibatch_size 64 --optimizer Adadelta
Stop-Transcript

##### Large dataset with vgg

# Started on Donkey, 10.06.2017, 10:00
Start-Transcript -path "$($pathToTranscript)2017-06-08_vgg_stroke1-2-3_staff74-81-88-95.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 1,2,3 -offsets 74,81,88,95 --width 128 --height 224 --minibatch_size 64 --optimizer Adadelta
Stop-Transcript


##### Smaller image-sizes, 4 different staff-lines

# Started on Donkey, 09.06.2017, 18:00
Start-Transcript -path "$($pathToTranscript)2017-06-09_vgg_staff60-67-74-81_192x96_Adam.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 3 -offsets 60,67,74,81 --width 96 --height 192 --minibatch_size 64 --optimizer Adam
Stop-Transcript

# Started on Donkey, 09.06.2017, 18:00
Start-Transcript -path "$($pathToTranscript)2017-06-09_vgg4_staff60-67-74-81_192x96_Adam.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 3 -offsets 60,67,74,81 --width 96 --height 192 --minibatch_size 64 --optimizer Adam
Stop-Transcript

# Started on Donkey, 09.06.2017, 18:00
Start-Transcript -path "$($pathToTranscript)2017-06-09_vgg_staff60-67-74-81_192x96_Adadelta.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 3 -offsets 60,67,74,81 --width 96 --height 192 --minibatch_size 64 --optimizer Adadelta
Stop-Transcript

# Started on Donkey, 09.06.2017, 18:00
Start-Transcript -path "$($pathToTranscript)2017-06-09_vgg4_staff60-67-74-81_192x96_Adadelta.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 3 -offsets 60,67,74,81 --width 96 --height 192 --minibatch_size 64 --optimizer Adadelta
Stop-Transcript

##### Smaller image-sizes, 1 staff-line

# Started on Monsti, 09.06.2017, 11:30
Start-Transcript -path "$($pathToTranscript)2017-06-09_vgg_staff74_192x96_Adadelta.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 3 -offsets 74 --width 96 --height 192 --minibatch_size 64 --optimizer Adadelta
Stop-Transcript

# Started on Monsti, 09.06.2017, 11:30
Start-Transcript -path "$($pathToTranscript)2017-06-09_vgg_staff74_192x96_Adam.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 3 -offsets 74 --width 96 --height 192 --minibatch_size 64 --optimizer Adadelta
Stop-Transcript

# Started on Donkey, 09.06.2017, 11:00
Start-Transcript -path "$($pathToTranscript)2017-06-09_vgg4_staff88_Adam.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 3 -offsets 88 --width 128 --height 224 --minibatch_size 64 --optimizer Adam
Stop-Transcript

# Started on Donkey, 09.06.2017, 11:00
Start-Transcript -path "$($pathToTranscript)2017-06-09_vgg4_staff88_Adadelta.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 3 -offsets 88 --width 128 --height 224 --minibatch_size 64 --optimizer Adadelta
Stop-Transcript

# Started on Donkey, 08.06.2017, 12:00
Start-Transcript -path "$($pathToTranscript)2017-06-08_vgg_staff60-67-74-81_192x96_no_lr_reduction.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 3 -offsets 60,67,74,81 --width 96 --height 192 --minibatch_size 64 --optimizer Adam --no_dynamic_learning_rate_reduction
Stop-Transcript

# Started on Donkey, 08.06.2017, 12:00
Start-Transcript -path "$($pathToTranscript)2017-06-08_vgg4_staff60-67-74-81_192x96_no_lr_reduction.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 3 -offsets 60,67,74,81 --width 96 --height 192 --minibatch_size 64 --optimizer Adam --no_dynamic_learning_rate_reduction
Stop-Transcript

# Started on Donkey, 08.06.2017, 12:00
Start-Transcript -path "$($pathToTranscript)2017-06-08_vgg_stroke2_staff74-81-88-95.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 2 -offsets 74,81,88,95 --width 128 --height 224 --minibatch_size 64 --optimizer Adadelta
Stop-Transcript

# Started on Donkey, 08.06.2017, 12:00
Start-Transcript -path "$($pathToTranscript)2017-06-08_vgg4_stroke2_staff74-81-88-95.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg4 -s 2 -offsets 74,81,88,95 --width 128 --height 224 --minibatch_size 64 --optimizer Adadelta
Stop-Transcript

##### Evaluating different optimizers on the same data, with/without LR-Reduction

# Started on Monsti, 08.06.2017, 12:48
Start-Transcript -path "$($pathToTranscript)2017-06-08_vgg_staff88_sgd.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 3 -offsets 88 --width 128 --height 224 --minibatch_size 16 --optimizer SGD
Stop-Transcript

# Started on Monsti, 08.06.2017, 12:48
Start-Transcript -path "$($pathToTranscript)2017-06-08_vgg_staff88_adadelta.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 3 -offsets 88 --width 128 --height 224 --minibatch_size 16 --optimizer Adadelta
Stop-Transcript

# Started on Monsti, 08.06.2017, 12:48
Start-Transcript -path "$($pathToTranscript)2017-06-08_vgg_staff88_adadelta_no_lr_reduction.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 3 -offsets 88 --width 128 --height 224 --minibatch_size 16 --optimizer Adadelta --no_dynamic_learning_rate_reduction
Stop-Transcript

# Started on Monsti, 08.06.2017, 12:48
Start-Transcript -path "$($pathToTranscript)2017-06-08_vgg_staff88_adam.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 3 -offsets 88 --width 128 --height 224 --minibatch_size 16 --optimizer Adam
Stop-Transcript

# Started on Monsti, 08.06.2017, 12:48
Start-Transcript -path "$($pathToTranscript)2017-06-08_vgg_staff88_adam_no_lr_reduction.txt" -append
python C:/Users/Alex/Repositories/MusicSymbolClassifier/ModelTrainer/TrainModel.py --model_name vgg -s 3 -offsets 88 --width 128 --height 224 --minibatch_size 16 --optimizer Adam --no_dynamic_learning_rate_reduction
Stop-Transcript
