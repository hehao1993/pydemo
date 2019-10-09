import requests
import urllib3
urllib3.disable_warnings()

url = "https://api.weibo.cn/2/cardlist?gsid=_2A25wWMc9DeRxGeRJ4lAT8y3MzD-IHXVRTF31rDV6PUJbkdAKLW3WkWpNUiIZ6zc4c9vO_z2TjJwfA3_Hp9_qex9o&sensors_mark=0&wm=3333_2001&sensors_is_first_day=false&from=1097193010&b=0&c=iphone&networktype=wifi&skin=default&v_p=74&v_f=1&s=11111111&sensors_device_id=E3921745-9BA5-4CB7-996D-6A5A0DFA3134&lang=zh_CN&sflag=1&ua=iPhone10,1__weibo__9.7.1__iphone__os13.0&ft=11&aid=01AnoH-XQPXcgf94n2U-oWwlIKzv2zFT06OBInhNKInXXzy6g.&moduleID=pagecard&lcardid=more_web&orifid=100012792233073%24%241076036412562467%24%24231051_-_fans_-_6412562467%24%24231051_-_followerstagBigV_-_6412562467_-_1042015%3AtagCategory_019%24%242302835801768120&count=20&luicode=10000198&containerid=2302835801768120_-_INFO&featurecode=10000001&uicode=10000011&fid=2302835801768120_-_INFO&need_head_cards=1&feed_mypage_card_remould_enable=1&need_new_pop=1&page=1&client_key=75e2c9bcd65d13ac61c877ddaa458060_1224&lfid=2302835801768120&sourcetype=page&oriuicode=10000001_10000198_10000011_10000011_10000198&cum=B9F05A7B"
r = requests.get(url=url, verify=False)
print(r.json())