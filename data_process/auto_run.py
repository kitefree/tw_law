import os

PY_LISTS = ['main01_LAWAA','main01_LAWAB','main01_LAWAC','main02_LAWAA','main02_LAWAB','main02_LAWAC','import_sql','update_parent']

for py_name in PY_LISTS:
    print('start ...' + py_name)
    os.system(py_name +".py")
    print('finish\n\r')
