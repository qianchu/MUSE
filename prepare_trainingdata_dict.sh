#!/usr/bin/env bash

en_emb=$1
zh_emb=$2
test_dict=$3
dict_sizes=$4
polys=$5

for dict_size in $dict_sizes
do
for poly in $polys
do
echo "python prepare_trainingdata_dict.py --emb_en .$en_emb --emb_zh $zh_emb --dict_wsd_produce --dict_size $dict_size --poly_percent $poly --dict_test $test_dict"
python prepare_trainingdata_dict.py --emb_en $en_emb --emb_zh $zh_emb --dict_wsd_produce --dict_size $dict_size --poly_percent $poly --dict_test $test_dict
done
done
