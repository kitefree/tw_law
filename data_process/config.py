import pathlib
import os
CUR_DIR = str(pathlib.Path(__file__).parent.resolve())
INPUT_FILE_ROOT_PATH = 'input_file\\20210819'
OUTPUT_FILE_ROOT_PATH = 'output_file'
# 法律資料
MAIN01 = {
    'INPUT_FILE_NAME' : CUR_DIR + '\\' + INPUT_FILE_ROOT_PATH + '\\FalV.xml'
    ,'OUTPUT_FILE_NAME_AA' : CUR_DIR + '\\' + OUTPUT_FILE_ROOT_PATH + '\\main01_LAWAA_SQL.sql'
    ,'OUTPUT_FILE_NAME_AB' : CUR_DIR + '\\' + OUTPUT_FILE_ROOT_PATH + '\\main01_LAWAB_SQL.sql'
    ,'OUTPUT_FILE_NAME_AC' : CUR_DIR + '\\' + OUTPUT_FILE_ROOT_PATH + '\\main01_LAWAC_SQL.sql'
}
# 命令資料
MAIN02 = {
    'INPUT_FILE_NAME' : CUR_DIR + '\\' + INPUT_FILE_ROOT_PATH + '\\MingLing.xml'
    ,'OUTPUT_FILE_NAME_AA' : CUR_DIR + '\\' + OUTPUT_FILE_ROOT_PATH + '\\main02_LAWAA_SQL.sql'
    ,'OUTPUT_FILE_NAME_AB' : CUR_DIR + '\\' + OUTPUT_FILE_ROOT_PATH + '\\main02_LAWAB_SQL.sql'
    ,'OUTPUT_FILE_NAME_AC' : CUR_DIR + '\\' + OUTPUT_FILE_ROOT_PATH + '\\main02_LAWAC_SQL.sql'
}
