#!/bin/env python3
import argparse, csv, sys, collections
import common as C 
import pickle

def process(csv_file, is_train=True):
	if is_train:
		csv_out = "data/tr_prep.csv"
		header = C.TR_EXT_FE_LS 
	else:
		csv_out = "data/te_prep.csv"
		header = C.TE_EXT_FE_LS

	fp = open(csv_out, 'w')
	ocw = csv.DictWriter(fp, fieldnames=header)
	ocw.writeheader()

	n = 0
	for r in csv.DictReader(open(csv_file, 'r')):
		n += 1
		if n%1000000 == 0:
			print(n)
			
		for fe in r:
			if fe in ['id', 'click', 'hour']:
				continue

			if fe == 'device_id':
				_did = '{0}_{1}'.format(fe, r[fe])
				if rare10.get(_did) is not None:
					r[fe] = "{0}_rare_{1}".format(fe, r[fe])
			elif fe == 'device_ip':
				_dip = '{0}_{1}'.format(fe, r[fe])
				if rare10.get(_dip) is not None:
					r[fe] = "{0}_rare_{1}".format(fe, r[fe])
			elif fe == 'uid':
				_uid = '{0}_{1}'.format(fe, r[fe])
				if rare10.get(_uid) is not None:
					r[fe] = "{0}_rare_{1}".format(fe, r[fe])
				elif exp_nday.get(_uid) == 1:
					r[fe] = "v_id_s"
			else:
				#新增的数值型特征
				fe_v = "{0}_{1}".format(fe, r[fe])
				if fe_v not in big10 and fe[0] != 'I': #数值型
					r[fe] = "{0}_rare".format(fe)
				else:
					r[fe] = fe_v
			#r[''] = "exp_nday_{0}".format(str(exp_nday))
		ocw.writerow(dict(r))

	fp.close()

big10 = pickle.load(open('data/big10_fe', 'rb'))
rare10 = pickle.load(open('data/rare10_cnt', 'rb'))
exp_nday = pickle.load(open('data/exp_nday_cnt', 'rb'))

process("data/tr_ext.csv")
process("data/te_ext.csv", False)
