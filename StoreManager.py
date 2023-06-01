import io
import json
import os
import random
import shutil

URL_BASE = ""
URL_ALL_PAGE = f"{URL_BASE}/all/%s.json"
URL_PROJECTS = f"{URL_BASE}/projects"
URL_PRJ = f"{URL_PROJECTS}/%s"
URL_PRJ_INFO = f"{URL_PROJECTS}/%s/index.json"
URL_APP = f"{URL_PROJECTS}/{'{project}'}/{'{platform}'}"
URL_APP_INFO = f"{URL_APP}/{'{category}'}.json"

PATH_BASE = "."
PATH_PUBLIC = f"{PATH_BASE}/public".replace("/", os.sep)
PATH_PROJECTS = f"{PATH_BASE}/projects".replace("/", os.sep)
PATH_PRJ = f"{PATH_BASE}/projects/%s".replace("/", os.sep)
PATH_DIST = f"{PATH_BASE}/dist".replace("/", os.sep)
PATH_DIST_ALL_PAGE = f"{PATH_DIST}/{URL_ALL_PAGE}".replace("/", os.sep)
PATH_DIST_PROJECTS = f"{PATH_DIST}/{URL_PROJECTS}".replace("/", os.sep)
PATH_DIST_PRJ = f"{PATH_DIST}/{URL_PRJ}".replace("/", os.sep)
PATH_DIST_PRJ_INFO = f"{PATH_DIST}/{URL_PRJ_INFO}".replace("/", os.sep)
PATH_DIST_APP = f"{PATH_DIST}/{URL_APP}".replace("/", os.sep)
PATH_DIST_APP_INFO = f"{PATH_DIST}/{URL_APP_INFO}".replace("/", os.sep)
PATH_DIST_SORTS = f"{PATH_DIST}/sorts".replace("/", os.sep)
PATH_DIST_SORTS_INFO = f"{PATH_DIST_SORTS}/index.json".replace("/", os.sep)
PATH_DIST_SORTS_FULL = f"{PATH_DIST_SORTS}/{'{sort}'}/{'{page}'}.json".replace("/", os.sep)

INT_MAX_ITEMS = 20  # 每页最多项目


