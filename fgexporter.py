#! python3
# fgexporter.py

import datetime
import logging
import os
import uuid
import webbrowser

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

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
class WebDriver:
    def __init__(self):
        self.find_executables()
        self.preferences = {
            "browser.download.folderList": 2,
            "browser.download.manager.showWhenStarting": True,
            "browser.download.dir": os.getcwd(),
            "browser.helperApps.neverAsk.saveToDisk": "text/csv"}
        self.options = Options()
        self.options.headless = True
        self.options.binary = self.browser
        for pref in self.preferences:
            self.options.set_preference(pref, self.preferences.get(pref))
        self.webdriver = selenium.webdriver.Firefox(
           options=self.options,
           firefox_binary=self.browser,
           executable_path=self.driver)

    def find_executables(self):
        user = os.path.expanduser('~')
        programs = os.path.join(user, 'AppData', 'Local', 'Programs')

        browser_options = (
            r"C:\Program Files\Mozilla Firefox",)
        browser_discovered = False
        for path in browser_options:
            if os.path.exists(os.path.join(path, 'firefox.exe')):
                self.browser = os.path.join(path, 'firefox.exe')
                browser_discovered = True
                break
        options = '\t- '+'\n\t- '.join(browser_options)
        if not browser_discovered:
            raise Exception(f"""
Firefox executable could not be found in any of the following locations:
{options}""")
        driver_options = (
            os.getcwd(), user, programs,
            os.path.join(programs, 'Python', 'Python38-32'),
            os.path.join(programs, 'Python', 'Python38-32', 'Scripts'),
            os.path.join(programs, 'Python', 'Python38-32', 'Lib'))
        driver_discovered = False
        for path in driver_options:
            if os.path.exists(os.path.join(path, 'geckodriver.exe')):
                self.driver = os.path.join(path, 'geckodriver.exe')
                driver_discovered = True
                break
        options = '\t- '+'\n\t- '.join(driver_options)
        if not driver_discovered:
            raise Exception(f"""
Geckodriver executable could not be found in any of the following locations:
{options}""")

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

class Projections:
    def __init__(self):
        self.base = "https://www.fangraphs.com/projections.aspx"
        self.original = 'FanGraphs Leaderboard.csv'
        self.name = f"{str(uuid.uuid4()}.csv"
        self.selectors = {
            'Stats': {'Options': 'ProjectionBoard1_tsStats'},
            'Position': {'Options': 'ProjectionBoard1_tsPosition'},
            'Team': {'Dropdown': 'ProjectionBoard1_rcbTeam',
                     'Options': 'ProjectionBoard1_rcbTeam_DropDown'},
            'League': {'Dropdown': 'ProjectionBoard1_rcbLeague',
                       'Options': 'ProjectionBoard1_rcbLeague_DropDown'},
            'Projection': {'Options': 'ProjectionBoard1_tsProj'},
            'Update': {'Options': 'ProjectionBoard1_tsUpdate'}}

class Leaderboards:
    def __init__(self):
        self.base = 'https://www.fangraphs.com/leaders.aspx'
        self.original = 'FanGraphs Leaderboard.csv'
        self.name = f"{str(uuid.uuid4())}.csv"
        self.selectors = {
            'Group': {'Options': 'LeaderBoard1_tsGroup'},
            'Stats': {'Options': 'LeaderBoard1_tsStats'},
            'League': {'Dropdown': 'LeaderBoard1_rcbLeague',
                       'Options': 'LeaderBoard_rcbTeam_DropDown'},
            'Team': {'Dropdown': 'LeaderBoard1_rcbTeam',
                     'Options': 'LeaderBoard1_rcbTeam_DropDown'},
            'SplitTeams': {'Checkbox': 'LeaderBoard1_cbTeams'},
            'ActiveRoster': {'Checkbox': 'LeaderBoard1_cbActive'},
            'HOF': {'Checkbox': 'LeaderBoard1_cbHOF'},
            'Position': {'Options': 'LeaderBoard1_tsPosition'},
            'SplitSeason': {'Checkbox': 'LeaderBoard1_cbSeason',
                            'Button': 'LeaderBoard1_btnMSeason'},
            'Rookies': {'Checkbox': 'LeaderBoard1_cbRookie',
                        'Rookies': 'LeaderBoard1_btnMSeason'},
            'SingleSeason': {'Dropdown': 'LeaderBoard_rcbSeason',
                              'Options': 'LeaderBoard1_rcbSeason_DropDown'},
            'Split': {'Dropdown': 'LeaderBoard1_rcbMonth',
                      'Options': 'LeaderBoard1_rcbMonth_DropDown'},
            'Min': {'Dropdown': 'LeaderBoard1_rcbMin',
                    'Options': 'LeaderBoard1_rcbMin_DropDown'},
            'Season1': {'Dropdown': 'LeaderBoard1_rcbSeason1',
                         'Options': 'LeaderBoard1_rcbSeason1_DropDown',
                         'Button': 'LeaderBoard1_btnMSeason'},
            'Season2': {'Dropdown': 'LeaderBoard1_rcbSeason2',
                         'Options': 'LeaderBoard1_rcbSeason2_DropDown',
                         'Button': 'LeaderBoard1_btnMSeason'},
            'Age1': {'Dropdown': 'LeaderBoard1_rcbAge1',
                      'Options': 'LeaderBoard1_rcbAge1_DropDown',
                      'Button': 'LeaderBoard1_cmdAge'},
            'Age2': {'Dropdown': 'LeaderBoard1_rcbAge2',
                      'Options': 'LeaderBoard1_rcbAge2_DropDown',
                      'Button': 'LeaderBoard1_cmdAge'}}
        self.options = {}
        self.init_webdriver = WebDriver()
        self.webdriver = self.init_webdriver.webdriver
        self.webdriver.get(self.base)

    def config(self, **kwargs):
        arguments = locals().get('kwargs')
        for (category, option) in arguments.items():
            self.refresh_options()
            try:
                self.clear_popup()
            except:
                pass
            if category in ('Group', 'Stats', 'Position'):
                index = list(self.options[category]).index(option)
                self.webdriver.click_table(self.selectors[category], index)
            elif category in ('League', 'Team', 'SingleSeason', 'Split',
                              'Min', 'Age1', 'Age2'):
                index = list(self.options[category]).index(option)
                self.webdriver.click_dropdown(self.selectors[category], index)
                if 'Button' in self.selectors[category]:
                    self.webdriver.click_button(self.selectors[category])
            elif category in ('SplitTeams', 'ActiveRoster', 'HOF',
                              'SplitSeason', 'Rookies'):
                self.click_checkbox(category, option)
                if 'Button' in self.selectors[category]:
                    self.webdriver.click_button(self.selectors[category])
            print(f'{category} set to {option}')

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
        if os.path.exists(os.path.join(os.getcwd(), self.name)):
            os.remove(os.path.join(os.getcwd(), self.name))
        os.rename(
            os.path.join(os.getcwd(), self.original),
            os.path.join(os.getcwd(), self.name))
