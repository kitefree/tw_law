from subprocess import check_output
import config
import os
FILE_LISTS = ['main01_LAWAA','main01_LAWAB','main01_LAWAC','main02_LAWAA','main02_LAWAB','main02_LAWAC']
for file in FILE_LISTS:    
    print("start ..." + file)
    fp = os.path.abspath("output_file/" + file + "_SQL.sql")
    check_output("C:/xampp/mysql/bin/mysql -uroot -p0000 --default-character-set=utf8 law < " + fp, shell=True)
    print("finish\r\n")
    

# import mysql.connector
# maxdb = mysql.connector.connect(
#   host = "127.0.0.1",
#   user = "root",
#   password = "0000",
#   database = "law",
#   )

# utf8_file = open("E:\\GitWorkSpace\\tw_law\\data_process\\output_file\\main01_LAWAA_SQL.sql", encoding="UTF-8")
# contents = utf8_file.readlines()

# all_str = ''
# for c in contents:
#     all_str = all_str + c
# cursor=maxdb.cursor()
#  # Read
# #cursor.execute("SELECT * FROM `lawab_test` where AB002='B0000001'")
# cursor.execute(all_str)