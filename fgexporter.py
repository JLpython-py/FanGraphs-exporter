#! python3
# fgexporter.py

import datetime
import json
import logging
import os

import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

CURRENT_TIME = datetime.datetime.now()
CURRENT_YEAR = CURRENT_TIME.strftime('%Y')

logging.basicConfig(
    level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

class WebDriver:

    def __init__(self):
        preferences = {
            "browser.download.folderList": 2,
            "browser.download.manager.showWhenStarting": False,
            "browser.download.dir": os.getcwd(),
            "browser.helperApps.neverAsk.saveToDisk": "text/csv"}
        options = Options()
        options.headless = True
        for pref in preferences:
            options.set_preference(pref, preferences.get(pref))
        self.browser = webdriver.Firefox(
           options=options)

class InvalidSettingError(Exception):
    ''' Raised when the setting argument of __init__ is invalid
'''
    def __init__(self, setting):
        self.message = f"Invalid setting passed, '{setting}'"
        super().__init__(self.message)

class FanGraphs:
    def __init__(self, *, setting):
        directory = setting.lower()
        if directory not in os.listdir('data'):
            raise InvalidSettingError(directory)
        with open(os.path.join('data', 'base_address.txt')) as file:
            address = json.load(file).get('leaders')

        options = ['menu', 'dropdown', 'checkbox', 'button']
        self.selectors = {}
        for opt in options:
            with open(os.path.join('data', directory, f'{opt}.txt')) as file:
                self.selectors.setdefault(opt, json.load(file))

        self.webdriver = WebDriver()
        self.browser = self.webdriver.browser
        self.browser.get(address)

    class InvalidCategoryError(Exception):
        ''' Raised when the category argument of listopts is invalid
'''
        
        def __init__(self, category):
            self.message = f"Invalid category passed: {category}."
            super().__init__(self.message)

    def get_options(self, category):
        category = category.lower()
        if not any([category in self.selectors[o] for o in self.selectors]):
            raise self.InvalidCategoryError(category)
        if category in self.selectors['dropdown']:
            elems = self.browser.find_elements_by_css_selector(
                f"div[id={self.selectors['dropdown'][category]}] li")
            return [elem.text for elem in elems]
        elif category in self.selectors['menu']:
            elems = self.browser.find_elements_by_css_selector(
                f"div[id={self.selectors['menu'][category]}] li")
            return [elem.text for elem in elems]
        elif category in self.selectors['checkbox']:
            return [True, False]

    def get_current(self, category):
        category = category.lower()
        if not any([category in self.selectors[o] for o in self.selectors]):
            raise self.InvalidCategoryError(category)
        if category in self.selectors['dropdown']:
            elem = self.browser.find_element_by_css_selector(
                f"div[id={self.selectors['menu'][category]}] input")
            return elem.get_attribute("value")
        elif category in self.selectors['menu']:
            elems = self.browser.find_elements_by_css_selector(
                f"div[id={self.selectors['menu'][category]}] a")
            for elem in elems:
                if "rtsSelected" in elem.get_attribute("class"):
                    return elem.text
        elif category in self.selectors['checkbox']:
            elem = self.browser.find_element_by_css_selector(
                f"input[id={self.selectors['checkbox'][category]}")
            return elem.get_attribute("checked") == "checked"
        
    def config(self, **kwargs):
        for (category, option) in kwargs.items():
            self.refresh_options()
            try:
                self.webdriver.clear_popup()
            except:
                pass

    def refresh_options(self):
        res = requests.get(self.webdriver.current_url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, features="html.parser")
        for selector in self.selectors:
            if 'Options' not in self.selectors[selector]:
                continue
            div_id = self.selectors[selector].get('Options')
            elements = soup.select(f'div[id="{div_id}"] li')
            self.options[selector] = [e.getText() for e in elements]
            options = [e.getText() for e in elements]

    def export(self):
        try:
            self.clear_popup()
        except:
            pass
        WebDriverWait(self.webdriver, 20).until(
            expected_conditions.element_to_be_clickable(
                (By.LINK_TEXT, "Export Data")
                )
            ).click()
        if os.path.exists(os.path.join(os.getcwd(), self.new)):
            os.remove(os.path.join(os.getcwd(), self.new))
        os.rename(
            os.path.join(
                os.getcwd(),
                "FanGraphs Leaderboard.csv"),
            os.path.join(
                os.getcwd(),
                f"{datetime.datetime.now().strftime('%D %T')}.csv"))
