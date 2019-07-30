"""
输入一个长度为13的字符串，每个字符都是1-9中的数字，且每个数字最多只有4个，
这个字符串对应现实生活中麻将的一副牌型（不考虑花色的情况），
编写函数或者类，判断该字符串对应的牌型是否下叫，即输出为True或False；
牌型：【4：刻子1111】【3：顺子123 刻子111】【2：对子11】
一、3+3+3+3+2
二、2+2+2+2+2+2+2
"""
import copy
import re


def listen(card):
    ret = list()
    true_num = 13
    # 去掉所有空格
    card = [int(c) for c in card if c != ' ']
    card.sort()
    # 得到每张牌的个数字典
    count = {}
    for c in card:
        count.setdefault(c, 0)  # 确保了键存在于count字典中(默认值是0)
        count[c] = count[c] + 1
        if count[c] == 4:
            card = card.replace(c, ' ')
            ret.append(c*4)
            true_num += 1
        if count[c] > 4:
            return '相同的牌最多出现4次'
    print(count)
    # 判断是否是花猪
    if len(card) != true_num:
        return f'花猪：应该有{true_num}张牌'
    card = re.sub(r'\s+', '', card)
    print(card)
    for i in range(len(card)):
        if str(int(card[i])+1) in card and str(int(card[i])+2) in card:
            print(card.index(str(int(card[i])+1)), card.index(str(int(card[i])+2)))
    return ret


if __name__ == '__main__':
    print(listen('123 2344 789 6666'))
