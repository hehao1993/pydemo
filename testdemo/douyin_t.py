import json
import requests
import urllib3
urllib3.disable_warnings()


# 改變x-tt-trace-id，X-Khronos，X-Gorgon
def get_header():
    h_str = """
        Host: aweme-eagle.snssdk.com
Connection: keep-alive
x-Tt-Token: 00cc1f0bb52b808bc49c8c9b61d7388faadd7b6313b4612838476935d902c7d0cd29f1d5d982d18d1ee19ebc82fabcd12d13
sdk-version: 1
User-Agent: Aweme 8.0.0 rv:80015 (iPhone; iOS 13.1; zh_CN) Cronet
x-tt-trace-id: 00-eb2dea1700150dcda32f070f6f6086a8-eb2dea1700150dcd-01
Accept-Encoding: gzip, deflate
Cookie: install_id=85759539441; ttreq=1$69bc1b5ecff87be6c498bd99f6a6fd5b2e13438d; sid_guard=cc1f0bb52b808bc49c8c9b61d7388faa%7C1568692905%7C5184000%7CSat%2C+16-Nov-2019+04%3A01%3A45+GMT; uid_tt=5b28e68f0f4409d3067dc8565756f9e9; sid_tt=cc1f0bb52b808bc49c8c9b61d7388faa; sessionid=cc1f0bb52b808bc49c8c9b61d7388faa; odin_tt=6a026017e88ed29ecd57a593eab7819f9ceda73dbc15d33049f67d6ee6d0abe19b0aff06015dc6f32f6bb353da1f7bea887b8cc4391e275afbdebb92ef4d8323
X-Khronos: 1568881111
X-Gorgon: 83000e560000493c4cab34ef714837de4f9411d88045c24b5775

    """
    r = h_str.split("\n")
    headers = {}
    for i in r:
        t = i.split(': ')
        if len(t) > 1:
            headers[t[0].strip()] = t[1]
    return headers

# 改變sec_user_id
# 98671398390
url = "https://aweme-eagle.snssdk.com/aweme/v1/user/?version_code=8.0.0&pass-region=1&pass-route=1&js_sdk_version=1.17.4.3&app_name=aweme&vid=C186EE9D-862C-494D-851C-BE632E0A2963&app_version=8.0.0&device_id=58199959580&channel=App%20Store&mcc_mnc=46000&aid=1128&screen_width=750&openudid=d49bf43289e2b95ae6aafd2380d409a17584eb6f&os_api=18&ac=WIFI&os_version=13.1&device_platform=iphone&build_number=80015&device_type=iPhone10,1&iid=85759539441&idfa=5036E26C-5E7C-484C-AD5E-5818E8DC2956&user_id=58664008125&address_book_access=1&sec_user_id=MS4wLjABAAAANIc0cmhrqIrapBy-9jcX8r295NcvSYX5QcFnSwKrh0M"
resp_json = requests.get(url=url, headers=get_header(), verify=False)
resp_json = resp_json.json()
print(json.dumps(resp_json, indent=4, ensure_ascii=False))
