from collections import defaultdict

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

    dictionary=list(set(list(en2zh.values())+list(zh2en.values())))
    with open(emb_en+'.dict','w') as f:
        for entry in dictionary:
            f.write('\t'.join(entry))
    return en2zh, zh2en


def remove_extra_wa(zh2en,en2zh):
    for zh_w in zh2en:
        if len(zh2en[zh_w])>1:
            found=False
            for wp in zh2en[zh_w]:
                if found:
                    en_w=zh2en[zh_w][0]
                    zh_w=zh2en[zh_w][1]
                    zh2en[zh_w].remove(wp)
                    if wp in en2zh[en_w]:
                        en2zh[en_w].remove(wp)
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


    with open(emb_en,'r') as emb_en, open(emb_zh,'r') as emb_zh, open(emb_en+'.filtered','w') as emb_en_out, open(emb_zh+'.filtered','w') as emb_zh_out:
        for line in emb_en:
            en_w=line.split(' ')[0]
            if en_w in dict_list:
                emb_en_out.write(line)
        for line in emb_zh:
            zh_w=line.split(' ')[0]
            if zh_w in dict_list:
                emb_zh_out.write(line)




if __name__=='__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Supervised training')
    parser.add_argument("--emb_en", type=str, help="emb en")
    parser.add_argument("--emb_zh", type=str, help="emb zh")
    parser.add_argument("--en2zh_dict", type=str, default='', help="en2zh dictionary")
    parser.add_argument('--dict_produce', type=bool, default=False, help='produce dictionary to one-to-one mapping')
    parser.add_argument('--dict_filter', type=str, default='', help='filter dictionary to one-to-one mapping')

    args=parser.parse_args()
    # with open(parser.en2zh_dict,'r') as dict:
    #     for line in dict:
    #         en,zh=line.strip().split()
    #         if en in

    en_dict=process_f(args.emb_en)
    zh_dict=process_f(args.emb_zh)

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
