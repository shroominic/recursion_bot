import os
import random
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as BS
from selenium import webdriver

most_important_link = "https://www.google.com/"


# Static Functions
def xpath_soup(soup_element):
    components = []
    child = soup_element if soup_element.name else soup_element.parent
    for parent in child.parents:
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name
            if siblings == [child] else
            '%s[%d]' % (child.name, 1 + siblings.index(child))
        )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)


class RekursionBot:
    def __init__(self):
        self.driver = None
        self.soup = None

    def init_chrome(self, chromedriver_path):
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--window-size=720,1080")
        self.driver = webdriver.Chrome(
            executable_path=chromedriver_path,
            options=chrome_options)

    def open_target_page(self):
        self.driver.get(most_important_link)
        time.sleep(1)
        self.refresh_soup()

    # Utility Methods
    def refresh_soup(self):
        self.soup = BS(self.driver.page_source, 'lxml')

    def typo_need_to_get_fixed(self):
        try:
            t = self.driver.find_element_by_xpath("/html/body/div[7]/div/div[9]/div[1]/div/div[1]/div[2]/p/a/b/i")
            return True
        except Exception as e:
            print(e)
            return False

    def click_button(self, text):
        btn_element = None

        for btn in self.soup.find_all('button'):
            if text in str(btn):
                btn_element = btn
        try:
            xpath = xpath_soup(btn_element)
            self.driver.find_element_by_xpath(xpath).click()
        except Exception as e:
            print(e)

    def send_keys(self, text):
        for char in text:
            self.driver.find_element(By.NAME, "q").send_keys(f"{char}")
            time.sleep(0.1)
        self.driver.find_element(By.NAME, "q").send_keys("" + Keys.ENTER)
        time.sleep(2)

    def fix_typo(self):
        element = self.driver.find_element_by_xpath("/html/body/div[7]/div/div[9]/div[1]/div/div[1]/div[2]/p/a/b/i")
        ActionChains(self.driver).move_to_element(element).perform()
        time.sleep(1)
        element.click()
