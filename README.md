# 粼光商店 API 测试

## 软件架构

* apps: 所有应用数据目录
  * xxxxxx: 应用数据目录
    * index.json: 应用展示在首页的信息
    * icon.svg: 矢量图标文件（可选）
    * icon.png: 位图图标文件（可选）
    * android.json: 安卓平台配置文件（可选）
    * pwa.json: 浏览器平台配置文件（可选）
    * windows.json: Windows平台配置文件（可选）
* build: 资源构建目录
  * apps: 所有应用数据目录，同 `apps`
* public：静态资源，一般存放图片、静态配置文件等资源

## 构建教程

1. 下载并安装 [Python](https://www.python.org/)
2. 运行

    ``` shell
    python Manager.py build
    ```

3. 将 `build` 文件夹复制到服务器内

## 使用说明

## 参与贡献

1. Fork 本仓库
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request
