#coding=utf8
"""
This code referenced from [here](https://github.com/PaddlePaddle/models/blob/develop/deep_fm/preprocess.py)
-For numerical features, normalzied to continous values.
-For categorical features, removed long-tailed data appearing less than 200 times.

TODO：
#1 连续特征 离散化
#2 Nagetive down sampling
"""
import os
import sys
import gzip
#import click
import random
import collections
import argparse
from multiprocessing import Pool as ThreadPool

# 0 is id, 1 is target, [2, 23] is categorical features
categorial_features = range(2, 24) 


class CategoryDictGenerator:
    """
    Generate dictionary for each of the categorical features
    """

    def __init__(self, num_feature):
        self.dicts = []
        self.num_feature = num_feature
        for i in range(0, num_feature):
            self.dicts.append(collections.defaultdict(int))

    def build(self, datafile, categorial_features, cutoff=0):
        print('CategoryDictGenerator.build')
        with gzip.open(datafile) as f:
            header = f.readline()
            print('header =', header)
            # line_count = 0
            for line in f:
                # line_count = line_count + 1
                features = line.strip().decode().split(",")
                sys.stdout.write('\r>> id = %s' % (features[0]))
                sys.stdout.flush()
                for i in range(0, self.num_feature):
                    if features[categorial_features[i]] != '':
                        self.dicts[i][features[categorial_features[i]]] += 1
                # if line_count > 2000:
                    # break
        sys.stdout.write('\n')
        sys.stdout.flush()
        for i in range(0, self.num_feature):
            self.dicts[i] = filter(lambda x: x[1] >= cutoff, self.dicts[i].items())
            self.dicts[i] = sorted(self.dicts[i], key=lambda x: (-x[1], x[0]))
            vocabs, _ = list(zip(*self.dicts[i]))
            self.dicts[i] = dict(zip(vocabs, range(1, len(vocabs) + 1)))
            self.dicts[i]['<unk>'] = 0

    def gen(self, idx, key):
        if key not in self.dicts[idx]:
            res = self.dicts[idx]['<unk>']
        else:
            res = self.dicts[idx][key]
        return res

    def dicts_sizes(self):
        return list(map(len, self.dicts))


#@click.command("preprocess")
#@click.option("--datadir", type=str, help="Path to raw criteo dataset")
#@click.option("--outdir", type=str, help="Path to save the processed data")
def preprocess(datadir, outdir):
    """
    Each of the categorical features are one-hot encoded and all the one-hot
    vectors are combined into one sparse binary vector.
    """
    dicts = CategoryDictGenerator(len(categorial_features))
    dicts.build(FLAGS.input_dir + 'train.gz', categorial_features, cutoff=FLAGS.cutoff)
    
    output = open(FLAGS.output_dir + 'feature_map','w')
    
    dict_sizes = dicts.dicts_sizes()
    categorial_feature_offset = [0]
    for i in range(1, len(categorial_features)+1):
        # print('dict_sizes[i - 1]=', dict_sizes[i - 1])
        offset = categorial_feature_offset[i - 1] + dict_sizes[i - 1]
        categorial_feature_offset.append(offset)
        for key, val in dicts.dicts[i-1].items():
            output.write("{0} {1}\n".format('C'+str(i)+'|'+key, categorial_feature_offset[i - 1]+val+1))

    random.seed(0)

    print('preprocess.train')
    # 90% of the data are used for training, and 10% of the data are used for validation.
    with open(FLAGS.output_dir + 'tr.libsvm', 'w') as out_train:
        with open(FLAGS.output_dir + 'va.libsvm', 'w') as out_valid:
            with gzip.open(FLAGS.input_dir + 'train.gz') as f:
                header = f.readline()
                print('header =', header)
                for line in f:
                    features = line.strip().decode().split(",")
                    feat_vals = []
                    
                    for i in range(0, len(categorial_features)):
                        val = dicts.gen(i, features[categorial_features[i]]) + categorial_feature_offset[i]
                        # print('val =', val)
                        feat_vals.append(str(val) + ':1')

                    id = features[0]
                    sys.stdout.write('\r>> id = %s' % (id))
                    sys.stdout.flush()
                    label = features[1]
                    out_line = "{0} {1} {2}\n".format(id, label, ' '.join(feat_vals))
                    # print('out_line =', out_line)
                    if random.randint(0, 9999) % 10 != 0:
                        out_train.write(out_line)
                    else:
                        out_valid.write(out_line)
                    # break
    sys.stdout.write('\n')
    sys.stdout.flush()
    
    print('preprocess.test')
    with open(FLAGS.output_dir + 'te.libsvm', 'w') as out:
        with gzip.open(FLAGS.input_dir + 'test.gz') as f:
            header = f.readline()
            print('header =', header)
            for line in f:
                features = line.strip().decode().split(",")
                feat_vals = []

                for i in range(0, len(categorial_features)):
                    # in test, 0 is id, [1, 22] is categorical features
                    val = dicts.gen(i, features[categorial_features[i] - 1]) + categorial_feature_offset[i]
                    # print('val =', val)
                    feat_vals.append(str(val) + ':1')
                
                id = features[0]
                sys.stdout.write('\r>> id = %s' % (id))
                sys.stdout.flush()
                out_line = "{0} {1} {2}\n".format(id, label, ' '.join(feat_vals))
                # print('out_line =', out_line)
                out.write(out_line)
                # break
    sys.stdout.write('\n')
    sys.stdout.flush()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--threads",
        type=int,
        default=2,
        help="threads num"
        )
    parser.add_argument(
        "--input_dir",
        type=str,
        default="",
        help="input data dir"
        )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="",
        help="feature map output dir"
        )
    parser.add_argument(
        "--cutoff",
        type=int,
        default=200,
        help="cutoff long-tailed categorical values"
        )

    FLAGS, unparsed = parser.parse_known_args()
    print('threads ', FLAGS.threads)
    print('input_dir ', FLAGS.input_dir)
    print('output_dir ', FLAGS.output_dir)
    print('cutoff ', FLAGS.cutoff)

    preprocess(FLAGS.input_dir, FLAGS.output_dir)
