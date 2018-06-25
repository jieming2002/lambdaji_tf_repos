# 不同的特征工程，得到不同的属性列
# FC mean what ?
FC_FE_LS = ['C1', 'banner_pos', 'site_id', 'site_domain', 'site_category', 'app_id', 'app_domain', 'app_category', 'device_id', 'device_ip', 'device_model', 'device_type', 'device_conn_type', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21']
# 测试集输出特征
TE_EXT_FE_LS = ['id', 'hour', 'C1', 'banner_pos', 'site_id', 'site_domain', 'site_category', 'app_id', 'app_domain', 'app_category', 'device_id', 'device_ip', 'device_model', 'device_type', 'device_conn_type', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 'uid', 'I1', 'I2', 'I3', 'I4', 'I5', 'I6']
# 训练集输出特征
TR_EXT_FE_LS = ['id', 'click', 'hour', 'C1', 'banner_pos', 'site_id', 'site_domain', 'site_category', 'app_id', 'app_domain', 'app_category', 'device_id', 'device_ip', 'device_model', 'device_type', 'device_conn_type', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 'uid', 'I1', 'I2', 'I3', 'I4', 'I5', 'I6']
# 稀有特征
FC_RARE_FE_LS = ['device_id', 'device_ip', 'uid']
