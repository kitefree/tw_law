
class LAWAA_Model:
    schema_map = {}
    AA002 = ''
    AA003 = ''
    AA004 = ''
    AA005 = ''
    AA006 = ''
    AA007 = ''
    AA008 = ''
    AA009 = ''
    AA010 = ''
    AA011 = ''
    AA012 = ''
    AA013 = ''
    AA014 = ''
    AA015 = ''
    def __init__(self):
        self.schema_map.setdefault('AA002','pcode')
        self.schema_map.setdefault('AA003','法規性質')
        self.schema_map.setdefault('AA004','法規名稱')
        self.schema_map.setdefault('AA005','法規網址')
        self.schema_map.setdefault('AA006','法規類別')
        self.schema_map.setdefault('AA007','最新異動日期')
        self.schema_map.setdefault('AA008','生效日期')
        self.schema_map.setdefault('AA009','生效內容')
        self.schema_map.setdefault('AA010','廢止註記')
        self.schema_map.setdefault('AA011','是否英譯註記')
        self.schema_map.setdefault('AA012','英文法規名稱')
        self.schema_map.setdefault('AA013','沿革內容')
        self.schema_map.setdefault('AA014','前言')
        self.schema_map.setdefault('AA015','法規內容')
        self.schema_map.setdefault('AA016','附件')
    
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
        schema_word = 'AA'
        attrs = [a for a in dir(self) if not a.startswith('__') and a.startswith(schema_word)]
        for attr in attrs:
            self.set_val_by_column_name(attr,'')

    def get_insert_sql(self):
        schema_word = 'AA'
        table_name = self.__class__.__name__[:-6] #remove _Model
        
        tmp_sql = 'INSERT INTO ' + table_name +  '('        
        attrs = [a for a in dir(self) if not a.startswith('__') and a.startswith(schema_word)]
        for attr in attrs:
            tmp_sql = tmp_sql + str(attr) + ","

        tmp_sql = tmp_sql[:-1] + ')VALUES('

        for attr in attrs:
            val = ''

            if getattr(self,attr) != None:
                val = getattr(self,attr)
            
            if "'" in str(val):
                val = val.replace("'","\\'")
            
            tmp_sql = tmp_sql + "'" + str(val) + "'" + ","

        tmp_sql = tmp_sql[:-1] + ');\r\n'
        return tmp_sql
        #print(tmp_sql)
