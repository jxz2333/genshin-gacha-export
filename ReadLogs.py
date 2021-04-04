import os
import re
import traceback

class ReadLogs:
    @staticmethod
    def get(log_file_path):
        if not os.path.isfile(log_file_path):
            print("文件不存在")
            return ""
        try:
            with open(log_file_path) as f:
                text = f.read()
                searchObj = re.search(r"OnGetWebViewPageFinish:(.*?#/log)", text, re.M | re.I)
                if searchObj:
                    return searchObj.group(1)
                else:
                    print("请在游戏中查看一次祈愿记录后再试")
                    return ""
        except Exception:
            traceback.print_exc()
            return ""

    @classmethod
    def get_url_cn(cls):
        USERPROFILE = os.environ["USERPROFILE"]
        output_log_path_cn = os.path.join(USERPROFILE, "AppData", "LocalLow", "miHoYo", "原神", "output_log.txt")
        return cls.get(output_log_path_cn)

    @classmethod
    def get_url_global(cls):
        USERPROFILE = os.environ["USERPROFILE"]
        output_log_path_global = os.path.join(USERPROFILE, "AppData", "LocalLow", "miHoYo", "Genshin Impact", "output_log.txt")
        return cls.get(output_log_path_global)
