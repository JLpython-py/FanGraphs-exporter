#! python3
# fgexporter.py

import datetime
import logging
import os
import uuid

import bs4
import requests
import selenium
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
        self.get_possible_paths()
        self.executables = {}
        self.find_executable('Firefox')
        self.find_executable('Geckodriver')
        self.webdriver_setup()

    def get_possible_paths(self):
        user = os.path.expanduser('~')
        programs = os.path.join(user, 'AppData', 'Local', 'Programs')
        self.options = {
            'Firefox': [
                r"C:\Program Files\Mozilla Firefox"],
            'Geckodriver': [
                os.getcwd(), user, programs,
                os.path.join(programs, 'Python', 'Python38-32'),
                os.path.join(programs, 'Python', 'Python38-32', 'Scripts'),
                os.path.join(programs, 'Python', 'Python38-32', 'Lib')]}

    def find_executable(self, name):
        file = f"{name.lower()}.exe"
        destination = None
        for location in self.options[name]:
            destination = os.path.join(location, file)
            if os.path.exists(destination):
                break
        self.executables[file] = destination

    def webdriver_setup(self):
        preferences = {
            "browser.download.folderList": 2,
            "browser.download.manager.showWhenStarting": False,
            "browser.download.dir": os.getcwd(),
            "browser.helperApps.neverAsk.saveToDisk": "text/csv"}
        options = Options()
        options.headless = True
        #options.binary = self.executables['Firefox']
        for pref in preferences:
            options.set_preference(pref, preferences.get(pref))
        self.webdriver = selenium.webdriver.Firefox(
           options=options,
           firefox_binary=self.executables['Firefox'],
           executable_path=self.executables['Geckodriver'])

class FanGraphs:
    def __init__(self, *, setting):
        self.original = 'FanGraphs Leaderboard.csv'
        self.new = f"{str(uuid.uuid4())}.csv"
        with open(f"docs\BaseAddress.txt") as jsonfile:
            base_address = json.load(jsonfile)
        with open(f"docs\Selectors.txt") as jsonfile:
            selectors = json.load(jsonfile)
        with open(f"docs\SelectionTypes.txt") as jsonfile:
            selection_types = json.load(jsonfile)

        self.base = base_address.get(setting)
        self.selectors = selectors.get(setting)
        self.selection_types = selection_types.get(setting)
        self.options = {}
        self.init_webdriver = WebDriver()
        self.webdriver = self.init_webdriver.webdriver
        self.webdriver.get(self.base)

    def config(self, **kwargs):
        arguments = locals().get('kwargs')
        for (category, option) in arguments.items():
            self.refresh_options()
            try:
                self.webdriver.clear_popup()
            except:
                pass
            if category in self.selection_types['Table']:
                index = list(self.options[category]).index(option)
                self.webdriver.click_table(self.selectors[category], index)
            elif category in self.selection_types['Dropdown']:
                index = list(self.options[category]).index(option)
                self.webdriver.click_dropdown(self.selectors[category], index)
            elif category in self.selection_types['Checkbox']:
                self.click_checkbox(category, option)
            if 'Button' in self.selectors[category]:
                self.webdriver.click_button(self.selectors[category])

    def click_table(self, selectors, index):
        div_li = selectors.get('Options')
        elem = self.webdriver.find_elements_by_css_selector(
            f"div[id='{div_li}'] li")[index]
        try:
            elem.click()
        except:
            self.webdriver.execute_script("arguments[0].click();", elem)

    def click_dropdown(self, selectors, index):
        div_input = selectors.get('Dropdown')
        dropdown = self.webdriver.find_element_by_css_selector(
            f"div[id='{div_input}'] input")
        try:
            dropdown.click()
        except:
            self.webdriver.execute_script("arguments[0].click();", dropdown)
        div_li = selectors.get('Options')
        option = self.webdriver.find_elements_by_css_selector(
            f"div[id='{div_li}'] li")[index]
        try:
            option.click()
        except:
            self.webdriver.execute_script("arguments[0].click();", option)

    def click_confirm(self, selectors):
        input_id = selectors.get('Button')
        button = self.webdriver.find_element_by_css_selector(
            f"input[id='{input_id}']")
        try:
            button.click()
        except:
            self.webdriver.execute_script("arguments[0].click();", button)

    def click_checkbox(self, selectors):
        input_id = selectors.get('Checkbox')
        checkbox = self.webdriver.fine_element_by_css_selector(
            f"input[id='{input_id}']")
        try:
            checkbox.click()
        except:
            self.webdriver.execute_script("arguments[0].click();", checkbox)

    def clear_popup(self):
        popup = self.webdriver.find_element_by_css_selector(
            'span[class="ezmob-footer-close"]')
        try:
            popup.click()
        except:
            self.webdriver.execute_script("arguments[0].click();", popup)

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
            os.path.join(os.getcwd(), self.original),
            os.path.join(os.getcwd(), self.new))
