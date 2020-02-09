from collections import defaultdict
from copy import deepcopy
from random import sample
def process_f(emb):
    w_dict=defaultdict(int)
    counter = 0
    with open(emb,'r') as emb_f, open(emb+'.clean','w') as emb_f_out:
        for line in emb_f:
            line_new=line
            if counter>0:
                w=line.split(' ')[0]
                w_dict[w]+=1
                if w_dict[w] !=1:
                    line_new=line.split(' ')
                    line_new[0]=w+'.'+str(w_dict[w])
                    line_new=' '.join(line_new)
            counter+=1
            emb_f_out.write(line_new)
    return w_dict

def update_wps_multisense_nowsd_select(wps_multisense_nowsd_select,wps_multisense_nowsd,en2zh_multisense,zh2en_multisense,i):
            wps_multisense_nowsd_select.append(i)
            wp = wps_multisense_nowsd[i]
            add=[]
            if wp[0] in en2zh_multisense:
                add_en=[i for i in en2zh_multisense[wp[0]] if i not in wps_multisense_nowsd_select]
                add+=add_en
            if wp[1] in zh2en_multisense:
                add_zh = [i for i in zh2en_multisense[wp[0]] if i not in wps_multisense_nowsd_select]
                add+=add_zh
            add=list(set(add))
            for add_i in add:
                update_wps_multisense_nowsd_select(wps_multisense_nowsd_select, wps_multisense_nowsd, en2zh_multisense,
                                                   zh2en_multisense, add_i)

def wsd_dict_produce(emb_en,emb_zh,dict_test,dict_size,poly_percent):
    wps_multisense_nowsd=[]
    wps_multisense_wsd=[]
    wps_monosense=[]

    dict_test_lst = {}
    with open(dict_test) as f:
        for line in f:
            en, zh = line.split()
            dict_test_lst[(en, zh)] = 1

    en_vocab=[line.split(' ')[0] for line in open(emb_en,'r')]
    zh_vocab=[line.split(' ')[0] for line in open(emb_zh,'r')]
    en2zh_multisense=defaultdict(list)
    zh2en_multisense=defaultdict(list)
    en_zh=list(zip(en_vocab,zh_vocab))
    wps_multisense_counter=0
    for wp in en_zh:
        en=wp[0]
        zh=wp[1]
        if '.' in en or '.' in zh:
            wps_multisense_wsd.append((en, zh))
            en_w=en
            zh_w=zh
            if '.' in en:
                en_w=en.split('.')[0]
                en2zh_multisense[en_w].append(wps_multisense_counter)
            if '.' in zh:
                zh_w=zh.split('.')[0]
                zh2en_multisense[zh_w].append(wps_multisense_counter)
            wps_multisense_counter+=1

            wps_multisense_nowsd.append((en_w,zh_w))
        else:
            if (en,zh) not in dict_test_lst:
                wps_monosense.append((en,zh))


    wps_all_wsd=wps_multisense_wsd+wps_monosense
    wps_all_nowsd=wps_monosense+wps_multisense_nowsd
    assert len(wps_all_wsd)==len(wps_all_nowsd)
    assert len(wps_multisense_wsd) == len(wps_multisense_nowsd)
    # dictionary=list(set(en2zh_wps+zh2en_wps))
    for i in range(5):

        wp_all_wsd_sample=sample(list(range(len(wps_all_wsd))),dict_size)
        wp_all_nowsd_sample=wp_all_wsd_sample
        wp_multisense_wsd_sample=sample(list(range(len(wps_multisense_wsd))),dict_size)
        wp_multisense_nowsd_sample=wp_multisense_wsd_sample
        wp_monosense_sample=sample(list(range(len(wps_monosense))),dict_size)



        with open('{0}_dict_wps.all.wsd_{1}_{2}'.format(emb_en,str(dict_size),str(i)),'w') as f:
            for entry in [wps_all_wsd[i] for i in wp_all_wsd_sample]:
                f.write('\t'.join(entry)+'\n')

        with open('{0}_dict_wps.all.nowsd_{1}_{2}'.format(emb_en,str(dict_size),str(i)),'w') as f:
            for entry in [wps_all_nowsd[i] for i in wp_all_nowsd_sample]:
                f.write('\t'.join(entry) + '\n')

        # with open('{0}.dict.wps_monosense.{1}.{2}'.format(emb_en,str(dict_size),str(i)),'w') as f:
        #     for entry in [wps_monosense[i] for i in wp_monosense_sample]:
        #         f.write('\t'.join(entry) + '\n')
        #
        # with open('{0}.dict.all_{1}_{2}'.format(emb_en, str(dict_size), str(i)), 'w') as f:
        #     for entry in [wps_all[i] for i in wp_all_sample]:
        #         f.write('\t'.join(entry) + '\n')

        wps_multisense_nowsd_select=[]

        for sample_i in wp_multisense_nowsd_sample:
            wps_multisense_nowsd_select_prev=deepcopy(wps_multisense_nowsd_select)
            print (sample_i,len(wps_multisense_nowsd_select))
            update_wps_multisense_nowsd_select(wps_multisense_nowsd_select, wps_multisense_nowsd, en2zh_multisense,
                                               zh2en_multisense, sample_i)
            if len(wps_multisense_nowsd_select)>int(dict_size*poly_percent):
                wps_multisense_nowsd_select=wps_multisense_nowsd_select_prev
                break
        wps_multisense_wsd_select=wps_multisense_nowsd_select

        monosense_len=int(dict_size)-len(wps_multisense_wsd_select)
        if monosense_len<0:
            monosense_len=0

        print ('poly: ', len(wps_multisense_wsd_select), 'mono:', monosense_len)
        with open('{0}_dict_wps.mono.multiwsd_poly{3}_{1}_{2}'.format(emb_en, str(dict_size), str(i),str(poly_percent)), 'w') as f:
            for entry in [wps_multisense_wsd[i] for i in wps_multisense_wsd_select]+[wps_monosense[i] for i in wp_monosense_sample[:monosense_len]]:
                f.write('\t'.join(entry) + '\n')

        with open('{0}_dict_wps.mono.multinowsd_poly{3}_{1}_{2}'.format(emb_en, str(dict_size), str(i),
                                                                          str(poly_percent)), 'w') as f:
            for entry in [wps_multisense_wsd[i] for i in wps_multisense_nowsd_select] + [wps_monosense[i] for i in
                                                                                       wp_monosense_sample[:monosense_len]]:
                f.write('\t'.join(entry) + '\n')





