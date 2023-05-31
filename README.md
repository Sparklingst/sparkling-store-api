# 粼光商店 API 测试

## 软件架构

* projects/: 所有应用数据目录
  * {prjId}/: 应用数据目录
    * index.json: 项目信息
    * icon.svg: 矢量图标文件
    * icon.png: 位图图标文件
    * android/: 安卓平台
      * main.json: 主版本
      * lite.json: Lite 版本
      * pro.json: Pro 版本
    * web
      * main.json: 主版本
      * lite.json: Lite 版本
      * pro.json: Pro 版本
    * windows
      * main.json: 主版本
      * lite.json: Lite 版本
      * pro.json: Pro 版本
* dist/: 资源构建目录
* public/：静态资源，一般存放图片、静态配置文件等资源
* storeConfig.json: 商店配置
* StoreManager.py: 商店管理器

## 资源链接

* projects/: 所有应用数据目录
  * {prjId}/: 应用数据目录
    * index.json: 项目信息
    * icon.svg: 矢量图标文件
    * icon.png: 位图图标文件
    * android/: 安卓平台
      * main.json: 主版本
      * lite.json: Lite 版本
      * pro.json: Pro 版本
    * web
      * main.json: 主版本
      * lite.json: Lite 版本
      * pro.json: Pro 版本
    * windows
      * main.json: 主版本
      * lite.json: Lite 版本
      * pro.json: Pro 版本



## 构建教程

1. 下载并安装 [Python](https://www.python.org/)
2. 运行 `python Manager.py build`
3. 将 `build` 文件夹复制到服务器内

## 使用说明

## 参与贡献

1. Fork 本仓库
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request
