
# set the path-to-files
TRAIN_FILE = "data/tr.csv"
TEST_FILE = "data/te.csv"

TRAIN_EXT_FILE = "data/tr_ext.csv"
TEST_EXT_FILE = "data/te_ext.csv"

SUB_DIR = "data"

NUM_SPLITS = 3
RANDOM_SEED = 2017

EXT_DTYPES ={
	'id':str,
	'C14':'int32',
	'banner_pos':'int32',
	'C14':'int32',
	'C15':'int32',
	'C16':'int32',
	'C17':'int32',
	'C18':'int32',
	'C19':'int32',
	'C20':'int32',
	'C21':'int32',
	'I1':'int32',
	'I2':'int32',
	'I3':'int32',
	'I4':'int32',
	'I5':'int32',
	'I6':'int32'
}

TE_EXT_FE_LS = ['id', 'hour', 'C1', 'banner_pos', 'site_id', 'site_domain', 
'site_category', 'app_id', 'app_domain', 'app_category', 'device_id', 'device_ip', 'device_model', 
'device_type', 'device_conn_type', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 
'I1', 'I2', 'I3', 'I4', 'I5', 'I6']

TR_EXT_FE_LS = ['id', 'click', 'hour', 'C1', 'banner_pos', 'site_id', 'site_domain', 
'site_category', 'app_id', 'app_domain', 'app_category', 'device_id', 'device_ip', 'device_model', 
'device_type', 'device_conn_type', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 
'I1', 'I2', 'I3', 'I4', 'I5', 'I6']

# types of columns of the dataset dataframe
CATEGORICAL_COLS = ['hour', 'C1', 'banner_pos', 'site_id', 'site_domain', 'site_category', 
'app_id', 'app_domain', 'app_category', 'device_id', 'device_ip', 'device_model', 'device_type', 'device_conn_type', 
'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21']

NUMERIC_COLS = ['I1', 'I2', 'I3', 'I4', 'I5', 'I6']

IGNORE_COLS = ['id', 'click', 'device_ip']
