from selenium import webdriver


def change(bb):
    # global a
    a = 2
    # global b
    del bb['bb']


a = 1
b = {"bb": 22, "a": 22}
b.pop('bb', 1)
print(b)