class ProjectInfo(dict):

    @staticmethod
    def from_file(prj_id: str):
        path = f"{PATH_PROJECTS}/{prj_id}/index.json"
        with open(path, encoding='utf-8') as file:
            content = ProjectInfo(prj_id, json.load(file))
            return content

    def __init__(self, prj_id: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.info_list_map = None
        self.__prj_id = prj_id

    def get_platforms(self):
        return self.get("platforms", {})

    def get_prj_id(self):
        return self.__prj_id

    def get_platform_info_list_map(self):
        if self.info_list_map is not None:
            return self.info_list_map
        info_list_map = {}
        self.info_list_map = info_list_map
        platforms = self.get_platforms()
        category_list: list
        for platform, category_list in platforms.items():
            info_list = []
            info_list_map[platform] = info_list
            for category in category_list:
                info_list.append(ApplicationInfo.from_file(self, platform, category))
        return info_list_map

    def get_name(self):
        return self.get("name")

    def get_icon_url(self):
        return self.get("iconUrl")

    def get_type(self):
        return self.get("type")

    def export(self):
        base_url = URL_PRJ % self.get_prj_id()
        copied = self.copy()
        copied["iconUrl"] = merge_url(copied.get("iconUrl", "icon.png"), base_url)

        screenshots = copied.get("screenshots", [])
        for index in range(0, len(screenshots)):
            print(index)

        # copied["screenshots"] = os.path.join(origin_dir, copied.get("screenshot", )).replace("\\", "/")
        copied["prjId"] = self.__prj_id
        return copied


class ApplicationInfo(dict):

    @staticmethod
    def from_file(prj_info: ProjectInfo, platform: str, category: str):
        prj_id = prj_info.get_prj_id()
        path = f"{PATH_PROJECTS}/{prj_id}/{platform}/{category}.json"
        with open(path, encoding='utf-8') as file:
            content = ApplicationInfo(prj_info, platform, category, json.load(file))
            return content

    def __init__(self, prj_info: ProjectInfo, platform: str, category: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__prj_info = prj_info
        self.__platform = platform
        self.__category = category

    def get_category(self):
        return self.__category

    def get_project_info(self):
        return self.__prj_info

    def get_name(self):
        return self.get("name", self.__prj_info.get_name())

    def get_icon_url(self):
        return self.get("name", self.__prj_info.get_icon_url())

    def get_prj_id(self):
        return self.get_project_info().get_prj_id()

    def get_type(self):
        return self.get("type", self.__prj_info.get_type())

    def export(self) -> dict:
        base_url = URL_APP.format(project=self.get_prj_id(), platform=self.__platform)
        copied = self.copy()
        copied["iconUrl"] = merge_url(copied.get("iconUrl", "icon.png"), base_url)
        copied["prjId"] = self.get_prj_id()
        copied["platform"] = self.__platform
        copied["category"] = self.__category
        screenshots = copied.get("screenshots", [])

        for index in range(len(screenshots)):
            item = screenshots[index]
            if type(item) == str:
                screenshots[index] = merge_url(item, base_url)
        copied["screenshots"] = screenshots
        merge_table(self.__prj_info.export(), copied)

        return copied


def get_store_config() -> dict:
    path = f"{PATH_BASE}/storeConfig.json"
    with open(path, encoding='utf-8') as file:
        content = json.load(file)
        return content


def get_sorts() -> dict:
    path = f"{PATH_BASE}/sorts.json"
    with open(path, encoding='utf-8') as file:
        content = json.load(file)
        return content


# def get_project_info(prj_id: str) -> ProjectInfo:
#     return ProjectInfo.from_file(prj_id)


# def get_application_info(prj_info: ProjectInfo, platform: str, category: str):
#     return ApplicationInfo.from_file(prj_info, platform, category)


# def get_info_with_fallback(prj_info: dict, app_info: dict, key):
#     return app_info.get(key, prj_info.get(key))


def get_similar_projects(prj_id: str):
    """
    获取相似项目
    @param prj_id: 项目ID
    """
    ...


def merge_url(url: str, base: str) -> str:
    url = os.path.join(base, url).replace("\\", "/")
    return url


def merge_table(src, dst):  # python3.8不支持类型标注
    if type(dst) == list and type(src) == list:
        for index in range(len(src)):
            value = src[index]
            dst_value = dst[index]
            if value is None:
                dst[index] = value
            elif type(dst_value) == dict or type(dst_value) == list:
                merge_table(value, dst_value)
    elif type(dst) == dict and type(src) == dict:
        for key, value in src.items():
            dst_value = dst.get(key)
            if dst_value is None:
                dst[key] = value
            elif type(dst_value) == dict or type(dst_value) == list:
                merge_table(value, dst_value)
    return dst


def save_project_info():
    ...


def get_projects() -> list:
    """
    获取所有项目ID
    """
    return os.listdir(PATH_PROJECTS)


def get_path(now_file_path: str, new_file_path: str):
    if new_file_path[0] == "/":
        return new_file_path
    elif now_file_path[-1] == "/":
        return now_file_path + new_file_path
    else:
        return os.path.join(os.path.dirname(now_file_path), new_file_path)


def build_copy_public():
    for root, dirs, files in os.walk(PATH_PUBLIC):
        dist_root = PATH_DIST + root[len(PATH_PUBLIC):] if PATH_PUBLIC != root else PATH_DIST
        for file in files:
            path = os.path.join(root, file)
            dist_path = os.path.join(dist_root, file)
            if not os.path.isdir(dist_root):
                os.mkdir(dist_root)
            print("正在复制公共文件", path, "到", dist_path)
            shutil.copy(path, dist_path)


def build_project(prj_info: ProjectInfo):
    prj_id = prj_info.get_prj_id()
    prj_info_dict = prj_info.export()
    origin_dir = PATH_PRJ % prj_id
    for root, dirs, files in os.walk(origin_dir):
        dist_root = PATH_DIST_PROJECTS + root[len(PATH_PROJECTS):] if PATH_PROJECTS != root else PATH_DIST_PROJECTS
        if not os.path.exists(dist_root):
            os.makedirs(dist_root)
        for file_name in files:
            path = os.path.join(root, file_name)
            dist_path = os.path.join(dist_root, file_name)
            shutil.copy(path, dist_path)

        # print(root, dist_root)
    prj_info_path = PATH_DIST_PRJ_INFO % prj_id
    with open(prj_info_path, "w", encoding='utf-8') as file:
        file.write(json.dumps(pack_data(prj_info_dict)))
    platform_info_list_map = prj_info.get_platform_info_list_map()
    for platform, platform_info_list in platform_info_list_map.items():
        for platform_info in platform_info_list:
            platform_info_dict = platform_info.export()
            platform_info_path = PATH_DIST_APP_INFO.format(project=prj_id, platform=platform,
                                                           category=platform_info.get_category())
            with open(platform_info_path, "w", encoding='utf-8') as file:
                file.write(json.dumps(pack_data(platform_info_dict)))


def split_to_page(item_list: list) -> list:
    new_list = []
    now_list = None
    for index in range(len(item_list)):
        if index % INT_MAX_ITEMS == 0:
            now_list = []
            new_list.append(now_list)
        now_list.append(item_list[index])
    if len(new_list) == 0:
        new_list.append([])
    return new_list


def pack_data(data):
    return {
        "name": "欢迎使用粼光商店API",
        "state": 200,
        "data": data,
    }


def build_apps(project_info_list: list):
    project_info_list = project_info_list.copy()
    random.shuffle(project_info_list)
    store_config = get_store_config()
    basic_info_list = store_config.get("basicInfoList")
    sorts = get_sorts()
    sorts_map = {}

    for item in sorts:
        item: dict
        if item.get("key") is not None:
            sorts_map[item.get("key")] = item
            item["prjIdList"] = []

    for item in project_info_list:
        item: ProjectInfo
        _type = item.get_type()
        if _type is None:
            return
        basic_info = {}
        sorts_map[_type]["prjIdList"].append(basic_info)
        item_exported = item.export()
        for key in basic_info_list:
            basic_info[key] = item_exported.get(key)
    sorts_index = []
    for item in sorts:
        prj_list_len = len(item["prjIdList"])
        item["length"] = prj_list_len
        split = split_to_page(item["prjIdList"])
        item["maxPages"] = len(split)
        for page in range(len(split)):
            now_page_item = item.copy()
            now_page_item["prjIdList"] = split[page]
            path = PATH_DIST_SORTS_FULL.format(sort=item["key"], page=page)
            os.makedirs(os.path.dirname(path))
            with open(path, "w", encoding='utf-8') as file:
                file.write(json.dumps(pack_data(now_page_item)))

        # 构建概览
        first_page_item = item.copy()
        first_page_item["prjIdList"] = split[0]
        sorts_index.append(first_page_item)
    with open(PATH_DIST_SORTS_INFO, "w", encoding='utf-8') as file:
        file.write(json.dumps(pack_data(sorts_index)))
        # print(path)
        # print(now_page_item)

    # print(sorts_map)


def build_api():
    if os.path.isdir(PATH_DIST):
        shutil.rmtree(PATH_DIST)
    if os.path.isfile(PATH_DIST):
        os.remove(PATH_DIST)
    os.mkdir(PATH_DIST)
    build_copy_public()
    projects = get_projects()
    project_info_list = []  # 所有项目的信息
    for prj_id in projects:
        prj_info = ProjectInfo.from_file(prj_id)
        project_info_list.append(prj_info)
        build_project(prj_info)
    build_apps(project_info_list)


def main():
    build_api()
    # print("所有项目")
    # print("名称", "\t", "图标")
    # for prj_id in get_projects():
    #     prj_info = get_project_info(prj_id)
    #     print(prj_info.get("name"), "\t", prj_info.get("iconUrl"))
    #     print(prj_info.get_platforms())
    # print(merge_info(prj_info))
    # print(info)
    # print(get_projects())


if __name__ == '__main__':
    main()
