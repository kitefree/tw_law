import xml.etree.ElementTree as ET
import pathlib
import os
from pathlib import Path
from LAWAA_Model import LAWAA_Model
import config

#https://stackoverflow.com/questions/15748528/python-how-to-determine-hierarchy-level-of-parsed-xml-elements

NODE_LIST = []
NODE_IDX = 1
LIST_SQL = []

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

lawaa_model = LAWAA_Model()

for nodes_01 in root.getroot():

    lawaa_model.reset_all_attr()
   
    for nodes_02 in nodes_01:
        #第一層
        if nodes_02.tag == '法規網址':
            pcode_val = nodes_02.text[-8:]
            lawaa_model.set_val_by_tagname('pcode',pcode_val)        
        
        lawaa_model.set_val_by_tagname(nodes_02.tag,nodes_02.text)
    
    LIST_SQL.append(lawaa_model.get_insert_sql())


# 建立資料夾
Path(config.CUR_DIR + "/" + config.OUTPUT_FILE_ROOT_PATH).mkdir(parents=True, exist_ok=True)

# 寫檔
fp = open(config.MAIN01['OUTPUT_FILE_NAME_AA'], "w", encoding = 'utf8')

fp.writelines(LIST_SQL)

fp.close()