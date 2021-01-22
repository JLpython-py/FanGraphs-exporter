#! python3
# fgexporter.py

'''
FanGraphs-exporter/fgexporter.py

fgexporter allows users to navigate the FanGraphs website pages.
Users can configure the data which the website outputs then export the data.

===============================================================================
MIT License

Copyright (c) 2021 Jacob Lee

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import datetime
import json
import os

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

class InvalidSettingError(Exception):
    ''' Raised when the setting argument of Fangraphs.__init__ is invalid
'''
    def __init__(self, setting):
        self.message = f"Invalid setting passed, '{setting}'"
        super().__init__(self.message)

class FanGraphs:
    ''' Create specialized browser which easily navigates the FanGraphs website
'''
    def __init__(self, *, setting):
        directory = setting.lower()
        if directory not in os.listdir('data'):
            raise InvalidSettingError(directory)
        with open(os.path.join('data', 'base_address.txt')) as file:
            self.address = json.load(file).get(directory)

        options = ['menu', 'dropdown', 'checkbox', 'button']
        self.selectors = {}
        for opt in options:
            with open(os.path.join('data', directory, f'{opt}.txt')) as file:
                self.selectors.setdefault(opt, json.load(file))

        self.preferences = {
            'browser.download.folderList': 2,
            'browser.download.manager.showWhenStarting': False,
            'browser.download.dir': os.getcwd(),
            'browser.helperApps.neverAsk.saveToDisk': 'text/csv'}
        self.options = Options()
        self.browser = self.driver_setup()
        self.browser.get(self.address)

    class InvalidCategoryError(Exception):
        ''' Raised when the data configuration category is invalid
'''

        def __init__(self, category):
            self.message = f"Invalid category passed: {category}."
            super().__init__(self.message)

    class InvalidOptionError(Exception):
        ''' Raised when the data configuration option is invalid
'''
        def __init__(self, category, option):
            self.message = f"Invalid option passed for category {category}: {option}."
            super().__init__(self.message)

    def driver_setup(self):
        ''' Create a selenium headless browser with pre-defined preferences
'''
        self.options.headless = True
        for pref in self.preferences:
            self.options.set_preference(pref, self.preferences.get(pref))
        browser = webdriver.Firefox(options=self.options)
        return browser

    def reset(self):
        ''' Navigate the browser to the initial FanGraphs page
'''
        self.browser.get(self.address)

    def location(self):
        ''' Return the browser current URL
'''
        return self.browser.current_url

    def end_task(self):
        ''' Call the quit method of the browser
'''
        self.browser.quit()

    def get_options(self, category):
        ''' Return the possible options which the category can be configured to
'''
        category = category.lower()
        if not any([category in self.selectors[s]
                    for s in self.selectors]):
            raise self.InvalidCategoryError(category)
        if category in self.selectors['dropdown']:
            elem = self.browser.find_element_by_css_selector(
                f"div[id={self.selectors['menu'][category]}] input")
            self.force_click(elem)
            elems = self.browser.find_elements_by_css_selector(
                f"div[id={self.selectors['dropdown'][category]}] li")
            options = [elem.text for elem in elems]
        elif category in self.selectors['menu']:
            elems = self.browser.find_elements_by_css_selector(
                f"div[id={self.selectors['menu'][category]}] li")
            options = [elem.text for elem in elems]
        elif category in self.selectors['checkbox']:
            options = [True, False]
        return options

    def get_current(self, category):
        ''' Return the options which the category is currently configured to
'''
        category = category.lower()
        if not any([category in self.selectors[s]
                    for s in self.selectors]):
            raise self.InvalidCategoryError(category)
        if category in self.selectors['dropdown']:
            elem = self.browser.find_element_by_css_selector(
                f"div[id={self.selectors['menu'][category]}] input")
            current = elem.get_attribute("value")
        elif category in self.selectors['menu']:
            elems = self.browser.find_elements_by_css_selector(
                f"div[id={self.selectors['menu'][category]}] a")
            for elem in elems:
                if "rtsSelected" in elem.get_attribute("class"):
                    current = elem.text
                    break
        elif category in self.selectors['checkbox']:
            elem = self.browser.find_element_by_css_selector(
                f"input[id={self.selectors['checkbox'][category]}")
            current = elem.get_attribute("checked") == "checked"
        return current

    def config(self, **kwargs):
        ''' Set the configuration option to the category
'''
        for (category, option) in kwargs.items():
            available_options = self.get_options(category)
            #Verify option is valid
            if option not in available_options:
                raise self.InvalidOptionError(category, option)
            #Verify option is not already set
            if option == self.get_current(category):
                return
            #Set categories to specified options
            if category in self.selectors['dropdown']:
                self.set_dropdown(category, option)
            elif category in self.selectors['menu']:
                self.set_menu(category, option)
            elif category in self.selectors['checkbox']:
                self.set_checkbox(category)
            #Click button to submit form, if necessary
            if category in self.selectors['button']:
                self.click_button(category)

    def force_click(self, element):
        ''' Successively attempt to click the element and scroll down until clicked

'''
        while True:
            try:
                element.click()
                return
            except ElementClickInterceptedException:
                html = self.browser.find_element_by_css_selector("html")
                html.send_keys(Keys.PAGE_DOWN)

    def set_menu(self, category, option):
        ''' Set the menu-type category to the specified option
'''
        available_options = self.get_options(category)
        elems = self.browser.find_elements_by_css_selector(
            f"div[id={self.selectors['menu'][category]}] li")
        opt_elem = elems[available_options.index(option)]
        self.force_click(opt_elem)

    def set_dropdown(self, category, option):
        ''' Set the dropdown-type category to the specified option
'''
        menu_elem = self.browser.find_elements_by_css_selector(
            f"div[id={self.selectors['menu'][category]}] input")
        self.force_click(menu_elem)
        available_options = self.get_options(category)
        elems = self.browser.find_elements_by_css_selector(
            f"div[id={self.selectors['dropdown'][category]}] li")
        opt_elem = elems[available_options.index(option)]
        self.force_click(opt_elem)

    def set_checkbox(self, category):
        ''' Set the checkbox-type category to the specified option
'''
        elem = self.browser.find_element_by_css_selector(
            f"input[id={self.selectors['checkbox'][category]}")
        self.force_click(elem)

    def click_button(self, category):
        ''' Click the corresponding button to submit the configuration
'''
        elem = self.browser.find_element_by_css_selector(
            f"input[id={self.selectors['button'][category]}")
        self.force_click(elem)

    def export(self):
        ''' Click the 'Export Data' button to download the configured data
'''
        filenames = [
            "FanGraphs Leaderboard.csv",
            f"{datetime.datetime.now().strftime('%d.%m.%y %H.%M.%S')}.csv"]
        directory = self.preferences.get('browser.download.dir')
        while True:
            try:
                WebDriverWait(self.browser, 20).until(
                    expected_conditions.element_to_be_clickable(
                        (By.LINK_TEXT, "Export Data")
                        )).click()
                break
            except ElementClickInterceptedException:
                html = self.browser.find_element_by_css_selector("html")
                html.send_keys(Keys.PAGE_DOWN)
        if os.path.exists(os.path.join(directory, filenames[1])):
            os.remove(os.path.join(directory, filenames[1]))
        os.rename(
            os.path.join(directory, filenames[0]),
            os.path.join(directory, filenames[1]))

        return filenames[1]
