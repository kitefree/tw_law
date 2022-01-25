import pathlib
import os
CUR_DIR = str(pathlib.Path(__file__).parent.resolve())

PY_LISTS = ['main01_LAWAA','main01_LAWAB','main01_LAWAC','main02_LAWAA','main02_LAWAB','main02_LAWAC','import_sql','update_parent']


for py_name in PY_LISTS:
    #print('start ...' + py_name)
    print(CUR_DIR + "/" + py_name +".py")
    os.system(CUR_DIR + "/" + py_name +".py")
    #print('finish\n\r')
