#!/usr/bin/env bash

model=$1
cuda=$2
lg=$3
dict_size=$4
cluster_flags=$5


if [ $cuda -lt 0 ]
then
cuda_flag=0
else
cuda_flag=1
fi

#declare -a cluster_flags=(cluster_flags)


for dict in ../../training_data/${model}_100000_cluster_wsd0_cwn_trans_wsd.clustered.0.en.vec_dict_wps.mono.multiwsd_poly*_${dict_size}_*
do

for cluster_flag in "$cluster_flags"
do
echo "CUDA_VISIBLE_DEVICES=$cuda python supervised.py --src_lang en --tgt_lang $lg --src_emb ../../training_data/${model}_100000_${cluster_flag}0_cwn_trans_wsd.clustered.0.en.vec.clean --tgt_emb ../../training_data/${model}_100000_${cluster_flag}0_cwn_trans_wsd.clustered.0.$lg.vec.clean --n_refinement 60 --emb_dim 768 --dico_train $dict --cuda $cuda_flag --dico_eval ./data/crosslingual/dictionaries/en-zh.txt.unsup &> supervised_${cluster_flag}_$(basename $dict).log"
CUDA_VISIBLE_DEVICES=$cuda python supervised.py --src_lang en --tgt_lang $lg --src_emb ../../training_data/${model}_100000_${cluster_flag}0_cwn_trans_wsd.clustered.0.en.vec.clean --tgt_emb ../../training_data/${model}_100000_${cluster_flag}0_cwn_trans_wsd.clustered.0.$lg.vec.clean --n_refinement 60 --emb_dim 768 --dico_train $dict --cuda $cuda_flag --dico_eval ./data/crosslingual/dictionaries/en-zh.txt.unsup &> supervised_${cluster_flag}_$(basename $dict).log

done

done
