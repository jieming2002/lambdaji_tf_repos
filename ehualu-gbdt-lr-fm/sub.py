import csv
import collections


def process(csv_file, predict_file):
	n = 0
	sub_csv = "data/submission.csv"
	ocw = csv.DictWriter(open(sub_csv, 'w'), fieldnames=['id', 'click'])
	ocw.writeheader()

	line = collections.defaultdict()
	for r, p in zip(csv.DictReader(open(csv_file)), open(predict_file)):
		n += 1
		if n%1000000 == 0:
			print(n)

		line['id'] = r['id']
		line['click'] = float(p)
		ocw.writerow(dict(line))


def run():
	process("data/te.csv", "data/te_ffm_gbdt_index.csv.out")


if __name__ == "__main__":
	run()
