#!/bin/env python3
""" 特征工程：新增特征，用户每天、每小时对广告、广告组、媒体的浏览量。。。等等 """

import csv
import sys
import argparse
from collections import defaultdict
import common as C 

def gen_uid(r):
    """ 根据设备ip和设备模式，生成 uid """
    if r['device_id'] != "a99f214a":
        return r['device_id']
    return r['device_ip'] + "_" + r['device_model']

def gen_media_id(r):
    """ 生成媒体 id """
    if r['app_id'] == "ecad2386":
        return r['site_id']
    return r['app_id']

def add(csv_file, is_train=True):
    """ 新增特征，用户每天、每小时对广告、广告组、媒体的浏览量 """
    if is_train:  
        out_csv = "data/tr_ext.csv"
        header = C.TR_EXT_FE_LS
    else:
        out_csv = "data/te_ext.csv"
        header = C.TE_EXT_FE_LS

    d = defaultdict(int) 
    h = defaultdict(int)
    t = {}

    n = 0
    day = "??"
    hour = "??"

    fp = open(out_csv, 'w')
    ocw = csv.DictWriter(fp, fieldnames=header)
    ocw.writeheader()

    for r in csv.DictReader(open(csv_file)):
        n += 1
        if n%100000 == 0:
            print(n)
        if r['hour'][4:6] != day:
            t = {}                          #时间差算的是一天之内的,所以这里也重新初始化
            d = defaultdict(int)
            day = r['hour'][4:6]
        if r['hour'][6:] != hour:
            h = defaultdict(int)
            hour = r['hour'][6:]

        # 时间戳？
        tm = int(r['hour'][6:])*60 + int(int(r['id'][:5])/100000.*60)
        uid = gen_uid(r)

        # 统计每个用户每天、每小时对广告、广告组的浏览量
        d[uid + "_" + r['C14']] += 1
        d[uid + "_" + r['C17']] += 1
        h[uid + "_" + r['C17']] += 1
        h[uid] += 1

        media_id = gen_media_id(r)
        # 统计用户对媒体的浏览量
        d[uid + "_" + media_id] += 1
        tm_delta = "-1"

        if uid not in t:
            t[uid] = tm
        else:
            tm_delta = str(tm - t[uid])
            t[uid] = tm

        r['uid'] = uid
        r['I1'] = d[uid + "_" + media_id]
        r['I2'] = h[uid + "_" + r['C17']]
        r['I3'] = h[uid]
        r['I4'] = d[uid + "_" + r['C14']]
        r['I5'] = d[uid + "_" + r['C17']]
        r['I6'] = tm_delta

        ocw.writerow(dict(r))

    fp.close()

def run():
    add("data/tr.csv")
    add("data/te.csv", False)


if __name__ == "__main__":
    run()

