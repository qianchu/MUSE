

if __name__ == '__main__':
    import argparse
    import os
    args = argparse.ArgumentParser('vocab compile')
    args.add_argument('--en2zh', type=str,help='en2zh vocab file')
    args.add_argument('--zh2en', type=str,help='zh2en vocab file')
    args.add_argument('--outputpre', type=str, help='en2zh file')
    args=args.parse_args()

    output_fname=os.path.join(os.path.dirname(args.en2zh),'en_zh_{0}'.format(args.outputpre))
    output_en_fname=os.path.join(os.path.dirname(args.en2zh),'en_{0}'.format(args.outputpre))
    output_zh_fname=os.path.join(os.path.dirname(args.en2zh),'zh_{0}'.format(args.outputpre))
    output_align_fname=os.path.join(os.path.dirname(args.en2zh),'en_zh_{0}.align'.format(args.outputpre))

    # en2zh_all_set=[]
    en2zh_lst= open(args.en2zh).readlines()
    zh2en_lst=['{0} {1}\n'.format(line.split()[1],line.split()[0]) for line in open(args.zh2en).readlines()]
    en2zh_all_set=list(set(en2zh_lst+zh2en_lst))
    en_lst,zh_lst=zip(*[(line.split()[0]+'\n',line.split()[1]+'\n') for line in list(set(en2zh_lst+zh2en_lst))])
    print (en2zh_all_set)
    print (len(en2zh_all_set))
    with open(output_fname,'w') as f:
        f.writelines(en2zh_all_set)
    with open(output_en_fname,'w') as f:
        f.writelines(en_lst)
    with open(output_zh_fname,'w') as f:
        f.writelines(zh_lst)
    with open(output_align_fname,'w') as f:
        f.writelines(['0-0\n']*len(en2zh_all_set))

    #     en2zh_gen=file2generator(args.en2zh)
    #     zh2en_gen=file2generator(args.zh2en)
    #     for line in en2zh_gen:
    #         if line not in en2zh_all_set:
    #             f.write(line)


