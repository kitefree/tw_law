
class LAWAC_Model:
    schema_map = {}
    AC002 = '(SELECT AA001 FROM LAWAA WHERE AA002=@pcode)'
    AC003 = ''        
    AC004 = '0'
    AC005 = ''    
    AC006 = ''    
    AC007 = ''
    AC008 = ''
    AC009 = ''
    AC010 = ''
    AC011 = ''
    def __init__(self):
        self.schema_map.setdefault('AC002','AA001_ID')
        self.schema_map.setdefault('AC003','pcode')
        self.schema_map.setdefault('AC004','AB003_ID')
        self.schema_map.setdefault('AC005','flno')
        self.schema_map.setdefault('AC006','法規名稱')
        self.schema_map.setdefault('AC007','最新異動日期')
        self.schema_map.setdefault('AC008','廢止註記')
        self.schema_map.setdefault('AC009','編章節')
        self.schema_map.setdefault('AC010','條號')
        self.schema_map.setdefault('AC011','條文內容')
    
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
        schema_word = 'AC'
        attrs = [a for a in dir(self) if not a.startswith('__') and a.startswith(schema_word)]
        for attr in attrs:
            if attr == 'AC002':
                AC002 = '(SELECT AA001 FROM LAWAA WHERE AA002=@pcode)'            
            elif attr == 'AC004':
                AC004 = '0'
            else:
                self.set_val_by_column_name(attr,'')

    def get_insert_sql(self):
        schema_word = 'AC'
        table_name = self.__class__.__name__[:-6] #remove _Model
        
        tmp_sql = 'INSERT INTO ' + table_name +  '('        
        attrs = [a for a in dir(self) if not a.startswith('__') and a.startswith(schema_word)]
        for attr in attrs:
            tmp_sql = tmp_sql + str(attr) + ","

        tmp_sql = tmp_sql[:-1] + ')VALUES('

        for attr in attrs:
            val = ''
            if attr == 'AC002':
                val = getattr(self,attr)
                val = val.replace("@pcode","'" + getattr(self,'AC003') + "'")
                tmp_sql = tmp_sql + str(val) + ","
                continue
            if attr == 'AC004':
                val = getattr(self,attr)
                if str(val) == '0':
                    val = "NULL"
                    
                tmp_sql = tmp_sql + str(val) + ","
                continue                

            
            if getattr(self,attr) != None:
                val = getattr(self,attr)            
            
            if "'" in str(val):
                val = val.replace("'","\\'")

            tmp_sql = tmp_sql + "'" + str(val) + "'" + ","
           

        tmp_sql = tmp_sql[:-1] + ');\r\n'
        return tmp_sql