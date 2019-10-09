from selenium import webdriver

driver = webdriver.Chrome()
driver.get(url='https://nper.cmbc.com.cn/pweb/static/login.html')
print(driver.page_source)