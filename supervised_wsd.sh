#!/usr/bin/env bash

model=$1
cuda=$2
lg=$3

if [ $cuda -lt 0 ]
then
cuda_flag=0
else
cuda_flag=1
fi

for dict in ../../training/data/$model_100000_cluster_wsd0_cwn_trans_wsd.clustered.0.en.vec_dict_wps.mono.multiwsd_poly*
do
echo "CUDA_VISIBLE_DEVICES=$cuda python supervised.py --src_lang en --tgt_lang $lg --src_emb ../../training_data/$model_100000_cluster_wsd_random0_cwn_trans_wsd.clustered.0.en.vec.clean --tgt_emb ../../training_data/$model_100000_cluster_wsd_random0_cwn_trans_wsd.clustered.0.$lg.vec.clean --n_refinement 60 --emb_dim 768 --dico_train $dict --cuda $cuda_flag --dico_eval ./data/crosslingual/dictionaries/en-zh.txt.unsup &> supervised_clusterwsdrandom_$(basename $dict).log"

CUDA_VISIBLE_DEVICES=$cuda python supervised.py --src_lang en --tgt_lang $lg --src_emb ../../training_data/$model_100000_cluster_wsd_random0_cwn_trans_wsd.clustered.0.en.vec.clean --tgt_emb ../../training_data/$model_100000_cluster_wsd_random0_cwn_trans_wsd.clustered.0.$lg.vec.clean --n_refinement 60 --emb_dim 768 --dico_train $dict --cuda $cuda_flag --dico_eval ./data/crosslingual/dictionaries/en-zh.txt.unsup &> supervised_clusterwsdrandom_$(basename $dict).log
echo "CUDA_VISIBLE_DEVICES=$cuda python supervised.py --src_lang en --tgt_lang $lg --src_emb ../../training_data/$model_100000_cluster_wsd0_cwn_trans_wsd.clustered.0.en.vec.clean --tgt_emb ../../training_data/$model_100000_cluster_wsd0_cwn_trans_wsd.clustered.0.$lg.vec.clean --n_refinement 60 --emb_dim 768 --dico_train $dict --cuda $cuda_flag --dico_eval ./data/crosslingual/dictionaries/en-zh.txt.unsup &> supervised_clusterwsd_$(basename $dict).log"
CUDA_VISIBLE_DEVICES=$cuda python supervised.py --src_lang en --tgt_lang $lg --src_emb ../../training_data/$model_100000_cluster_wsd0_cwn_trans_wsd.clustered.0.en.vec.clean --tgt_emb ../../training_data/$model_100000_cluster_wsd0_cwn_trans_wsd.clustered.0.$lg.vec.clean --n_refinement 60 --emb_dim 768 --dico_train $dict --cuda $cuda_flag --dico_eval ./data/crosslingual/dictionaries/en-zh.txt.unsup &> supervised_clusterwsd_$(basename $dict).log

done
