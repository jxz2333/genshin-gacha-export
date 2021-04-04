import time
import traceback
import requests
import json
from Params import Params
from ReadLogs import ReadLogs


api_getGachaLog = "https://hk4e-api.mihoyo.com/event/gacha_info/api/getGachaLog"
api_getConfigList = "https://hk4e-api.mihoyo.com/event/gacha_info/api/getConfigList"
url = ReadLogs.get_url_cn()

# 国际服
# api_getGachaLog = "https://hk4e-api-os.mihoyo.com/event/gacha_info/api/getGachaLog"
# api_getConfigList = "https://hk4e-api-os.mihoyo.com/event/gacha_info/api/getConfigList"
# url = ReadLogs.get_url_global()

try:
    if url == "":
        raise Exception()
    r = requests.get(api_getGachaLog, params=Params(url).get())
    j = r.json()
    if j["retcode"] != 0:
        raise Exception(j["message"])
except Exception as e:
    traceback.print_exc()
    print(e)
    input("任意键退出...")
    exit()

gacha_type_list = []
try:
    r = requests.get(api_getConfigList, params=Params(url).get())
    j = r.json()
    if j["retcode"] != 0:
        print(j["message"])
    else:
        gacha_type_list = j["data"]["gacha_type_list"]
except Exception as e:
    traceback.print_exc()
    print(e)
    input("任意键退出...")
    exit()

# print(gacha_type_list)
gacha_type_ids = [banner["key"] for banner in gacha_type_list]
gacha_type_names = [banner["name"] for banner in gacha_type_list]
gacha_type_dict = dict(zip(gacha_type_ids, gacha_type_names))


gachaData = {}
gachaData["uid"] = ""
gachaData["gachaType"] = gacha_type_list
for gacha_type in gacha_type_ids:
    gachaData["gachaLog"] = {}
    gachaData["gachaLog"][gacha_type] = []
    MAX_PAGES = 10000
    page = 0
    end_id = ""
    while page < MAX_PAGES:
        page += 1
        print(f"正在获取 {gacha_type_dict[gacha_type]} 第 {page} 页", flush=True)
        params = Params(url).size(20).page(page).gacha_type(gacha_type).end_id(end_id).get()
        req = requests.get(api_getGachaLog, params=params).json()
        if req["retcode"] == 0:
            data_list = req["data"]["list"]
            if data_list != []:
                end_id = data_list[-1]["id"]
                gachaData["uid"] = data_list[-1]["uid"]
                gachaData["gachaLog"][gacha_type].extend(data_list)
            else:
                break
        else:
            print(req["message"])
            break

uid = gachaData["uid"]
t = time.strftime("%Y%m%d%H%M%S", time.localtime())
with open(f"gacha_data_uid{uid}_{t}.json", "w", encoding="utf-8") as f:
    json.dump(gachaData, f, ensure_ascii=False, sort_keys=False, indent=4)
