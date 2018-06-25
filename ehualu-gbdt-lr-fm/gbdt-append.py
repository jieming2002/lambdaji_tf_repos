#!/bin/env python3
import argparse, csv, sys, collections
import common as C 
import pickle

d = {}
d_app = {}
d_site = {}

def process(csv_file, gbdt_file, is_train=True):
    if is_train:
        csv_out = "data/tr_ffm_gbdt_index.csv"
        #header = C.TR_INDEX_HEADER 
        csv_out_app = "data/tr_ffm_gbdt_index_app.csv"
        #header_app = C.TR_INDEX_APP_HEADER
        csv_out_site = "data/tr_ffm_gbdt_index_site.csv"
        #header_site = C.TR_INDEX_SITE_HEADER
    else:
        csv_out = "data/te_ffm_gbdt_index.csv"
        #header = C.TE_INDEX_HEADER 
        csv_out_app = "data/te_ffm_gbdt_index_app.csv"
        #header_app = C.TE_INDEX_APP_HEADER
        csv_out_site = "data/te_ffm_gbdt_index_site.csv"
        #header_site = C.TE_INDEX_SITE_HEADER

    ocw_all = csv.writer(open(csv_out, 'w'), delimiter=' ')
    ocw_app = csv.writer(open(csv_out_app, 'w'), delimiter=' ')
    ocw_site = csv.writer(open(csv_out_site, 'w'), delimiter=' ')

    n = 0
    for r, line_gbdt in zip(csv.DictReader(open(csv_file)), open(gbdt_file)):
        n += 1
        if n%1000000 == 0:
            print(n)

        if is_train:
            if int(r['click']) == 0:
                y = -1
            else:
                y = 1
        else:
            y = -1
        
        cur_x = [y]
        cur_split_x = [y]
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
                cur_x.append(len(d))
                d[r[fe]] = len(d)
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
                cur_split_x.append(len(d_split))
                d_split[r[fe]] = len(d_split)
            else:
                cur_split_x.append(idx_split)
            
        line_gbdt_ls = line_gbdt.split()
        for i in range(1, len(line_gbdt_ls)):
        	fe2 = "gbdt_{0}_{1}".format(i, line_gbdt_ls[i])
        	idx2 = d.get(fe2)
        	if idx2 is None:
        		cur_x.append(len(d))
        		d[fe2] = len(d)
        	else:
        		cur_x.append(idx2)

        	idx2_split = d_split.get(fe2)
        	if idx2_split is None:
        		cur_split_x.append(len(d_split))
        		d_split[fe2] = len(d_split)
        	else:
        		cur_split_x.append(idx2_split)


        ocw_all.writerow(list(map(str, cur_x)))
        if is_app:
            ocw_app.writerow(list(map(str, cur_split_x)))
        else:
            ocw_site.writerow(list(map(str, cur_split_x)))


def run():
    process("data/tr_prep.csv", "data/tr_gbdt_out")
    process("data/te_prep.csv", "data/te_gbdt_out", False)


if __name__ == "__main__":
    run()
