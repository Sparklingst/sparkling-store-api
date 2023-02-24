import json
import os
import platform
import shutil

NOW_SYSTEM = platform.system()
TAG_INFO = "\033[0;37m[INFO]\033[0m"
TAG_ERROR = "\033[0;31m[ERROR]\033[0m"


def cls():
    '''
    清屏
    '''
    os.system("cls" if NOW_SYSTEM == "Windows" else "clear")


def print_menu():
    '''
    打印主菜单
    '''
    print("欢迎使用粼光商店管理系统")
    print("请选择您的操作")
    print(" 1. 查看所有应用")
    print(" 2. 上传/更新应用")
    print(" 3. 删除应用")
    print(" 4. 构建API")
    print(" 0. 退出程序")


def print_all_apps():
    '''
    打印所有APP
    '''
    cls()
    apps_dir_path = "apps"
    packages_list = os.listdir(apps_dir_path)
    index = -1
    print("序号", "\t", "名称", "\t", "包名", "\t", "平台")
    for package_name in packages_list:
        index += 1
        path = os.path.join(apps_dir_path, package_name)
        try:
            with open(path + '/index.json', encoding='utf-8') as index_file:
                index_content = json.load(index_file)
        except Exception as e:
            print(index, "\t", "\033[0;31m打开文件失败", e, "\033[0m")
            continue
        # 打印名称
        print(index, "\t", index_content.get("name"), "\t", package_name, "\t",
              index_content.get("platforms"))
    input("按任意键继续")


def update_app_input_package_name():
    '''
    更新应用的输入包名
    '''
    package_name = input("请输入包名，0为返回：")
    if not package_name:
        print("输入错误，请重新输入")
        input("按任意键继续")
        return False, None
    if package_name == "0":
        return False, "exit"

    app_cfg_path = "apps/"+package_name
    index_path = app_cfg_path + '/index.json'
    index_content = {}
    app_name = None
    platforms = []
    summary = None
    icon = "icon.svg"

    if os.path.isfile(index_path):
        print("应用已存在，您正在更新应用")
        with open(index_path, encoding="utf-8") as index_file:
            index_content = json.load(index_file)
        app_name = index_content.get("name")
        platforms = index_content.get("platforms")
        summary = index_content.get("summary")
        print("应用名：", "\t", app_name)
        print("平台：", "\t", platforms)
    else:
        print("应用不存在，您正在新建应用")

    app_name = input(f"应用名 ({app_name})：") or app_name
    summary = input(f"应用介绍 ({summary})：") or summary
    icon = input(f"图标 ({icon})：") or icon
    platforms = input(f"平台 (使用\", \"分割) ({platforms})：").split(
        ",") or platforms
    index_content["name"] = app_name
    index_content["summary"] = summary
    index_content["icon"] = icon
    index_content["platforms"] = platforms
    if not os.path.isfile(index_path):
        os.makedirs(app_cfg_path)
    index_content_str = json.dumps(index_content)
    print("index.json:", "\n", index_content_str)
    with open(index_path, "w", encoding="utf-8") as index_file:
        index_file.write(index_content_str)
    print("应用 index.json 更新完成")
    return True, index_content


def update_app():
    '''
    上传/更新应用
    '''
    while True:
        cls()
        print("上传/更新应用")
        input_package_state, index_content = update_app_input_package_name()
        if input_package_state is False:
            if index_content == "exit":
                break
            continue
        app_platform = input(
            "请输入要编辑的应用平台（android, windows, pwa），默认为 android，0为返回：") or "android"
        if app_platform == "0":
            continue
        app_name = index_content.get("name")
        app_name = input(f"应用名：({app_name})") or app_name


def build_api():
    output_dir_path = "build"
    output_apps_dir_path = output_dir_path+"/apps"
    apps_dir_path = "apps"
    shutil.rmtree(output_dir_path)
    packages_list = os.listdir(apps_dir_path)
    for package_name in packages_list:
        print(TAG_INFO, "正在构建", package_name)
        app_cfg_path = os.path.join(apps_dir_path, package_name)
        index_path = app_cfg_path + '/index.json'
        try:
            with open(index_path, encoding='utf-8') as index_file:
                index_content = json.load(index_file)
        except Exception as e:
            print(TAG_ERROR, package_name, "\t", "打开文件失败", e)
            continue
        os.makedirs(f"{output_apps_dir_path}/{package_name}")

        for app_platform_file_name in os.listdir(app_cfg_path):
            app_platform_file_path = os.path.join(
                app_cfg_path, app_platform_file_name)
            if os.path.isfile(app_platform_file_path) and app_platform_file_path.endswith(".json") and app_platform_file_path != "index.json":
                try:
                    with open(app_platform_file_path, encoding='utf-8') as app_platform_file:
                        app_platform_file_content = json.load(
                            app_platform_file)
                except Exception as e:
                    print(TAG_ERROR, package_name, "\t", "打开文件失败", e)
                    continue
                app_platform_file_content["platforms"] = index_content.get(
                    "platforms")
                with open(f"{output_apps_dir_path}/{package_name}/{app_platform_file_name}", "w",
                          encoding="utf-8") as app_platform_file:
                    app_platform_file.write(
                        json.dumps(app_platform_file_content))
            elif os.path.isfile(app_platform_file_path):
                shutil.copy(
                    app_platform_file_path, f"{output_apps_dir_path}/{package_name}/{app_platform_file_name}")
            else:
                shutil.copytree(
                    app_platform_file_path, f"{output_apps_dir_path}/{package_name}/{app_platform_file_name}")
    input("按任意键继续")


while True:
    cls()
    print_menu()
    selection = input("请输入选项：")
    try:
        selection = int(selection)
        if selection is None:
            print("输入错误，请重新输入")
            input("按任意键继续")
            continue
    except Exception:
        print("输入错误，请输入正整数:")
        input("按任意键继续")
        continue
    # cls()
    if selection == 0:
        break
    elif selection == 1:
        print_all_apps()
    elif selection == 2:
        update_app()
    elif selection == 4:
        build_api()
    else:
        print("输入错误，请重新输入")
        input("按任意键继续")

    # input("按任意键继续")

cls()
print("再见！")
