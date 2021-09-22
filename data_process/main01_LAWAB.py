import xml.etree.ElementTree as ET
import pathlib
import os
from pathlib import Path
from LAWAB_Model import LAWAB_Model
import config

#https://stackoverflow.com/questions/15748528/python-how-to-determine-hierarchy-level-of-parsed-xml-elements

NODE_LIST = []
NODE_IDX = 1
LIST_SQL = []
SNO = 1

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

root = ET.parse(config.MAIN01['INPUT_FILE_NAME'])
perf_func(root.getroot(), print_level)


lawab_model = LAWAB_Model()


for nodes_01 in root.getroot():
    lawab_model.reset_all_attr() 
    for nodes_02 in nodes_01:
        #第一層
        if nodes_02.tag == '法規網址':
            pcode_val = nodes_02.text[-8:]
            lawab_model.set_val_by_tagname('pcode',pcode_val)
        elif nodes_02.tag == '法規名稱':
            lawab_model.set_val_by_tagname(nodes_02.tag,nodes_02.text)
        elif nodes_02.tag == '法規內容':
            SNO = 1
            for nodes_03 in nodes_02:
                #第二層
                if nodes_03.tag =='編章節':
                    lawab_model.set_val_by_tagname('sno',SNO)
                    lawab_model.set_val_by_tagname(nodes_03.tag,nodes_03.text)
                    LIST_SQL.append(lawab_model.get_insert_sql())
                    SNO = SNO + 1
    
    
# 建立資料夾
Path(config.CUR_DIR + "\\" + config.OUTPUT_FILE_ROOT_PATH).mkdir(parents=True, exist_ok=True)

#寫檔
fp = open(config.MAIN01['OUTPUT_FILE_NAME_AB'], "w", encoding = 'utf8')

fp.writelines(LIST_SQL)

fp.close()