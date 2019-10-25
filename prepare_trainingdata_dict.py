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


if __name__=='__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Supervised training')
    parser.add_argument("--emb_en", type=str, help="emb en")
    parser.add_argument("--emb_zh", type=str, help="emb zh")
    parser.add_argument("--en2zh_dict", type=str, default='', help="en2zh dictionary")
    args=parser.parse_args()
    # with open(parser.en2zh_dict,'r') as dict:
    #     for line in dict:
    #         en,zh=line.strip().split()
    #         if en in

    en_dict=process_f(args.emb_en)
    zh_dict=process_f(args.emb_zh)

    if args.en2zh_dict:

        with open(parser.en2zh_dict,'r') as dict_in, open(parser.en2zh_dict+'.unsup', 'w') as dict_out:
            for line in dict_in:
                en,zh=line.strip().split()
                if en in en_dict and zh in zh_dict:
                    dict_out.write(line)

