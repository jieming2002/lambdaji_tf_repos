import csv
import sys
import argparse
from collections import defaultdict
import config_avazu_ctr as config 

def gen_uid(r):
    if r['device_id'] != "a99f214a":
        return r['device_id']
    return r['device_ip'] + "_" + r['device_model']

def gen_media_id(r):
    if r['app_id'] == "ecad2386":
        return r['site_id']
    return r['app_id']

def add_numeric(csv_file, csv_out, is_train=True):
    if is_train:  
        header = config.TR_EXT_FE_LS
    else:
        header = config.TE_EXT_FE_LS

    t = {}
    d = defaultdict(int) 
    h = defaultdict(int)

    day = "??"
    hour = "??"

    fp = open(csv_out, 'w')
    ocw = csv.DictWriter(fp, fieldnames=header)
    ocw.writeheader()

    for r in csv.DictReader(open(csv_file)):
        if r['hour'][4:6] != day:
            t = {}                          #时间差算的是一天之内的,所以这里也重新初始化
            d = defaultdict(int)
            day = r['hour'][4:6]
        if r['hour'][6:] != hour:
            h = defaultdict(int)
            hour = r['hour'][6:]

        tm = int(r['hour'][6:])*60 + int(int(r['id'][:5])/100000.*60)
        uid = gen_uid(r)
    
        d[uid + "_" + r['C14']] += 1
        d[uid + "_" + r['C17']] += 1
        h[uid + "_" + r['C17']] += 1
        h[uid] += 1

        media_id = gen_media_id(r)
        d[uid + "_" + media_id] += 1
        tm_delta = "-1"

        if uid not in t:
            t[uid] = tm
        else:
            tm_delta = str(tm - t[uid])
            t[uid] = tm

        r['I1'] = d[uid + "_" + media_id]
        r['I2'] = h[uid + "_" + r['C17']]
        r['I3'] = h[uid]
        r['I4'] = d[uid + "_" + r['C14']]
        r['I5'] = d[uid + "_" + r['C17']]
        r['I6'] = tm_delta

        ocw.writerow(dict(r))

    fp.close()

