#!/bin/env python3
import pickle
import common as C 
import argparse, csv, sys, collections

counts = collections.defaultdict(int)
def stat(csv_file):
	""" 统计每个特征的每个值的出现次数 """
	n = 0
	global days,counts
	for r in csv.DictReader(open(csv_file)):
		n += 1
		if n % 1000000 == 0:
			print(n)
		for fe in r:
			if fe in ['id', 'click', 'hour']:
				continue
			key = "{0}_{1}".format(fe, r[fe])
			counts[key] += 1
            

def run():
	stat("data/tr.csv")
	stat("data/te.csv")

	rare10 = {}
	big10  = set()

	for key in counts:
		if counts[key] >= 10:
			big10.add(key)

		fe = key.split('_')[0]
		if fe in C.FC_RARE_FE_LS and counts[key] <= 10:
			rare10[key] = counts[key]

	# 分别保存特征值出现次数大于10 和小于 10 的特征名称和特征值
	pickle.dump(big10, open('data/big10_fe', 'wb'))
	pickle.dump(rare10, open('data/rare10_cnt', 'wb'))

if __name__ == "__main__":
	run()
