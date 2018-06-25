#!/bin/env python3
import argparse, csv, sys, collections
import common as C 
import pickle

d = {}
d_app = {}
d_site = {}

def process(csv_file, is_train=True):
    if is_train:
        csv_out = "data/tr_ffm_index.csv"
        #header = C.TR_INDEX_HEADER 
        csv_out_app = "data/tr_ffm_index_app.csv"
        #header_app = C.TR_INDEX_APP_HEADER
        csv_out_site = "data/tr_ffm_index_site.csv"
        #header_site = C.TR_INDEX_SITE_HEADER
    else:
        csv_out = "data/te_ffm_index.csv"
        #header = C.TE_INDEX_HEADER 
        csv_out_app = "data/te_ffm_index_app.csv"
        #header_app = C.TE_INDEX_APP_HEADER
        csv_out_site = "data/te_ffm_index_site.csv"
        #header_site = C.TE_INDEX_SITE_HEADER

    fp = open(csv_out, 'w')
    ocw_all = csv.writer(fp, delimiter=' ')
    fp_app = open(csv_out_app, 'w')
    ocw_app = csv.writer(fp_app, delimiter=' ')
    fp_site = open(csv_out_site, 'w')
    ocw_site = csv.writer(fp_site, delimiter=' ')

    n = 0
    for r in csv.DictReader(open(csv_file, 'r')):
        n += 1
        if n%1000000 == 0:
            print(n)

        if is_train:
            if int(r['click']) == 0:
                label = -1
            else:
                label = 1
        else:
            label = -1
        
        cur_x = []
        cur_split_x = []
        cur_x.append(label)
        cur_split_x.append(label)
        is_app = False
        if r["site_id"] == "site_id_85f751fd":
            is_app = True

        for fe in r:
            if fe in ["id", "click", "hour"]:
                continue
            if fe == "I6":
                if int(r[fe].split('_')[1]) >= 50:
                    r[fe] = "{0}_50".format(fe)
            elif fe == 'I3':
                if int(r[fe].split('_')[1]) >= 20:
                    r[fe] = "{0}_20".format(fe)
            elif fe[0] == "I":
                if int(r[fe].split('_')[1]) >= 10:
                    r[fe] = "{0}_10".format(fe)
            idx = d.get(r[fe])
            if idx is None:
                cur_x.append(str(len(d)))
                d[r[fe]] = str(len(d))
            else:
                cur_x.append(idx)
            if is_app:
                d_split = d_app
                if fe in ["site_id", "site_domain", "site_category"]:
                    continue
            else:
                d_split = d_site
                if fe in ["app_id", "app_domain", "app_category"]:
                    continue
            idx_split = d_split.get(r[fe])
            if idx_split is None:
                cur_split_x.append(str(len(d_split)))
                d_split[r[fe]] = str(len(d_split))
            else:
                cur_split_x.append(idx_split)
            
            
        ocw_all.writerow(cur_x)
        if is_app:
            ocw_app.writerow(cur_split_x)
        else:
            ocw_site.writerow(cur_split_x)

    fp.close()
    fp_app.close()
    fp_site.close()


def run():
    process("data/tr_prep.csv")
    process("data/te_prep.csv", False)


if __name__ == "__main__":
    run()
