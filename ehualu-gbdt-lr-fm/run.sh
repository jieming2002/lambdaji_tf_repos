echo "run addi.py ......"
python3 addi.py 

echo "run count.py ......"
python3 count.py 

echo "run count_ext.py ......"
python3 count_ext.py 

echo "run prep.py ......"
python3 prep.py

echo "run gbdt-prep.py ......"
python3 gbdt-prep.py 

echo "run gbdt"
gbdt/gbdt -d 5 -t 19 data/te_dense data/tr_dense data/te_gbdt_out data/tr_gbdt_out 

echo "run index.py ......"
python3 index.py

echo "run gbdt-append.py ......"
python3 gbdt-append.py

echo "run ffm"
fm/fm -k 8 -t 5 -l 0.00003 data/te_ffm_gbdt_index.csv data/tr_ffm_gbdt_index.csv
fm/fm -k 8 -t 4 -l 0.00004 data/te_ffm_gbdt_index_app.csv data/tr_ffm_gbdt_index_app.csv
fm/fm -k 8 -t 10 -l 0.00005 data/te_ffm_gbdt_index_site.csv data/tr_ffm_gbdt_index_site.csv

echo "run sub"
python3 sub.py
