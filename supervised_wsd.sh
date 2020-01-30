#!/usr/bin/env bash

model=$1
cuda=$2
lg=$3


for dict in ../../training/data/$model_100000_cluster_wsd0_cwn_trans_wsd.clustered.0.en.vec_dict_wps.mono.multiwsd_poly*
do
CUDA_VISIBLE_DEVICES=$cuda python supervised.py --src_lang en --tgt_lang $lg --src_emb ../../training_data/$model_100000_cluster_wsd_random0_cwn_trans_wsd.clustered.0.en.vec.clean --tgt_emb ../../training_data/$model_100000_cluster_wsd_random0_cwn_trans_wsd.clustered.0.$lg.vec.clean --n_refinement 60 --emb_dim 768 --dico_train $dict --cuda 1 --dico_eval ./data/crosslingual/dictionaries/en-zh.txt.unsup &> supervised_clusterwsdrandom_$(basename $dict).log
CUDA_VISIBLE_DEVICES=$cuda python supervised.py --src_lang en --tgt_lang $lg --src_emb ../../training_data/$model_100000_cluster_wsd0_cwn_trans_wsd.clustered.0.en.vec.clean --tgt_emb ../../training_data/$model_100000_cluster_wsd0_cwn_trans_wsd.clustered.0.$lg.vec.clean --n_refinement 60 --emb_dim 768 --dico_train $dict --cuda 1 --dico_eval ./data/crosslingual/dictionaries/en-zh.txt.unsup &> supervised_clusterwsd_$(basename $dict).log

done
