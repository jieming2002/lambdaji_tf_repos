#!/bin/env python3
import pickle
import common as C 
import argparse, csv, sys, collections

counts = collections.defaultdict(int) 		#保存特征-值的频数
exp_days = collections.defaultdict(set)		#保存特征-值展示日

def stat(csv_file):
	n = 0
	global exp_days, counts
	for r in csv.DictReader(open(csv_file)):
		n += 1
		if n % 1000000 == 0:
			print(n)

		_uid = "{0}_{1}".format('uid', r['uid'])
		_dip = "{0}_{1}".format('device_ip', r['device_ip'])
		_did = "{0}_{1}".format('device_id', r['device_id'])

		counts[_uid] += 1 #统计用户id 出现次数
		counts[_dip] += 1 #统计设备ip 出现次数
		counts[_did] += 1 #统计设备id 出现次数

		exp_days[_dip].add(r['hour'][4:6])  #给集合添加元素：日期
		exp_days[_uid].add(r['hour'][4:6]) #给集合添加元素：日期

def run():
	stat("data/tr_ext.csv")
	stat("data/te_ext.csv")
	
	exp_nday = {}
	for key in exp_days:
	    exp_nday[key] = len(exp_days[key]) #得到展示的天数

	pickle.dump(counts, open("data/d3_cnt", 'wb'))
	pickle.dump(exp_nday, open('data/exp_nday_cnt', 'wb'))


if __name__ == "__main__":
	run()
