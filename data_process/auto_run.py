import os

PY_LISTS = ['main01_LAWAA','main01_LAWAB','main01_LAWAC','main02_LAWAA','main02_LAWAB','main02_LAWAC','import_sql','update_parent']

for py_name in PY_LISTS:
    print('start ...' + py_name)
    os.system(py_name +".py")
    print('finish\n\r')


# print('start main01_LAWAB')
# os.system("main01_LAWAB.py")
# print('finish main01_LAWAB')

# print('start main01_LAWAC')
# os.system("main01_LAWAC.py")
# print('finish main01_LAWAC')


# print('start main02_LAWAA')
# os.system("main02_LAWAA.py")
# print('finish main02_LAWAA')

# print('start main02_LAWAB')
# os.system("main02_LAWAB.py")
# print('finish main02_LAWAB')

# print('start main02_LAWAC')
# os.system("main02_LAWAC.py")
# print('finish main02_LAWAC')

