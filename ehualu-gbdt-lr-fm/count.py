#!/bin/env python3
import pickle
import common as C 
import argparse, csv, sys, collections

counts = collections.defaultdict(int)
def stat(csv_file):
	""" ͳ��ÿ��������ÿ��ֵ�ĳ��ִ��� """
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

	# �ֱ𱣴�����ֵ���ִ�������10 ��С�� 10 ���������ƺ�����ֵ
	pickle.dump(big10, open('data/big10_fe', 'wb'))
	pickle.dump(rare10, open('data/rare10_cnt', 'wb'))

if __name__ == "__main__":
	run()
