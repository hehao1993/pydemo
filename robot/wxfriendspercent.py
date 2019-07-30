import itchat

itchat.login()
friends = itchat.get_friends(update=True)[0:]
# 初始化计数器，有男有女，当然，有些人是不填的
male = female = other = 0
# 遍历这个列表，列表里第一位是自己，所以从"自己"之后开始计算
for i in friends[1:]:
    sex = i["Sex"]
    if sex == 1:
        male += 1
    elif sex == 2:
        female += 1
    else:
        other += 1
total = len(friends[1:])

male = round(male / total * 100, 2)
female = round(female / total * 100, 2)
other = round(other / total * 100, 2)

print(f'男性好友{male}%')
print(f'女性好友{female}%')
print(f'其他好友{other}%')
