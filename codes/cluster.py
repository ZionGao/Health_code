# -*- coding: utf-8 -*-
import os
import argparse
import pickle
from collections import defaultdict
import pandas as pd
from tqdm import tqdm
import json
from utils.similar import jaccard
from utils.segmentor import Segmentor
from utils.utils import check_file, ensure_dir, clean_dir, sample_file, get_stop_words, line_counter, Range


class Text_Cluster:
    def __init__(self):
        pass

    def _get_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--infile', type=str, default='./data/infile', help='Directory of input file.')
        parser.add_argument('--output', type=str, default='./data/output', help='Directory to save output file.')
        parser.add_argument('--dict', type=str, default='./data/seg_dict', help='Directory of dict file.')
        parser.add_argument('--stop_words', type=str, default='./data/stop_words', help='Directory of stop words.')
        parser.add_argument('--sample_number', type=int, default=5, choices=[Range(1)], help='Sample number for each bucket.')
        parser.add_argument('--threshold', type=float, default=0.3, choices=[Range(0.0, 1.0)], help='Threshold for matching.')
        parser.add_argument('--name_len', type=int, default=9, choices=[Range(2)], help='Filename length.')
        parser.add_argument('--name_len_update', type=bool, default=False, help='To update file name length.')
        parser.add_argument('--lang', type=str, choices=['cn', 'en'], default='cn', help='Segmentor language setting.')
        args = parser.parse_args()
        return args


    def run(self, questions):
        args = self._get_parser()

        # preliminary work
        ensure_dir(args.output)

        if args.name_len_update:
            line_cnt = line_counter(args.infile)
            args.name_len = len(str(line_cnt)) + 1

        clean_dir(args.output, args.name_len)
        # end preliminary work

        p_bucket = defaultdict(list)
        save_idx = 0
        id_name = '{0:0' + str(args.name_len) + 'd}'
        # load stop words
        stop_words = get_stop_words(args.stop_words) if os.path.exists(args.stop_words) else list()
        # load tokenizer
        seg = Segmentor(args)

        print('Splitting sentence into different clusters ...')
        infile = questions
        for inline in tqdm(infile):
            inline = inline.rstrip()
            line = inline.split(':::')[0]
            is_match = False
            seg_list = list(seg.cut(line))
            if stop_words:
                seg_list = list(filter(lambda x: x not in stop_words, seg_list))
            for wd in seg_list:
                if is_match:
                    break
                w_bucket = p_bucket[wd]
                for bucket in w_bucket:
                    bucket_path = os.path.join(args.output, bucket)
                    check_file(bucket_path)
                    selected = sample_file(bucket_path, args.sample_number)
                    selected = list(map(lambda x: x.split(':::')[0], selected))
                    selected = list(map(lambda x: list(seg.cut(x)), selected))
                    # remove stop words
                    if stop_words:
                        filt_selected = list()
                        for sen in selected:
                            sen = list(filter(lambda x: x not in stop_words, sen))
                            filt_selected.append(sen)
                        selected = filt_selected
                    # calculate similarity with each bucket
                    if all(jaccard(seg_list, cmp_list) > args.threshold for cmp_list in selected):
                        is_match = True
                        with open(bucket_path, 'a', encoding='utf-8') as outfile:
                            outfile.write(line+'\n')
                        for w in seg_list:
                            if bucket not in p_bucket[w]:
                                p_bucket[w].append(bucket)
                        break
            if not is_match:
                bucket_name = ('tmp' + id_name).format(save_idx)
                bucket_path = os.path.join(args.output, bucket_name)
                with open(bucket_path, 'a', encoding='utf-8') as outfile:
                    outfile.write(line+'\n')
                for w in seg_list:
                    p_bucket[w].append(bucket_name)
                save_idx += 1

        # sort and rename file
        file_list = os.listdir(args.output)
        file_list = list(filter(lambda x: x.startswith('tmp'), file_list))
        cnt = dict()
        for file in file_list:
            file_path = os.path.join(args.output, file)
            cnt[file] = line_counter(file_path)

        sorted_cnt = sorted(cnt.items(), key=lambda kv: kv[1], reverse=True)
        name_map = dict()
        for idx, (file_name, times) in enumerate(sorted_cnt):
            origin_path = os.path.join(args.output, file_name)
            new_name = id_name.format(idx)
            new_path = os.path.join(args.output, new_name)
            os.rename(origin_path, new_path)
            name_map[file_name] = new_name

        for k, v in p_bucket.items():
            p_bucket[k] = list(map(lambda x: name_map[x], v))

        #合并文件
        output_file = os.path.join(args.output,'all_cluster.txt')
        try:
            if os.path.isfile(output_file):
                os.unlink(output_file)
        except Exception as e:
            print(e)
        file_list = os.listdir(args.output)
        fw = open(output_file, 'w+')
        for file in file_list:
            with open(os.path.join(args.output, file)) as f:
                for line in f.readlines():
                    fw.write(str(int(file)) + ',' +line)
        fw.close()
        df = pd.read_csv(output_file, names=['id', 'text'])
        df.columns = ['cluster_id', 'ques']
        print('All is well')
        # json.dumps(dict(ques=ques))
        df_dict = df.set_index('cluster_id').T.to_dict('records')[0]

        #dataframe 的数据格式转换
        #df 0 aa
        #   0 aaa                   => aa  [aaa]
        #   1 bb                       bb  []
        #df_dict = {0: aa, 1: bb}
        print(df_dict)
        result_dict = {}
        for cluster_id, ques in df_dict.items():
            li = df[df['cluster_id']==cluster_id].ques.values.tolist()
            # if(ques in li): li.remove(ques)
            result_dict[ques] = li

        my_list = [result_dict]
        my_df = pd.DataFrame(my_list).T
        my_df = my_df.reset_index()
        my_df.columns = ['ques', 'info']
        print(my_df)
        return my_df.to_json(orient="records",force_ascii=False)


if __name__ == '__main__':
    cluster = Text_Cluster()
    result = cluster.run(["我是海贼王的男人","我是海贼王的女人","我是海贼王","教练，我想打球"])
    print(result)


