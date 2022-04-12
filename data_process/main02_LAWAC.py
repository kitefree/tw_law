import xml.etree.ElementTree as ET
import pathlib
import os
from pathlib import Path
from LAWAC_Model import LAWAC_Model
import config

#https://stackoverflow.com/questions/15748528/python-how-to-determine-hierarchy-level-of-parsed-xml-elements


NODE_LIST = []
NODE_IDX = 1
LIST_SQL = []
AB003_ID = 0

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

root = ET.parse(config.MAIN02['INPUT_FILE_NAME'])
perf_func(root.getroot(), print_level)


lawac_model = LAWAC_Model()

for nodes_01 in root.getroot():    
    lawac_model.reset_all_attr()
    for nodes_02 in nodes_01:
        #第一層
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
                #第二層          
                if nodes_03.tag =='編章節':
                    AB003_ID = AB003_ID + 1
                    lawac_model.set_val_by_tagname(nodes_03.tag,nodes_03.text)
                    lawac_model.set_val_by_tagname('AB003_ID',AB003_ID)
                    
                elif nodes_03.tag =='條文':
                    for nodes_04 in nodes_03:
                        #第三層
                        if nodes_04.tag == '條號':
                            AC005 = nodes_04.text.replace('第','').replace('條','').strip()                            
                            lawac_model.set_val_by_tagname('flno',AC005)
                            lawac_model.set_val_by_tagname(nodes_04.tag,nodes_04.text)
                        else:
                            lawac_model.set_val_by_tagname(nodes_04.tag,nodes_04.text)
                    
                    LIST_SQL.append(lawac_model.get_insert_sql())
                    LIST_SQL.append('\n')        
                        
            
# 建立資料夾
Path(config.CUR_DIR + "/" + config.OUTPUT_FILE_ROOT_PATH).mkdir(parents=True, exist_ok=True)


#寫檔
fp = open(config.MAIN02['OUTPUT_FILE_NAME_AC'], "w", encoding = 'utf8')
 
# 將 lines 所有內容寫入到檔案
fp.writelines(LIST_SQL)
 
# 關閉檔案
fp.close()