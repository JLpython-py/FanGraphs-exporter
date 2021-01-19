#! python3
# functional_tests.py

import json
import unittest

from selenium import webdriver

class TestNavigateFanGraphsWebsite(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_leaderboards_page(self):
        #User navigate to the FanGraphs Leaderboards page
        with open('data\\base_address.txt') as file:
            self.browser.get(json.load(file).get("leaders"))
        self.assertIn("Leaderboards", self.browser.title)

        #User notices all options to configure the data
        with open('data\\leaders_selectors.txt') as file:
            selectors = json.load(file)
        for select in selectors:
            for sel in selectors[select]:
                self.assertEqual(
                    len(self.browser.find_elements_by_id(
                        selectors[select][sel])),
                    1,
                    sel)

        #User notices 'Export Data' button
        export_data_button = self.browser.find_element_by_id(
            "LeaderBoard1_cmdCSV")
        self.assertEqual(export_data_button.text, "Export Data")

        #User notices advertisement covering page and 'X' button to close it
        close_ad_button = self.browser.find_element_by_css_selector(
            "span[class='ezmob-footer-close']")
        self.assertEqual(close_ad_button.text, "x")

    '''
    def test_predictions_page(self):
        with open('data\\base_address.txt') as file:
            self.browser.get(json.load(file).get("Projections"))
        self.assertIn("Projections", self.browser.title)
    '''

if __name__ == '__main__':
    unittest.main()
