#!/bin/env python3
import pickle
import common as C 
import argparse, csv, sys, collections

# 读取提前处理好的数据
# 保存device_ip,device_id,uid出现的频数
d3_cnt = pickle.load(open('data/d3_cnt', 'rb'))

#准备稠密数据集
def process(csv_file, is_train=True):
	y = None
	global d3_cnt

	output_file = "data/tr_dense" if is_train else "data/te_dense"
	fp = open(output_file, 'w')

	n = 0
	for r in csv.DictReader(open(csv_file)):
		n += 1
		if n%1000000 == 0:
		    print(n)

		if is_train:
			click = int(r['click'])
			y = 0 if click == -1 else click
		else:
			y = -1

		ls = [y]
		for fe in r: #遍历样本的每个特征 fe 是特征列名
			if fe in ['id', 'click', 'hour']:
				continue

			if fe == "device_ip":
				_dip = "{0}_{1}".format('device_ip', r['device_ip'])
				ls.append(d3_cnt[_dip]) 
			elif fe == "uid":
				_uid = "{0}_{1}".format('uid', r['uid'])
				ls.append(d3_cnt[_uid])
			elif fe[0] == 'I':
				ls.append(int(r[fe]))

		ls = [str(e) for e in ls]
		fp.write(' '.join(ls) + '\n')

	fp.close()

def run():
	process("data/tr_ext.csv")
	process("data/te_ext.csv", False)


if __name__ == "__main__":
	run()

