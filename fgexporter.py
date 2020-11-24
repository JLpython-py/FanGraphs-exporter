#! python3

import datetime
import logging
import os
import webbrowser

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

        if not browser_discovered or not driver_discovered:
            if not browser_discovered and not driver_discovered:
                print('''
Firefox executable could not be found in any of the following locations:
''', file=sys.stderr)
                [print(opt, file=sys.stderr) for opt in browser_options]
                print('''
Geckodriver executable could not be found in any of the following locations:
''', file=sys.stderr)
                [print(opt, file=sys.stderr) for opt in driver_options]
                print()
                raise Exception(
                    'firefox.exe and geckodriver.exe could not be found')
            elif not browser_discovered:
                print('''
Firefox executable could not be found in any of the following locations:
''', file=sys.stderr)
                [print(opt, file=sys.stderr) for opt in browser_options]
                print()
                raise Exception(
                    'firefox.exe could not be found')
            elif not driver_discovered:
                print('''
Geckodriver executable could not be found in any of the following locations:
''', file=sys.stderr)
                [print(opt, file=sys.stderr) for opt in driver_options]
                print()
                raise Exception(
                    'geckodriver.exe could not be found')

class Leaderboards:
    def __init__(self):
        self.base = 'https://www.fangraphs.com/leaders.aspx'
        self.original = 'FanGraphs Leaderboard.csv'
        self.name = datetime.datetime.now().strftime('%y%m%d %H.%M.%S')+'.csv'
        self.tables = {
            'Group': 'LeaderBoard1_tsGroup',
            'Stats': 'LeaderBoard1_tsStats',
            'Position': 'LeaderBoard1_tsPosition',
            'Type': 'LeaderBoard1_tsType'}
        self.dropdowns = {
            'League': (
                'LeaderBoard1_rcbLeague',
                'LeaderBoard1_rcbLeague_DropDown'),
            'Team': (
                'LeaderBoard1_rcbTeam',
                'LeaderBoard1_rcbTeam_DropDown'),
            'Single Season': (
                'LeaderBoard1_rcbSeason',
                'LeaderBoard1_rcbSeason_DropDown'),
            'Split': (
                'LeaderBoard1_rcbMonth',
                'LeaderBoard1_rcbMonth_DropDown'),
            'Min': (
                'LeaderBoard1_rcbMin',
                'LeaderBoard1_rcbMin_DropDown'),
            'Season 1': (
                'LeaderBoard1_rcbSeason1',
                'LeaderBoard1_rcbSeason1_DropDown',
                'LeaderBoard1_btnMSeason'),
            'Season 2': (
                'LeaderBoard1_rcbSeason2',
                'LeaderBoard1_rcbSeason2_DropDown',
                'LeaderBoard1_btnMSeason'),
            'Age 1': (
                'LeaderBoard1_rcbAge1',
                'LeaderBoard1_rcbAge1_DropDown',
                'LeaderBoard1_cmdAge'),
            'Age 2': (
                'LeaderBoard1_rcbAge1',
                'LeaderBoard1_rcbAge2_DropDown',
                'LeaderBoard1_cmdAge')}
        self.checkboxes = {
            'SplitTeams': ('LeaderBoard1_cbTeams',),
            'ActiveRoster': ('LeaderBoard1_cbActive',),
            'HOF': ('LeaderBoard1_cbHOF',),
            'SplitSeason': ('LeaderBoard1_cbSeason', 'LeaderBoard1_btnMSeason'),
            'Rookies': ('LeaderBoard1_cbRookie', 'LeaderBoard1_btnMSeason')}
        self.options = {
            'Group': ('Player Stats', 'Team Stats', 'League Stats'),
            'Stats': ('Batting', 'Pitching', 'Fielding'),
            'League': ('All Leagues', 'AL', 'NL'),
            'Team': (
                'All Teams', 'Angels', 'Astros', 'Athletics', 'Blue Jays',
                'Braves', 'Brewers', 'Cardinals', 'Cubs', 'Diamondbacks',
                'Dodgers', 'Gitans', 'Indians', 'Mariners', 'Marlins', 'Mets',
                'Nationals', 'Orioles', 'Padres', 'Phillies', 'Pirates',
                'Rangers', 'Rays', 'Red Sox', 'Reds', 'Rockies', 'Royals',
                'Tigers', 'Twins', 'White Sox', 'Yankees'),
            'SplitTeams': (True, False),
            'ActiveRoster': (True, False),
            'HOF': (True, False),
            'Position': (
                'All', 'P', 'C', '1B', '2B', 'SS', '3B', 'RF', 'CF', 'LF',
                'OF', 'DH', 'NP'),
            'SingleSeason': tuple(
                [y for y in range(int(CURRENT_YEAR), 1870, -1)]),
            'Split': (
                'Full Season', 'Live Stats - Today',
                'Live Stats - Full Season', 'Custom Date Range', 'Yesterday',
                'Last 7 Days', 'Last 14 Days', 'Last 30 Days',
                'Past 1 Calendar Years', 'Past 2 Calendar Years',
                'Past 3 Calendar Years', 'March/April', 'May', 'June', 'July',
                'August', 'September/October', '1st Half', '2nd Half', 'vs L',
                'vs R', 'vs L as L', 'vs R as L', 'vs L as R', 'vs R as R',
                'Shift - All', 'No Shift', 'Shift - Traditional',
                'Shift - Non Traditional', 'Home', 'Away', 'Grounders',
                'Flies', 'Liners', 'Bunts', 'Pull', 'Center', 'Opposite',
                'Low Leverage', 'Medium Leverage', 'High Leverage',
                'Bases Empty', 'Men on Base', 'Men in Scoring', 'C', '1B',
                '2B', 'SS', '3B', 'RF', 'LF', 'OF', 'DH', 'P', 'PH', 'PR',
                'Batting 1st', 'Batting 2nd', 'Batting 3rd', 'Batting 4th',
                'Batting 5th', 'Batting 6th', 'Batting 7th', 'Batting 8th',
                'Batting 9th'),
            'Min': (
                'y', 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100,
                110, 120, 130, 140, 150, 160, 170, 180, 190, 200,
                210, 220, 230, 240, 250, 300, 350, 450, 500,
                550, 600, 650, 700, 750, 800, 850, 900, 950, 1000,
                1500, 2000, 2500, 300, 3500, 4000, 4500, 5000,
                5500, 6000, 6500, 7000, 7500,
                8000, 8500, 9000, 9500, 10000),
            'SplitSeason': (True, False),
            'Rookies': (True, False),
            'Season1': tuple(
                [y for y in range(int(CURRENT_YEAR), 1870, -1)]),
            'Season2': tuple(
                [y for y in range(int(CURRENT_YEAR), 1870, -1)]),
            'Age1': tuple(
                [a for a in range(14, 59)]),
            'Age2': tuple(
                [a for a in range(14, 59)]),
            'Type': (
                'Dashboard', 'Standard', 'Advanced', 'Batted Ball',
                'Win Probability', 'Pitch Type', 'Pitch Value',
                'Plate Discipline', 'Value', 'Pitch Info', '+Stats',
                'Statcast', 'Pitch Type', 'Velocity', 'H-Movement',
                'V-Movement', 'Pitch Type Value', 'Pitch Type Value / 100',
                'Plate Discipline')}
        self.current_settings = {
            'Group': 'Player Stats',
            'Stats': 'Batting',
            'League': 'All Leagues',
            'Team': 'All Teams',
            'SplitTeams': False,
            'ActiveRoster': False,
            'HOF': False,
            'Position': 'All',
            'SingleSeason': CURRENT_YEAR,
            'Split': 'Full Season',
            'Min': 'y',
            'SplitSeason': False,
            'Rookies': False,
            'Season1': CURRENT_YEAR,
            'Season2': CURRENT_YEAR,
            'Age1': 14,
            'Age2': 58,
            'Type': 'Dashboard'}
        self.init_webdriver = WebDriver()
        self.webdriver = self.init_webdriver.webdriver
        self.webdriver.get(self.base)

    def open(self):
        url = self.webdriver.current_url
        webbrowser.open(url)

    def terminate(self):
        self.webdriver.quit()

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

    def config(self, **kwargs):
        arguments = locals().get('kwargs')
        for (category, option) in arguments.items():
            if self.current_settings[category] == option:
                print(f"{category} already set to {option}")
                continue
            try:
                self.clear_popup()
            except:
                pass
            if category in self.tables:
                self.click_table(category, option)
            elif category in self.dropdowns:
                self.click_dropdown(category, option)
                if len(self.dropdowns[category]) == 3:
                    self.click_confirm()
            elif category in self.checkboxes:
                self.click_checkbox(category, option)
            self.current_settings[category] = option
            self.refresh_options()
            print(f'{category} set to {option}')

    def click_table(self, category, option):
        index = list(self.options[category]).index(option)
        tag = 'li'
        div_id = self.tables.get(category)
        options = f'div[id="{div_id}"] {tag}'
        elem = self.webdriver.find_elements_by_css_selector(options)[index]
        try:
            elem.click()
        except:
            self.webdriver.execute_script("arguments[0].click();", elem)

    def click_dropdown(self, category, option):
        index = list(self.options[category]).index(option)
        tag = ('input', 'li')
        div_id = (self.dropdowns[category][0], self.dropdowns[category][1])
        dropdown = f'div[id="{div_id[0]}"] {tag[0]}'
        options = f'div[id="{div_id[1]}"] {tag[1]}'
        elem = self.webdriver.find_element_by_css_selector(dropdown)
        try:
            elem.click()
        except:
            self.webdriver.execute_script("arguments[0].click();", elem)
        print("Dropdown selected")
        elem = self.webdriver.find_elements_by_css_selector(options)[index]
        try:
            elem.click()
        except:
            self.webdriver.execute_script("arguments[0].click();", elem)

    def click_confirm(self):
        if option == self.current_settings[category]:
            return
        input_id = self.dropdowns[category][3]
        button = f'input[id="{input_id}"]'
        elem = self.webdriver.find_element_by_css_selector(button)
        try:
            elem.click()
        except:
            self.webdriver.execute_script("arguments[0].click();", elem)

    def click_checkbox(self):
        input_id = self.checkboxes[category]
        checkbox = f'input[id="{input_id}"]'
        elem = self.webdriver.fine_element_by_css_selector(checkbox)
        try:
            elem.click()
        except:
            self.webdriver.execute_script("arguments[0].click();", elem)

    def clear_popup(self):
        css_selector = 'span[class="ezmob-footer-close"]'
        elem = self.webdriver.find_element_by_css_selector(css_selector)
        try:
            elem.click()
        except:
            self.webdriver.execute_script("arguments[0].click();", elem)
        print("Pop-Up cleared")

    def refresh_options(self):
        self.refresh_group()
        self.refresh_stats()
        self.refresh_active_roster()
        self.refresh_hof()

    def refresh_group(self):
        if self.current_settings['Group'] == 'Player Stats':
            self.options['SplitTeams'] = (True, False)
            self.options['Min'] = (
                'y', 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120,
                130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240,
                250, 300, 350, 450, 500, 550, 600, 650, 700, 750, 800, 850,
                900, 950, 1000, 1500, 2000, 2500, 300, 3500, 4000, 4500, 5000,
                5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000)
        elif self.current_settings['Group'] == 'Team Stats':
            self.options['SplitTeams'] = (False,)
            self.options['Min'] = (0,)
        elif self.current_settings['Group'] == 'League Stats':
            self.options['SplitTeams'] = (False,)
            self.options['Min'] = (0,)
        self.current_settings['SplitTeams'] = self.options['SplitTeams'][0]
        self.current_settings['Min'] = self.options['Min'][0]

    def refresh_stats(self):
        if self.current_settings['Stats'] == 'Batting':
            self.options['Position'] = (
                'All', 'P', 'C', '1B', '2B', 'SS', '3B', 'RF', 'CF', 'LF',
                'OF', 'DH', 'NP')
            self.options['Type'] = (
                'Dashboard', 'Standard', 'Advanced', 'Batted Ball',
                'Win Probability', 'Pitch Type', 'Pitch Value',
                'Plate Discipline', 'Value', 'Pitch Info', '+Stats',
                'Statcast', 'Pitch Type', 'Velocity', 'H-Movement',
                'V-Movement', 'Pitch Type Value', 'Pitch Type Value / 100',
                'Plate Discipline')
        elif self.current_settings['Stats'] == 'Pitching':
            self.options['Position'] = (
                'All', 'Starters', 'Relievers')
            self.options['Type'] = (
                'Dashboard', 'Standard', 'Advanced', 'Batted Ball',
                'Win Probability', 'Pitch Type', 'Pitch Value',
                'Plate Discipline', 'Value', 'Pitch Info', '+Stats',
                'Statcast', 'Pitch Type', 'Velocity', 'H-Movement',
                'V-Movement', 'Pitch Type Value', 'Pitch Type Value / 100',
                'Plate Discipline')
        elif self.current_settings['Stats'] == 'Fielding':
            self.options['Position'] = (
                'All', 'P', 'C', '1B', '2B', 'SS', '3B', 'RF', 'CF', 'LF',
                'OF')
            self.options['Type'] = (
                'Standard', 'Advanced', 'Fans Scouting Report',
                'Inside Edge Fielding')
        self.current_settings['Position'] = self.options['Position'][0]
        self.current_settings['Type'] = self.options['Type'][0]

    def refresh_active_roster(self):
        if self.current_settings['ActiveRoster'] is True:
            self.current_settings['HOF'] = False

    def refresh_hof(self):
        if self.current_settings['HOF'] is True:
            self.options['Min'] = (0,)
            self.current_settings['Season1'] = 1871
            self.current_settings['SplitTeam'] = False
        elif self.current_settings['HOF'] is False:
            self.options['Min'] = (
                'y', 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100,
                110, 120, 130, 140, 150, 160, 170, 180, 190, 200,
                210, 220, 230, 240, 250, 300, 350, 450, 500,
                550, 600, 650, 700, 750, 800, 850, 900, 950, 1000,
                1500, 2000, 2500, 300, 3500, 4000, 4500, 5000,
                5500, 6000, 6500, 7000, 7500,
                8000, 8500, 9000, 9500, 10000)
        self.current_settings['Min'] = self.options['Min'][0]
