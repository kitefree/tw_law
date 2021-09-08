import xml.etree.ElementTree as ET
import pathlib
import os
from LAWAC_Model import LAWAC_Model


#https://stackoverflow.com/questions/15748528/python-how-to-determine-hierarchy-level-of-parsed-xml-elements


CUR_DIR = str(pathlib.Path(__file__).parent.resolve())
FILE_NAME = 'MingLing.xml'

NODE_LIST = []
NODE_IDX = 1

def re_print_tag(ll,deep=False):
    global NODE_IDX,NODE_LIST
    if deep == True:
        NODE_IDX = NODE_IDX + 1
    if str(NODE_IDX) + ll.tag not in NODE_LIST:        
        NODE_LIST.append(str(NODE_IDX) + ll.tag)    
    if len(list(ll)):        
        #print(ll.tag)
        for l in ll:            
            re_print_tag(l,True)
    else:
        return
        



def perf_func(elem, func, level=0):
    func(elem,level)
    for child in elem:
        perf_func(child, func, level+1)

def print_level(elem,level):
    if '-'*level+elem.tag not in NODE_LIST:        
        NODE_LIST.append('-'*level+elem.tag)       
    #print('-'*level+elem.tag)

root = ET.parse(CUR_DIR + '\\' + FILE_NAME)
perf_func(root.getroot(), print_level)



LIST_SQL = []
AB003_ID = 0
lawac_model = LAWAC_Model()

# test code
# for nodes_01 in root.getroot():
#     for nodes_02 in nodes_01:
#         if nodes_02.tag == '法規性質' or nodes_02.tag == '法規名稱':
#             print(nodes_02.tag,":",nodes_02.text)
#             LIST_SQL.append(nodes_02.tag+":"+nodes_02.text + '\n')
#         elif nodes_02.tag == '法規網址':
#             pcode_val = nodes_02.text[-8:]
#             LIST_SQL.append('pcode' + ':' + pcode_val + '\n')
#         elif nodes_02.tag == '法規內容':
#             tmp_AC006 = '' #編章節
#             for nodes_03 in nodes_02:                
#                 if nodes_03.tag =='編章節':
#                     tmp_AC006 = nodes_03.text        
#                     LIST_SQL.append(nodes_03.tag+':'+nodes_03.text + '\n')
#                 elif nodes_03.tag =='條文':
#                     for nodes_04 in nodes_03:
#                         if nodes_04.tag == '條號':
#                             LIST_SQL.append(nodes_04.tag+':'+nodes_04.text + '\n')
                    
#             LIST_SQL.append('\n')
            

# #寫檔
# fp = open(CUR_DIR + "\\中文法規_法律資料_編章節_LAWAC_SQL_test.txt", "w", encoding = 'utf8')

# # # 將 lines 所有內容寫入到檔案
# # lines = ["One\n", "Two\n", "Three\n", "Four\n", "Five\n"]
# fp.writelines(LIST_SQL)
 
# # # 關閉檔案
# fp.close()

# exit




# LAWAC
# AC001 AA001 ID refkey
# AC002 AA002 代號(pcode) refkey 
# AC003 AB003 ID refkey 
# AC004 SELF ID(flno) 
# AC005 法規名稱 AA004 法規名稱 refkey
# AC006 AB005 編章節(編、章、節、款、目)    refkey
# AC007 條號
# AC008 條文內容
    

for nodes_01 in root.getroot():
    lawac_model.reset_all_attr()    
    for nodes_02 in nodes_01:
        if nodes_02.tag == '法規網址':
            pcode_val = nodes_02.text[-8:]
            lawac_model.set_val_by_tagname('pcode',pcode_val)
        elif nodes_02.tag == '法規名稱':
            lawac_model.set_val_by_tagname(nodes_02.tag,nodes_02.text)
        elif nodes_02.tag == '最新異動日期':
            lawac_model.set_val_by_tagname(nodes_02.tag,nodes_02.text)            
        elif nodes_02.tag == '廢止註記':
            lawac_model.set_val_by_tagname(nodes_02.tag,nodes_02.text)                 
        elif nodes_02.tag == '法規內容':
            AB003_ID = 0
            lawac_model.set_val_by_tagname('AB003_ID',AB003_ID)

            for nodes_03 in nodes_02:                
                if nodes_03.tag =='編章節':
                    AB003_ID = AB003_ID + 1
                    lawac_model.set_val_by_tagname(nodes_03.tag,nodes_03.text)
                    lawac_model.set_val_by_tagname('AB003_ID',AB003_ID)
                    
                elif nodes_03.tag =='條文':
                    for nodes_04 in nodes_03:
                        if nodes_04.tag == '條號':
                            AC005 = nodes_04.text.replace('第','').replace('條','').strip()                            
                            lawac_model.set_val_by_tagname('flno',AC005)
                            lawac_model.set_val_by_tagname(nodes_04.tag,nodes_04.text)
                        else:
                            lawac_model.set_val_by_tagname(nodes_04.tag,nodes_04.text)
                    
                    LIST_SQL.append(lawac_model.get_insert_sql())
                    LIST_SQL.append('\n')        
                        
            



#寫檔
fp = open(CUR_DIR + "\\中文法規_命令資料_編章節_LAWAC_SQL.txt", "w", encoding = 'utf8')
 
# 將 lines 所有內容寫入到檔案
fp.writelines(LIST_SQL)
 
# 關閉檔案
fp.close()