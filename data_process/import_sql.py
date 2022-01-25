from subprocess import check_output
import config
import os
FILE_LISTS = ['main01_LAWAA','main01_LAWAB','main01_LAWAC','main02_LAWAA','main02_LAWAB','main02_LAWAC']
for file in FILE_LISTS:    
    print("start ..." + file)
    fp = os.path.abspath("output_file/" + file + "_SQL.sql")
    check_output("mysql -ukite -p0000 --default-character-set=utf8 law < " + fp, shell=True)
    print("finish\r\n")
    
