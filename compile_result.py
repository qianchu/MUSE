from collections import defaultdict

def extract_res(fname):
    results=defaultdict(lambda: defaultdict(float))
    with open(fname) as f:
        for line in f:

            if 'Precision at k' in line:
                line=line.strip()
                metric,precision=line.split(' - ')[4:]
                topn,score=precision.split(' = ')[1].split(': ')
                topn=int(topn)
                score=float(score)
                if score> results[metric][topn]:
                    results[metric][topn]=score
    return results

def print_result(results):

    for key in results:
        print (key)
        metric2avgscore=defaultdict(lambda: defaultdict(list))
        for result in results[key]:
            for metric in result:
                for topn in result[metric]:
                    metric2avgscore[metric][topn].append(float(result[metric][topn]))
        for metric in metric2avgscore:
            for topn in metric2avgscore[metric]:
                score=sum(metric2avgscore[metric][topn])/len(metric2avgscore[metric][topn])
                print ('metric', 'topn','avg_score')
                print (metric,topn, score)

if __name__=='__main__':
    import argparse
    import os
    parser = argparse.ArgumentParser(description='compile results for semisupervised alignment from seed dictionary')
    parser.add_argument("--dir", type=str, help="")
    args=parser.parse_args()
    results=defaultdict(list)
    for root, dirs, files in os.walk(args.dir, topdown=False):
        for name in files:

            if name.startswith('supervised_clusterwsd') and '100000_cluster_wsd0_cwn_trans_wsd.clustered.0.en.vec' in name:
                result = extract_res(os.path.join(root, name))
                name = name.rstrip('.log')
                fields=name.split('_')
                cluster_flag=fields[1]
                model='_'.join(fields[2:fields.index('100000')])
                iteration=fields[-1]
                dict_size=fields[-2]
                poly_degree=fields[-3]


                results[(cluster_flag,model,dict_size,poly_degree)].append(result)

    print_result(results)

