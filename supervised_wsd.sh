#!/usr/bin/env bash

model=$1
cuda=$2
lg=$3
dict_sizes=$4
cluster_flags=$5
dim=$6
dico_multi=${7:-""}

#IFS=' ' # space is set as delimiter
#read -ra cluster_flags <<< "$cluster_flags"
#read -ra dict_sizes <<< "$dict_sizes"

if [ $cuda -lt 0 ]
then
cuda_flag=0
else
cuda_flag=1
fi


#declare -a cluster_flags=(cluster_flags)

for cluster_flag in $cluster_flags
do

    if [ "$cluster_flag" == "clusterall" ]
    then
    dict_flag='nowsd'
    else
    dict_flag='wsd'
    fi
    for dict_size in $dict_sizes
    do
        for dict in ../../training_data/${model}_100000_cluster_wsd0_cwn_trans_wsd.clustered.0.en.vec_dict_wps.mono.multi${dict_flag}_poly*_${dict_size}_*
        do


        echo "        CUDA_VISIBLE_DEVICES=$cuda python supervised.py --src_lang en --tgt_lang $lg --src_emb ../../training_data/${model}_100000_${cluster_flag}0_cwn_trans_wsd.clustered.0.en.vec.clean --tgt_emb ../../training_data/${model}_100000_${cluster_flag}0_cwn_trans_wsd.clustered.0.$lg.vec.clean --n_refinement 60 --emb_dim $dim --dico_train $dict --cuda $cuda_flag --dico_eval ./data/crosslingual/dictionaries/en-zh.txt.unsup $dico_multi &> supervised_${cluster_flag}_$(basename $dict)${dico_multi}.log"
        CUDA_VISIBLE_DEVICES=$cuda python supervised.py --src_lang en --tgt_lang $lg --src_emb ../../training_data/${model}_100000_${cluster_flag}0_cwn_trans_wsd.clustered.0.en.vec.clean --tgt_emb ../../training_data/${model}_100000_${cluster_flag}0_cwn_trans_wsd.clustered.0.$lg.vec.clean --n_refinement 60 --emb_dim $dim --dico_train $dict --cuda $cuda_flag --dico_eval ./data/crosslingual/dictionaries/en-zh.txt.unsup $dico_multi &> supervised_${cluster_flag}_$(basename $dict)${dico_multi}.log

        done
    done

done
