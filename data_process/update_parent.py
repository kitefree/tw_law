import re
import pathlib
import os
import mysql.connector
maxdb = mysql.connector.connect(
  host = "127.0.0.1",
  user = "root",
  password = "0000",
  database = "law_test",
  )
cursor=maxdb.cursor()
 # Read
#cursor.execute("SELECT * FROM `lawab_test` where AB002='B0000001'")
cursor.execute("SELECT * FROM `LAWAB` ORDER BY AB002,AB003")
result = cursor.fetchall()


LEVEL_1_ID = '0' #編
LEVEL_2_ID = '0' #章
LEVEL_3_ID = '0' #節
LEVEL_4_ID = '0' #款
LEVEL_5_ID = '0' #目
CUR_DIR = str(pathlib.Path(__file__).parent.resolve())
LIST_SQL = []

EXCLUDE_NO = ['S0110006','S0110013','H0170012']

def get_key_word(word):  
    if re.search('\u7b2c\s.+\s\u7de8', word) != None:
        return "編"    
    #第 一 章
    elif re.search('\u7b2c\s.+\s\u7ae0', word) != None:
        return "章"
    #第一章
    elif re.search('\u7b2c.+\u7ae0', word) != None:
        return "章"        
    #第 一 節
    elif re.search('\u7b2c\s.+\s\u7bc0', word) != None:
        return "節"
    #第一節
    elif re.search('\u7b2c.+\u7bc0', word) != None:
        return "節"                  
    elif re.search('\u7b2c\s.+\s\u6b3e', word) != None:
        return "款"        
    elif re.match('\u7b2c\s.+\s\u76ee', word) != None:
        return "目"


def set_key_id(AB003,now_key_word):
    global LEVEL_1_ID,LEVEL_2_ID,LEVEL_3_ID,LEVEL_4_ID
    if now_key_word == "編":
        LEVEL_1_ID = AB003 #編 
    elif now_key_word =="章":
        LEVEL_2_ID = AB003 #章 
    elif now_key_word =="節":
        LEVEL_3_ID = AB003 #節 
    elif now_key_word =="款":
        LEVEL_4_ID = AB003 #款 
    elif now_key_word =="目":
        LEVEL_5_ID = AB003 #目 


def get_parent_key(word):
    if word =="編":
        return '0'        
    elif word =="章":
        return LEVEL_1_ID #編 
    elif word =="節":
        return LEVEL_2_ID  #章 
    elif word =="款":
        return LEVEL_3_ID  #節 
    elif word =="目":
        return LEVEL_4_ID  #款    

for row in result:
    AB002 = row[1]
    AB003 = row[2]
    AB005 = row[4]    
    #if AB005.find("第二章之一") > 0:
    #    print("AA")

    if AB002 in EXCLUDE_NO:
        continue


    now_key_word = get_key_word(AB005.lstrip())
    set_key_id(AB003,now_key_word)
    parent_key = get_parent_key(now_key_word)      
    
    #update_users = "UPDATE LAWAB_TEST SET AB006 = "  + str(parent_key) + " WHERE AB002='" + str(AB002) + "' AND AB003='" + str(AB003) + "';" 
    update_users = "UPDATE LAWAB SET AB006 =%s WHERE AB002=%s AND AB003=%s;" 
    #print(update_users)
    #LIST_SQL.append(update_users)
    #LIST_SQL.append(str(AB005) + "\t" + str(AB003) + "\t" + str(parent_key) + "\n")
    if str(parent_key) == '0':
        parent_key = None
    cursor.execute(update_users,(parent_key,str(AB002),str(AB003)))
    maxdb.commit()    
    #print(AB005,AB003,parent_key)    


#寫檔
#fp = open(CUR_DIR + "\\UPDATE_REF_KEY.txt", "w", encoding = 'utf8')
 
# # 將 lines 所有內容寫入到檔案
#fp.writelines(LIST_SQL)
 
# # 關閉檔案
#fp.close()
    
    
