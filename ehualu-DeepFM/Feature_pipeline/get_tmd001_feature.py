#coding=utf8
"""
This code referenced from [here](https://github.com/PaddlePaddle/models/blob/develop/deep_fm/preprocess.py)
-For numerical features,normalzied to continous values.
-For categorical features, removed long-tailed data appearing less than 200 times.

TODO：
#1 连续特征 离散化
#2 Nagetive down sampling
"""
import os
import sys
#import click
import random
import collections
import argparse
from multiprocessing import Pool as ThreadPool

# There are 13 integer features and 26 categorical features
continous_features = range(2, 102) # 0 is filename, 1 is target, [1, 14)
# categorial_features = range(14, 40)

# Clip integer features. The clip point for each integer feature
# is derived from the 95% quantile of the total values in each feature
# continous_clip = [100, 600, 100, 50, 64000, 500, 100, 50, 500, 10, 10, 10, 50]


class ContinuousFeatureGenerator:
    """
    Normalize the integer features to [0, 1] by min-max normalization
    """

    def __init__(self, num_feature):
        self.num_feature = num_feature
        self.min = [sys.maxsize] * num_feature
        self.max = [-sys.maxsize] * num_feature

    def build(self, datafile, continous_features):
        with open(datafile, 'r') as f:
            head = f.readline()
            print('ContinuousFeatureGenerator head=',head)
            for line in f:
                features = line.rstrip('\n').split(',')
                # print('features=',features)
                for i in range(0, self.num_feature):
                    val = features[continous_features[i]]
                    if val != '':
                        val = float(val)
                        self.min[i] = min(self.min[i], val)
                        self.max[i] = max(self.max[i], val)

    def gen(self, idx, val):
        if val == '':
            return 0.0
        val = float(val)
        return (val - self.min[idx]) / (self.max[idx] - self.min[idx])


#@click.command("preprocess")
#@click.option("--datadir", type=str, help="Path to raw criteo dataset")
#@click.option("--outdir", type=str, help="Path to save the processed data")
def preprocess(datadir, outdir):
    """
    All the 13 integer features are normalzied to continous values and these
    continous features are combined into one vecotr with dimension 13.
    Each of the 26 categorical features are one-hot encoded and all the one-hot
    vectors are combined into one sparse binary vector.
    """
    dists = ContinuousFeatureGenerator(len(continous_features))
    dists.build(FLAGS.input_dir + 'tr-all-prob.csv', continous_features)

    output = open(FLAGS.output_dir + 'feature_map','w')
    for i in continous_features:
        output.write("{0} {1}\n".format('I'+str(i), i))
    
    random.seed(0)
    # 90% of the data are used for training, and 10% of the data are used
    # for validation.
    with open(FLAGS.output_dir + 'tr.libsvm', 'w') as out_train:
        with open(FLAGS.output_dir + 'va.libsvm', 'w') as out_valid:
            with open(FLAGS.input_dir + 'tr-all-prob.csv', 'r') as f:
                head = f.readline()
                print('tr-all-prob head=',head)
                for line in f:
                    features = line.rstrip('\n').split(',')
                    feat_vals = []
                    for i in range(0, len(continous_features)):
                        val = dists.gen(i, features[continous_features[i]])
                        feat_vals.append(str(continous_features[i]) + ':' + "{0:.6f}".format(val).rstrip('0').rstrip('.'))

                    label = features[1]
                    if random.randint(0, 9999) % 10 != 0:
                        out_train.write("{0} {1}\n".format(label, ' '.join(feat_vals)))
                    else:
                        out_valid.write("{0} {1}\n".format(label, ' '.join(feat_vals)))

    with open(FLAGS.output_dir + 'te.libsvm', 'w') as out:
        with open(FLAGS.input_dir + 'all-prob.csv', 'r') as f:
            head = f.readline()
            print('all-prob head=',head)
            for line in f:
                features = line.rstrip('\n').split(',')

                feat_vals = []
                for i in range(0, len(continous_features)):
                    val = dists.gen(i, features[continous_features[i] - 1])
                    feat_vals.append(str(continous_features[i]) + ':' + "{0:.6f}".format(val).rstrip('0').rstrip('.'))

                label = features[0]
                out.write("{0} {1}\n".format(label, ' '.join(feat_vals)))


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
