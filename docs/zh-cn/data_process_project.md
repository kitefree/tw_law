# 一、資料轉換專案

## 1. 程式資料夾

```shell
tw_law\data_process
```

## 2. 環境安裝

確認python版本

```shell
python3 --version
```

安裝python

```sh
sudo apt-get update
sudo apt-get install python3.6
sudo apt install python3-pip
```

安裝套件

```shell
pip3 install pathlib
pip3 install mysql-connector
```

## 3. data_process程式、架構

| 序號 | 程式名稱         | 說明                                                         |
| ---- | ---------------- | ------------------------------------------------------------ |
| 1    | auto_run01.py      | 依據XML資料產生SQL檔案                                                       |
| 2    | auto_run02.py      | 匯入SQL檔，更新父子節點資料 |
| 3    | config.py        | 相關全域變數設定檔                                           |
| 4    | input_file資料夾     | 放置download法規的xml檔                                      |
| 5    | output_file資料夾      | 放置 output sql 檔                                           |
| 6    | LAWAA_Model.py   | LAWAA 資料表 model ，for main01_LAWAA.py 、main02_LAWAA.py 使用 |
| 7    | LAWAB_Model.py   | LAWAB 資料表 model，for main01_LAWAB.py 、main02_LAWAB.py 使用 |
| 8    | LAWAC_Model.py   | LAWAC 資料表 model，for main01_LAWAC.py 、main02_LAWAC.py 使用 |
| 9    | main01_LAWAA.py  | 執行讀取法規_法律xml，產出LAWAA SQL 放置於output_file，於auto_run01.py中執行        |
| 10   | main01_LAWAB.py  | 執行讀取法規_法律xml，產出LAWAB SQL 放置於output_file，於auto_run01.py中執行        |
| 11   | main01_LAWAC.py  | 執行讀取法規_法律xml，產出LAWAC SQL 放置於output_file，於auto_run01.py中執行        |
| 12   | main02_LAWAA.py  | 執行讀取法規_命令xml，產出LAWAA SQL 放置於output_file，於auto_run01.py中執行        |
| 13   | main02_LAWAB.py  | 執行讀取法規_命令xml，產出LAWAB SQL 放置於output_file，於auto_run01.py中執行        |
| 14   | main02_LAWAC.py  | 執行讀取法規_命令xml，產出LAWAC SQL 放置於output_file，於auto_run01.py中執行        |
| 15   | import_sql.py    | 匯入sql檔至資料庫，於auto_run02.py中執行|
| 16   | update_parent.py | 更新父子節點資料，於auto_run02.py中執行     |

## 4. 步驟順序

### 1. 下載法規、命令資料(XML格式)

請參考`法規資料下載`

### 2. 建立資料夾

請在 `data_process\input_file`資料夾底下放置下載資料，以資料夾為命名原則。

```sh
input_file/
├── 20210819
│   ├── FalV.xml
│   └── MingLing.xml
└── 20220411
    ├── FalV.xml
    └── MingLing.xml

```

### 3. 修改config.py

修改`20220411`字串

```python
import pathlib
import os

CUR_DIR = str(pathlib.Path(__file__).parent.resolve())
INPUT_FILE_ROOT_PATH = 'input_file/20220411' #修改這行
OUTPUT_FILE_ROOT_PATH = 'output_file'

DB_ACCOUNT = 'tqe'
DB_PWD = '0000'
DB_NAME = 'law'
...
...
```

### 4. 執行auto_run01.py程式，產生SQL檔案

請在`data_process`資料夾底下執行：

```python
python3 auto_run01.py
```

### 5. 修改異常資料

到`data_process/output_file`資料夾底下打開 `main02_LAWAC_SQL.sql`檔案，搜尋`食品器具、容器、包裝應符合下列試驗標準`，將此項的內容清空，此筆資料在寫入資料庫會失敗。
因此項內容對於使用者來說並不重要，故可直接清空。清空此筆資料後，依序執行以下SQL(請注意資料庫帳號密碼、檔案路徑是否正確)。

### 6. 執行auto_run02.py程式，匯入資料至資料庫

```python
python3 auto_run02.py
```

