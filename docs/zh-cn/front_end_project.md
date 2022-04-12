# 二、前端專案

前端使用的是`vuejs`  +`bootstrap-vue` 套件開發而成的。

## 1. 程式資料夾

```sh
tw_law\law_fe
```

## 2. 環境安裝

請在`law_fe`資料夾底下執行

### 1. 安裝nodejs套件

```sh
sudo apt install nodejs
```

### 2. 安裝npm套件

```sh
sudo apt install npm
```

### 3. 安裝專案所有套件

```sh
npm i
```

### 4. 修正套件

```sh
npm audit fix
```

### 5. 安裝 vue cli

```sh
sudo npm install -g @vue/cli
```

### 6. rebuild 安裝 (for linux)

```sh
npm rebuild node-sass
```

### 7. 運行伺服器

```sh
npm run serve
```

![image-20220125134736095](../images/image-20220125134736095.png)

### 8. build 程式碼

```sh
npm run build
```

下完此指令之後，會生產相關靜態程式碼於`dist`資料夾底下

## 3. law_fe程式、架構

| 序號 | 程式名稱            | 說明                                                         |
| ---- | ------------------- | ------------------------------------------------------------ |
| 1    | dist                | npm run build 指令後的output資料夾，之後要用這個資料夾的程式跟後端程式碼合併佈署 |
| 2    | src/api/config.js   | 設定後端api url path                                         |
| 3    | src/router/index.js | 設定路由                                                     |
| 4    | src/views           | 撰寫vue 程式碼                                               |
| 5    | src/main.js         | vue 路口,引用相關套件                                        |

`config.js` 請修改正確的server ip

```js
const baseURL = 'http://192.168.152.140/law/'
```
