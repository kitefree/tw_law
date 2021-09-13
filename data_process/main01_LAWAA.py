import xml.etree.ElementTree as ET
import pathlib
import os
import config
from LAWAA_Model import LAWAA_Model


#https://stackoverflow.com/questions/15748528/python-how-to-determine-hierarchy-level-of-parsed-xml-elements

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

root = ET.parse(config.MAIN01['INPUT_FILE_NAME'])
perf_func(root.getroot(), print_level)

#print 階層
# for n in NODE_LIST:
#     print(n)


LIST_SQL = []
lawaa_model = LAWAA_Model()

for nodes_01 in root.getroot():
    lawaa_model.reset_all_attr() 
    for nodes_02 in nodes_01:
        if nodes_02.tag == '法規網址':
            pcode_val = nodes_02.text[-8:]
            lawaa_model.set_val_by_tagname('pcode',pcode_val)        
        
        lawaa_model.set_val_by_tagname(nodes_02.tag,nodes_02.text)
        # print(nodes_02.tag,":",nodes_02.text)
    
    LIST_SQL.append(lawaa_model.get_insert_sql())




#col = lwaa_model.get_key_by_tagname('法規性質')
#lwaa_model.set_val_by_column_name('AA002','kite')
#print(lwaa_model.AA002)
#lwaa_model.reset_all_attr()
#print(lwaa_model.AA002)
#print(col)

#lwaa_model.get_insert_sql()

#print(LIST_SQL)

#寫檔
fp = open(config.MAIN01['OUTPUT_FILE_NAME_AA'], "w", encoding = 'utf8')
 
# # 將 lines 所有內容寫入到檔案
# lines = ["One\n", "Two\n", "Three\n", "Four\n", "Five\n"]
fp.writelines(LIST_SQL)
 
# # 關閉檔案
fp.close()