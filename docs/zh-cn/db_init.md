
# DB Init

## Table

### LAWAA

```sql
--
-- 資料表結構 `lawaa`
--

CREATE TABLE `lawaa` (
  `AA001` int(11) NOT NULL COMMENT 'SELF ID',
  `AA002` char(50) NOT NULL COMMENT 'pcode',
  `AA003` char(255) NOT NULL COMMENT '法規性質',
  `AA004` char(150) NOT NULL COMMENT '法規名稱',
  `AA005` char(255) NOT NULL COMMENT '法規網址',
  `AA006` char(255) NOT NULL COMMENT '法規類別',
  `AA007` char(255) NOT NULL COMMENT '最新異動日期',
  `AA008` char(255) NOT NULL COMMENT '生效日期',
  `AA009` text NOT NULL COMMENT '生效內容',
  `AA010` char(255) NOT NULL COMMENT '廢止註記',
  `AA011` char(255) NOT NULL COMMENT '是否英譯註記',
  `AA012` text NOT NULL COMMENT '英文法規名稱',
  `AA013` text NOT NULL COMMENT '沿革內容',
  `AA014` char(255) NOT NULL COMMENT '前言',
  `AA015` char(255) NOT NULL COMMENT '法規內容',
  `AA016` char(255) NOT NULL COMMENT '附件'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `lawaa`
--
ALTER TABLE `lawaa`
  ADD PRIMARY KEY (`AA001`),
  ADD KEY `idx_AA002` (`AA002`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `lawaa`
--
ALTER TABLE `lawaa`
  MODIFY `AA001` int(11) NOT NULL AUTO_INCREMENT COMMENT 'SELF ID', AUTO_INCREMENT=1;
COMMIT;
```

### LAWAB

```sql
--
-- 資料表結構 `lawab`
--

CREATE TABLE `lawab` (
  `AB001` int(11) NOT NULL COMMENT 'AA001 ID refkey',
  `AB002` char(50) NOT NULL COMMENT 'AA002 代號(pcode) refkey',
  `AB003` smallint(6) NOT NULL COMMENT 'SELF ID',
  `AB004` char(150) NOT NULL COMMENT 'AA004 法規名稱 refkey',
  `AB005` varchar(150) NOT NULL COMMENT '編章節',
  `AB006` smallint(6) DEFAULT NULL COMMENT 'parent ID'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `lawab`
--
ALTER TABLE `lawab`
  ADD PRIMARY KEY (`AB001`,`AB002`,`AB003`) USING BTREE,
  ADD KEY `idx_AB002` (`AB002`) USING BTREE;
COMMIT;
```

### LAWAC

```sql
CREATE TABLE `lawac` (
  `AC001` int(11) NOT NULL,
  `AC002` int(11) NOT NULL COMMENT 'AA001 ID refkey',
  `AC003` char(50) NOT NULL COMMENT 'AA002 代號(pcode) refkey',
  `AC004` smallint(6) DEFAULT NULL COMMENT 'AB003 ID refkey ',
  `AC005` char(5) NOT NULL COMMENT 'SELF ID flno',
  `AC006` char(150) NOT NULL COMMENT 'AA004 法規名稱 refkey',
  `AC007` char(255) NOT NULL COMMENT '最新異動日期',
  `AC008` char(255) NOT NULL COMMENT '廢止註記',
  `AC009` varchar(150) NOT NULL COMMENT '編章節',
  `AC010` varchar(20) NOT NULL COMMENT '條號',
  `AC011` text NOT NULL COMMENT '條文內容'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 資料表索引 `lawac`
--
ALTER TABLE `lawac`
  ADD PRIMARY KEY (`AC001`),
  ADD KEY `idx_AC003` (`AC003`);
ALTER TABLE `lawac` ADD FULLTEXT KEY `fulltext_AC008` (`AC008`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `lawac`
--
ALTER TABLE `lawac`
  MODIFY `AC001` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
COMMIT;
```

## Function

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