def dict_produce(emb_en,emb_zh):
    en2zh=defaultdict(list)
    zh2en=defaultdict(list)
    en_vocab=[line.split(' ')[0] for line in open(emb_en,'r')]
    zh_vocab=[line.split(' ')[0] for line in open(emb_zh,'r')]
    en_zh=list(zip(en_vocab,zh_vocab))
    for wp in en_zh:
        en=wp[0]
        zh=wp[1]
        en_w=en
        zh_w=zh
        if '.' in en:
            en_w=en.split('.')[0]
            zh_w=en.split('.')[1]

        if '.' in zh:
            en_w = zh.split('.')[1]
            zh_w = zh.split('.')[0]

        zh2en[zh_w].append((en_w,zh_w))
        en2zh[en_w].append((en_w,zh_w))


    remove_extra_wa(zh2en,en2zh)
    remove_extra_wa(en2zh,zh2en)

    en2zh_wps=[wp for w in en2zh for wp in en2zh[w]]
    zh2en_wps=[wp for w in zh2en for wp in zh2en[w]]

    dictionary=list(set(en2zh_wps+zh2en_wps))
    with open(emb_en+'.dict','w') as f:
        for entry in dictionary:
            f.write('\t'.join(entry)+'\n')
    return en2zh, zh2en


def remove_extra_wa(zh2en,en2zh):
    for zh_w in zh2en:
        if len(zh2en[zh_w])>1:
            found=False
            wp_list=deepcopy(zh2en[zh_w])
            for wp in wp_list:
                en_w=wp[1-wp.index(zh_w)]

                if found:
                    # en_w=zh2en[zh_w][0]
                    # zh_w=zh2en[zh_w][1]
                    zh2en[zh_w].remove(wp)
                    if wp in en2zh[en_w]:
                        en2zh[en_w].remove(wp)
                    continue
                found=True

def dict_filter(dict_f,emb_en,emb_zh):
    dict_list={}
    with open(dict_f,'r') as f:
        for line in f:
            wp=line.strip().split('\t')
            dict_list['.'.join(wp)]=True
            dict_list['.'.join([wp[1],wp[0]])]=True
            dict_list[wp[0]]=True
            dict_list[wp[1]]=True


    with open(emb_en,'r') as emb_en_f, open(emb_zh,'r') as emb_zh_f, open(emb_en+'.filtered','w') as emb_en_out, open(emb_zh+'.filtered','w') as emb_zh_out:
        for line in emb_en_f:
            en_w=line.split(' ')[0]
            if en_w in dict_list:
                emb_en_out.write(line)
        for line in emb_zh_f:
            zh_w=line.split(' ')[0]
            if zh_w in dict_list:
                emb_zh_out.write(line)




if __name__=='__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Supervised training')
    parser.add_argument("--emb_en", type=str, help="emb en")
    parser.add_argument("--emb_zh", type=str, help="emb zh")
    parser.add_argument("--en2zh_dict", type=str, default='', help="en2zh dictionary")
    parser.add_argument('--dict_produce', action='store_true', help='produce dictionary to one-to-one mapping')
    parser.add_argument('--dict_filter', type=str, default='', help='filter dictionary to one-to-one mapping')
    parser.add_argument('--dict_wsd_produce', action='store_true',help='produce wsd dictionary')
    parser.add_argument('--dict_test', type=str, help='test dictionary file to be excluded from training data')
    parser.add_argument('--dict_size',type=int, help='dictionary size')
    parser.add_argument('--poly_percent',type=float, help='percentage of ambiguous words')

    args=parser.parse_args()
    # with open(parser.en2zh_dict,'r') as dict:
    #     for line in dict:
    #         en,zh=line.strip().split()
    #         if en in

    en_dict=process_f(args.emb_en)
    zh_dict=process_f(args.emb_zh)

    if args.dict_wsd_produce:
        wsd_dict_produce(args.emb_en,args.emb_zh,args.dict_test,args.dict_size,args.poly_percent)
    if args.dict_produce:
        dict_produce(args.emb_en,args.emb_zh)

    if args.dict_filter:
        dict_filter(args.dict_filter,args.emb_en,args.emb_zh)
    if args.en2zh_dict:

        with open(args.en2zh_dict,'r') as dict_in, open(args.en2zh_dict+'.unsup', 'w') as dict_out:
            for line in dict_in:
                en,zh=line.strip().split()
                if en in en_dict and zh in zh_dict:
                    dict_out.write(line)

