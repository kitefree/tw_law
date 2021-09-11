# MYSQL

## [自關聯表遞迴查詢所有子節點[MySQL]](https://www.gushiciku.cn/pl/gJ2I/zh-tw)

```
CREATE TABLE `menu` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '選單id',
  `parent_id` int(11) DEFAULT NULL COMMENT '父節點id',
  `menu_name` varchar(128) DEFAULT NULL COMMENT '選單名稱',
  `menu_url` varchar(128) DEFAULT '' COMMENT '選單路徑',
  `status` tinyint(3) DEFAULT '1' COMMENT '選單狀態 1-有效；0-無效',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12212 DEFAULT CHARSET=utf8;
```

插入資料：



```
INSERT INTO `menu` VALUES ('0', null, '選單0', ' ', '1');
INSERT INTO `menu` VALUES ('1', '0', '選單1', '', '1');
INSERT INTO `menu` VALUES ('11', '1', '選單11', '', '1');
INSERT INTO `menu` VALUES ('12', '1', '選單12', '', '1');
INSERT INTO `menu` VALUES ('13', '1', '選單13', '', '1');
INSERT INTO `menu` VALUES ('111', '11', '選單111', '', '1');
INSERT INTO `menu` VALUES ('121', '12', '選單121', '', '1');
INSERT INTO `menu` VALUES ('122', '12', '選單122', '', '1');
INSERT INTO `menu` VALUES ('1221', '122', '選單1221', '', '1');
INSERT INTO `menu` VALUES ('1222', '122', '選單1222', '', '1');
INSERT INTO `menu` VALUES ('12211', '1222', '選單12211', '', '1');
```

 得到的目錄結構如下圖所示：

**![img](https://images2017.cnblogs.com/blog/837877/201712/837877-20171219135203365-504537466.png)**

 

**查詢**                                                      

 先貼出sql語句：

```
SELECT
    *
FROM
    menu
WHERE
    id IN (
        SELECT
            id
        FROM
            (
                SELECT
                    t1.id,

                IF (
                    find_in_set(parent_id, @pids) > 0,
                    @pids := concat(@pids, ',', id),
                    0
                ) AS ischild
                FROM
                    (
                        SELECT
                            id,
                            parent_id
                        FROM
                            menu t
                        WHERE
                            t. STATUS = 1
                        ORDER BY
                            parent_id,
                            id
                    ) t1,
                    (SELECT @pids := 12) t2
            ) t3
        WHERE
            ischild != 0
    )
```

![img](https://i.imgur.com/csycWh6.png)





## [遞迴查詢](https://iter01.com/519765.html)



### `向下遞迴`函式

```MYSQL
DELIMITER $$
CREATE DEFINER=`root`@`localhost` FUNCTION `get_child_list_ab`(in_id varchar(10),p_ab002 varchar(50)) RETURNS varchar(1000) CHARSET utf8mb4 COLLATE utf8mb4_bin
begin 
	declare ids varchar(1000) default ''; 
	declare tempids varchar(1000); 
 
	set tempids = in_id; 
	while tempids is not null do 
		set ids = CONCAT_WS(',',ids,tempids); 
		select GROUP_CONCAT(AB003) into tempids from LAWAB where ab002 = p_ab002 and FIND_IN_SET(AB006,tempids)>0;  
	end while; 
	return ids; 
end$$
DELIMITER ;
```

#### 查詢

```mysql
select * from lawab where AB002='B0000001' and FIND_IN_SET(AB003,get_child_list_ab('20','B0000001'))
```



### `向上遞迴`函式

```MYSQL
DELIMITER $$
CREATE DEFINER=`root`@`localhost` FUNCTION `get_parent_list_ab`(in_id varchar(10),p_ab002 varchar(50)) RETURNS varchar(1000) CHARSET utf8mb4 COLLATE utf8mb4_bin
begin 
	declare ids varchar(1000); 
	declare tempid varchar(10); 
	 
	set tempid = in_id; 
	while tempid is not null do 
		set ids = CONCAT_WS(',',ids,tempid); 
		select AB006 into tempid from LAWAB where ab002 = p_ab002 and AB003=tempid; 
	end while; 
	return ids; 
end$$
DELIMITER ;
```



#### 查詢

```MYSQL
      SELECT '' AS AA003,'' AS AA004
      ,AB002,AB003
      ,AB005
      ,'0' AS AC005
      ,'' AS AC010
      ,'' AS AC011
      FROM LAWAB 
      WHERE AB002='B0000001' AND FIND_IN_SET(AB003,get_parent_list_ab('20','B0000001'))
```





## 參考連結

- 待整理

  - [MySQL遞回CTE簡介](https://www.tw511.com/25/12420.html)
  - [同事問我MySQL怎麼遞迴查詢，我懵逼了](https://iter01.com/519765.html)

  - [岳仔](https://hackmd.io/@cw110you/B17iG5zxF)

