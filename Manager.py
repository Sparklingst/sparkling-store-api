import StoreManager
import sys

if len(sys.argv) > 1:
    cmd = sys.argv[1]
    if cmd == "build":
        StoreManager.build_api()
        # build_api()
    elif cmd == "print":
        ...
        # print_all_apps()
    elif cmd == "update":
        ...
        # update_app()
else:
    ...
    # while True:
    #     cls()
    #     print_menu()
    #     selection = input("请输入选项：")
    #     try:
    #         selection = int(selection)
    #         if selection is None:
    #             print("输入错误，请重新输入")
    #             input("按任意键继续")
    #             continue
    #     except TypeError:
    #         print("输入错误，请输入正整数:")
    #         input("按任意键继续")
    #         continue
    #     cls()
    #     if selection == 0:
    #         break
    #     elif selection == 1:
    #         print_all_apps()
    #     elif selection == 2:
    #         update_app()
    #     elif selection == 4:
    #         build_api()
    #     else:
    #         print("输入错误，请重新输入")
    #
    #     input("按任意键继续")
    #
    # cls()
    # print("再见！")
    # main_ui()
