import random
import time
from io import BytesIO

from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webspider.captcharecognition.chaojiying import Chaojiying
from selenium.webdriver.support import expected_conditions as EC

EMAIL = '347428365@qq.com'
PASSWORD = 'Hehao3911160512'
# 超级鹰用户名、密码、软件ID、验证码类型
CHAOJIYING_USERNAME = '1hehao'
CHAOJIYING_PASSWORD = 'Hehao3911160512'
CHAOJIYING_SOFT_ID = 897777
CHAOJIYING_KIND = 9004


class CrackTouClick():
    def __init__(self):
        self.url = 'https://www.geetest.com/show/'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.email = EMAIL
        self.password = PASSWORD
        self.chaojiying = Chaojiying(CHAOJIYING_USERNAME, CHAOJIYING_PASSWORD, CHAOJIYING_SOFT_ID)

    def open(self):
        """
        打开网页输入用户名密码
        :return:
        """
        self.browser.get(self.url)
        tab = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tab-item-2')))
        tab.click()
        # email = self.wait.until(EC.presence_of_element_located((By.ID, 'email')))
        # password = self.wait.until(EC.presence_of_element_located((By.ID, 'password')))
        # email.send_keys(self.email)
        # password.send_keys(self.password)

    def get_geetest_button(self):
        """
        获取初始验证按钮
        :return: 按钮对象
        """
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))
        return button

    def get_touclick_element(self):
        element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_big_item')))
        return element

    def get_position(self):
        """
        获取验证图片位置
        :return: 验证图片元组
        """
        img = self.get_touclick_element()
        time.sleep(2)
        location = img.location_once_scrolled_into_view
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        return top, bottom, left, right

    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_geetest_image(self, name='captcha.png'):
        """
        获取验证图片
        :param name:
        :return: 图片对象
        """
        top, bottom, left, right = self.get_position()
        print('验证图片位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        screenshot.save('screenshot.png')
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha

    def get_points(self, captcha_result):
        """
        解析识别结果
        :param captcha_result: 识别结果
        :return: 转化后的结果
        """
        groups = captcha_result.get('pic_str').split('|')
        locations = [[int(number) for number in group.split(',')] for group in groups]
        return locations

    def touch_click_word(self, locations):
        """
        点击验证图片
        :param locations: 点击位置
        :return: None
        """
        for location in locations:
            print(location)
            ActionChains(self.browser).move_to_element_with_offset(self.get_touclick_element(), location[0], location[1]).click().perform()
            time.sleep(random.randint(1,5))

    def touch_click_verify(self):
        """
        点击验证按钮
        :return: None
        """
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_commit_tip')))
        button.click()

    def try_crack(self):
        # 获取验证图片
        image = self.get_geetest_image('captcha.png')
        byte_array = BytesIO()
        image.save(byte_array, format='PNG')
        result = self.chaojiying.post_pic(byte_array.getvalue(), CHAOJIYING_KIND)
        print(result)
        locations = self.get_points(result)
        self.touch_click_word(locations)
        self.touch_click_verify()
        # 判断是否成功
        try:
            success = self.wait.until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_success_radar_tip_content'), '验证成功'))
            print('验证成功')
        except TimeoutException:
            print('未通过验证，登陆失败')
            result = self.chaojiying.report_error(result.get('pic_id'))
            print(result)
            self.try_crack()

    def crack(self):
        # 输入用户名密码
        self.open()
        # 点击验证按钮
        button = self.get_geetest_button()
        button.click()
        # 向下滚动
        self.browser.execute_script('window.scroll(0, 500)')
        self.try_crack()


if __name__ == '__main__':
    crack = CrackTouClick()
    crack.crack()