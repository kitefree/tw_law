
# TABLE Schema

## LAWAA

```text
===================================
LAWAA 法規-單頭
===================================
AA001	SELF ID autokey PK KEY
AA002	代號(pcode) A0000001 
AA003	法規性質    憲法                                
AA004	法規名稱    中華民國憲法   
AA005	法規網址    https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=A0000001
AA006	法規類別   
AA007	最新異動日期         
AA008	生效日期   
AA009	生效內容   
AA010	廢止註記   
AA011	是否英譯註記
AA012	英文法規名稱
AA013	沿革內容
AA014	前言           
AA015	法規內容
AA016	附件
```

## LAWAB

```text
===================================
LAWAB 編章節-單身
===================================
AB001 AA001 ID refkey
AB002 AA002 代號(pcode) refkey 
AB003 SELF ID(bp) sno
AB004 AA004 法規名稱 refkey
AB005 編章節(編、章、節、款、目)
AB006 父親sno 
```

## LAWAC

```text
===================================
LAWAC 條文-單身
===================================
AC001 SELF ID PK KEY
AC002 AA001 ID refkey
AC003 AA002 代號(pcode) refkey 
AC004 AB003 ID sno 
AC005 SELF ID(flno) 
AC006 法規名稱 AA004 法規名稱 refkey
AC007 AA007	最新異動日期
AC008 AA010	廢止註記 
AC009 AB005 編章節(編、章、節、款、目)    refkey
AC010 條號
AC011 條文內容
```
