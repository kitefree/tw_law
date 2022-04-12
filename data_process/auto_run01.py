import pathlib
import os
CUR_DIR = str(pathlib.Path(__file__).parent.resolve())

#法律
PY_LISTS01 = ['main01_LAWAA','main01_LAWAB','main01_LAWAC']

#命令
PY_LISTS02 = ['main02_LAWAA','main02_LAWAB','main02_LAWAC']


print('將XML轉為SQL檔案開始\n\r')

# 處理法律資料
print('  轉換法律資料開始\n\r')

for py_name in PY_LISTS01:
    print('    執行開始: ' + py_name)
    #print(CUR_DIR + '/' + py_name + '.py')
    os.system('python3 ' + CUR_DIR + '/' + py_name + '.py')
    print('    執行結束\n\r')

print('  轉換法律資料結束\n\r')

# 處理命令資料
print('  轉換命令資料開始\n\r')

for py_name in PY_LISTS02:
    print('    執行開始: ' + py_name)
    #print(CUR_DIR + '/' + py_name + '.py')
    os.system('python3 ' + CUR_DIR + '/' + py_name + '.py')
    print('    執行結束\n\r')

print('  轉換命令資料結束\n\r')


print('將XML轉為SQL檔案結束\n\r')

