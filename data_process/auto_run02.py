import pathlib
import os
from subprocess import check_output
import config

CUR_DIR = str(pathlib.Path(__file__).parent.resolve())


def import_data_to_db(db_name,db_account,db_pwd,file_name):
    file_name 
    print("  匯入資料開始:" + file_name)
    check_output("mysql -u" + db_account + " -p" + db_pwd + " --default-character-set=utf8 " + db_name + " < " + file_name, shell=True)
    print("  匯入資料結束\r\n")


def part01():
    # part 1

    print("匯入SQL檔案至資料庫開始")

    ## main01 aa
    import_data_to_db(config.DB_NAME,config.DB_ACCOUNT,config.DB_PWD,config.MAIN01["OUTPUT_FILE_NAME_AA"])

    ## main01 ab
    import_data_to_db(config.DB_NAME,config.DB_ACCOUNT,config.DB_PWD,config.MAIN01["OUTPUT_FILE_NAME_AB"])

    ## main01 ac
    import_data_to_db(config.DB_NAME,config.DB_ACCOUNT,config.DB_PWD,config.MAIN01["OUTPUT_FILE_NAME_AC"])

    ## main02 aa
    import_data_to_db(config.DB_NAME,config.DB_ACCOUNT,config.DB_PWD,config.MAIN02["OUTPUT_FILE_NAME_AA"])

    ## main02 ab
    import_data_to_db(config.DB_NAME,config.DB_ACCOUNT,config.DB_PWD,config.MAIN02["OUTPUT_FILE_NAME_AB"])

    ## main02 ac
    import_data_to_db(config.DB_NAME,config.DB_ACCOUNT,config.DB_PWD,config.MAIN02["OUTPUT_FILE_NAME_AC"])


    print("匯入SQL檔案至資料庫結束")


def part02():
    # part 2
    print("更新父子節點資料開始")
    os.system('python3 ' + CUR_DIR + '/' + 'update_parent.py')
    print("更新父子節點資料結束")

part01()
part02()


