#! python3
# tests.py

import json
import os
import unittest

import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class TestClassFanGraphs(unittest.TestCase):

    def test_files_exist(self):
        directories = {
            'leaders': [
                'menu.txt', 'dropdown.txt', 'checkbox.txt', 'button.txt']
            }
        for dirname in directories:
            self.assertTrue(
                os.path.exists(os.path.join('data', dirname)))
            self.assertEqual(
                set(os.listdir(os.path.join('data', dirname))),
                set(directories[dirname]))

class TestFanGraphsLeadersSettings(unittest.TestCase):

    def setUp(self):
        with open(os.path.join('data', 'base_address.txt')) as file:
            self.url = json.load(file).get("leaders")
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)

    def tearDown(self):
        self.browser.quit()

    def test_leaders_address(self):
        self.browser.get(self.url)
        self.assertIn("Leaderboards", self.browser.title)

    def test_find_data_configuration_elements(self):
        self.browser.get(self.url)
        files = ['menu.txt', 'dropdown.txt', 'checkbox.txt', 'button.txt']
        for filename in files:
            with open(os.path.join('data', 'leaders', filename)) as file:
                data = json.load(file)
                for select in data:
                    self.assertEqual(
                        len(self.browser.find_elements_by_id(data[select])),
                        1, data[select])

    def test_find_export_data_elements(self):
        self.browser.get(self.url)
        export_data_button = self.browser.find_element_by_id(
            "LeaderBoard1_cmdCSV")
        self.assertEqual(export_data_button.text, "Export Data")

    def test_find_popup_elements(self):
        self.browser.get(self.url)
        while True:
            try:
                close_popup_button = self.browser.find_element_by_css_selector(
                    "span[class='ezmob-footer-close']")
                break
            except selenium.common.exceptions.NoSuchElementException:
                self.browser.refresh()
                continue
        self.assertEqual(close_popup_button.text, "x")
        popup = self.browser.find_element_by_id("ezmobfooter")
        self.assertEqual(popup.get_attribute("style"), "")
        close_popup_button.click()
        self.assertNotEqual(popup.get_attribute("style"), "")

if __name__ == '__main__':
    unittest.main()
