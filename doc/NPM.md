# NPM

`NPM`



## Package json 是什麼?

NPM 是一個 package manager，當專案什麼都沒有的時候，會需要我們輸入 `npm init` 來把專案初始化，填入相關資訊後，未來所有相關的配置檔都會存在 `package.json` 中

- dependencies: 執行環境會需要
- devDependencies: 開發或測試環境需要
- optionalDependencies: 不一定在每個環境都能夠裝起來



## npm 安裝 node_module 的語法

用最常用的 lodash 舉例，列出幾種指令與結果說明

| 指令                             | node_modules | `package.json` 說明                 |
| :------------------------------- | :----------- | :---------------------------------- |
| `npm install lodash;`            | 專案環境     | 僅安裝最新版本                      |
| `npm install lodash -g;`         | **全域環境** | 僅安裝最新版本                      |
| `npm install lodash@4.17.4`      | 專案環境     | 僅安裝**指定版本**                  |
| `npm install lodash --save;`     | 專案環境     | 安裝並加入 **dependencies**         |
| `npm install lodash --save-dev;` | 專案環境     | 安裝並加入 **devDependencies**      |
| `npm install lodash -O;`         | 專案環境     | 安裝並加入 **optionalDependencies** |

透過以下指令可以針對 `package.json` 做部分安裝 ，熟悉這些指令在未來我們需要控制 Docker Image 的大小、縮短 CI/CD 的時間上會有很大的幫助。

| 指令                         | 說明                             |
| :--------------------------- | :------------------------------- |
| `npm install --no-optional;` | 不安裝 optionalDependencies      |
| `npm install --production`   | 執行環境，不安裝 devDependencies |



## node_module 版本號碼

node_module 版號通常會有三位數字 `1.2.3` 對應到 `主版號.次版號.修訂號`

> [版號遞增規則如下](https://semver.org/lang/zh-TW/)：
>
> - 主版號：當你做了不相容的 API 修改
> - 次版號：當你做了向下相容的功能性新增
> - 修訂號：當你做了向下相容的問題修正
>
> 先行版號及版本編譯資訊可以加到「主版號.次版號.修訂號」的後面，作為延伸。



安裝特定版號的方法，可以去 [npm 官方提供的計算機](https://semver.npmjs.com/)試用看看

- 主版號 releases: * or x
- 次版號 releases: 1 or 1.x or ^1.0.4
- 修訂號 releases: 1.0 or 1.0.x or ~1.0.4



## npm 維護 node_module 的語法

| 指令            | 說明                                 |
| :-------------- | :----------------------------------- |
| `npm audit`     | 查看是否 node_modules 有相關資安漏洞 |
| `npm audit fix` | 自動修正相關漏洞                     |
| `npm update`    | 更新可更新的 node_modules            |
| `npm prune`     | 清理 node_modules 中不需要的檔案     |





## 參考網站

[npm 入門到進階](https://linyencheng.github.io/2020/03/22/tool-npm/)

