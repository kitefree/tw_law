
class LAWAB_Model:
    schema_map = {}
    AB001 = '(SELECT AA001 FROM LAWAA WHERE AA002=@pcode)'
    AB002 = ''    
    AB003 = ''    
    AB004 = ''    
    AB005 = ''    
    def __init__(self):
        self.schema_map.setdefault('AB002','pcode')
        self.schema_map.setdefault('AB003','sno')
        self.schema_map.setdefault('AB004','法規名稱')
        self.schema_map.setdefault('AB005','編章節')


    
    def get_key_by_tagname(self,tagname):
        try:
            for key, dictVal in self.schema_map.items():
                if dictVal == tagname:
                    return key
        except:
            print('no found key:' + tagname)
    
    def set_val_by_column_name(self,col_name,col_val):
        setattr(self,col_name,col_val)       

    def set_val_by_tagname(self,tagname,col_val):
        col_name = self.get_key_by_tagname(tagname)
        self.set_val_by_column_name(col_name,col_val)
         
    def reset_all_attr(self):
        schema_word = 'AB'
        attrs = [a for a in dir(self) if not a.startswith('__') and a.startswith(schema_word)]
        for attr in attrs:
            if attr == 'AB001':
                AB001 = '(SELECT AA001 FROM LAWAA WHERE AA002=@pcode)'
            else:
                self.set_val_by_column_name(attr,'')

    def get_insert_sql(self):
        schema_word = 'AB'
        table_name = self.__class__.__name__[:-6] #remove _Model
        
        tmp_sql = 'INSERT INTO ' + table_name +  '('        
        attrs = [a for a in dir(self) if not a.startswith('__') and a.startswith(schema_word)]
        for attr in attrs:
            tmp_sql = tmp_sql + str(attr) + ","

        tmp_sql = tmp_sql[:-1] + ')VALUES('

        for attr in attrs:
            val = ''
            if attr == 'AB001':
                val = getattr(self,attr)
                val = val.replace("@pcode","'" + getattr(self,'AB002') + "'")
                tmp_sql = tmp_sql + str(val) + ","
                continue
            
            if getattr(self,attr) != None:
                val = getattr(self,attr)            
            
            if "'" in str(val):
                val = val.replace("'","\\'")

            tmp_sql = tmp_sql + "'" + str(val) + "'" + ","
           

        tmp_sql = tmp_sql[:-1] + ');\r\n'
        return tmp_sql
        #print(tmp_sql)
