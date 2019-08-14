import json
import requests
import urllib3
urllib3.disable_warnings()
# 改變x-tt-trace-id，X-Khronos，X-Gorgon
headers = {
    "Host": "aweme-eagle.snssdk.com",
    "Connection": "keep-alive",
    "x-Tt-Token": "006803e112fefc48cfcea99b36b01e68876719c09d00f283c95cc09230454abf8673bd403625d590373bf5d136273f152057",
    "sdk-version": "1",
    "User-Agent": "Aweme 7.4.0 rv:74023 (iPhone; iOS 13.0; zh_CN) Cronet",
    "x-tt-trace-id": "00-8b1379fa26d0554744dc626ee1c7bb0c-8b1379fa26d05547-01",
    "Accept-Encoding": "gzip, deflate",
    "X-Khronos": "1565577458",
    "X-Gorgon": "83000e560000c8f4636534ef71d41838968111d8804509608abe"
}
# 不變
cookies = {
    "odin_tt": "626d636e7243374772596e733579494747c49e7879e8da941404d0f79ca11f65053e03c8ea4ad802ee0d5887d4287115d35c02088f1d2b7a1db0fdf6e83daff7",
    "sid_guard": "6803e112fefc48cfcea99b36b01e6887%7C1563983617%7C5184000%7CSun%2C+22-Sep-2019+15%3A53%3A37+GMT",
    "uid_tt": "2461410cbe2088eed060939febdf05b9",
    "sid_tt": "6803e112fefc48cfcea99b36b01e6887",
    "sessionid": "6803e112fefc48cfcea99b36b01e6887",
    "install_id": "82093697106",
    "ttreq": "1$a84de7facbd40a968e5be61bde830b8a9e9c2365"
}
# 改變sec_user_id
url = "https://aweme-eagle.snssdk.com/aweme/v1/user/?version_code=7.4.0&pass-region=1&pass-route=1&js_sdk_version=1.17.4.3&app_name=aweme&vid=C186EE9D-862C-494D-851C-BE632E0A2963&app_version=7.4.0&device_id=58199959580&channel=App%20Store&mcc_mnc=46000&aid=1128&screen_width=750&openudid=d49bf43289e2b95ae6aafd2380d409a17584eb6f&os_api=18&ac=WIFI&os_version=13.0&device_platform=iphone&build_number=74023&device_type=iPhone10,1&iid=82093697106&idfa=5036E26C-5E7C-484C-AD5E-5818E8DC2956&user_id=80812090202&address_book_access=1&sec_user_id=MS4wLjABAAAA9yeV8IIJxpee3_u9zb_Al3_mOA8IffgD3_ueMCQUly4"
resp_json = requests.get(url=url, headers=headers, cookies=cookies, verify=False)
resp_json = resp_json.json()
print(json.dumps(resp_json, indent=4, ensure_ascii=False))
