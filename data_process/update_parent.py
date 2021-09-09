# Connect MySQL
import mysql.connector
maxdb = mysql.connector.connect(
  host = "127.0.0.1",
  user = "root",
  password = "0000",
  database = "law_test",
  )
cursor=maxdb.cursor()
 # Read
cursor.execute("SELECT * FROM `lawab_test` where AB002='B0000001'")
result = cursor.fetchall()


LEVEL_1_ID = '' #編
LEVEL_2_ID = '' #章
LEVEL_3_ID = '' #節
LEVEL_4_ID = '' #款
LEVEL_5_ID = '' #目


      

def get_key_word(word):  
    if word.find(" 編 ") > 0:
        return " 編 "    
    elif word.find(" 章 ") > 0:
        return " 章 "   
    elif word.find(" 節 ") > 0:
        return " 節 "       
    elif word.find(" 款 ") > 0:
        return " 款 "        
    elif word.find(" 目 ") > 0:
        return " 目 "   

def set_key_id(AB003,now_key_word):
    global LEVEL_1_ID,LEVEL_2_ID,LEVEL_3_ID,LEVEL_4_ID
    if now_key_word == " 編 ":
        LEVEL_1_ID = AB003 #編 
    elif now_key_word ==" 章 ":
        LEVEL_2_ID = AB003 #章 
    elif now_key_word ==" 節 ":
        LEVEL_3_ID = AB003 #節 
    elif now_key_word ==" 款 ":
        LEVEL_4_ID = AB003 #款 
    elif now_key_word ==" 目 ":
        LEVEL_5_ID = AB003 #目 

def get_parent_key(word):
    if word ==" 編 ":
        return ''        
    elif word ==" 章 ":
        return LEVEL_1_ID #編 
    elif word ==" 節 ":
        return LEVEL_2_ID  #章 
    elif word ==" 款 ":
        return LEVEL_3_ID  #節 
    elif word ==" 目 ":
        return LEVEL_4_ID  #款    

for row in result:
    AB003 = row[2]
    AB005 = row[4]
    now_key_word = get_key_word(AB005)
    set_key_id(AB003,now_key_word)
    parent_key = get_parent_key(now_key_word)    
    print(AB005,AB003,parent_key)
    
