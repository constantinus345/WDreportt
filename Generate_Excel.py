import mongo_funcs
import configs

#after_unix_date= mongo_funcs.maxdate_path(configs.Folder_Excel)
after_unix_date = 1640717029
mongo_funcs.Mongo_toExcel(configs.Folder_Excel, after_unix_date)