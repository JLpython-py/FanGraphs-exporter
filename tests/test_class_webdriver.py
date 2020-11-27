#! python3
# test_class_webdriver

import os
import unittest

import selenium
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options

class TestClassWebDriver(unittest.TestCase):
    def test_get_possible_paths(self):
        user = os.path.expanduser('~')
        programs = os.path.join(user, 'AppData', 'Local', 'Programs')
        options = {
            'Firefox': [
                r"C:\Program Files\Mozilla Firefox"],
            'Geckodriver': [
                os.getcwd(),
                user,
                programs,
                os.path.join(programs, 'Python', 'Python38-32'),
                os.path.join(programs, 'Python', 'Python38-32', 'Scripts'),
                os.path.join(programs, 'Python', 'Python38-32', 'Lib')]}
        results = []
        for file in options:
            for path in options[file]:
                results.append(os.path.exists(path))
        self.assertTrue(all(results))

    def test_find_firefox(self):
        options = [
            r"C:\Program Files\Mozilla Firefox"]
        found = False
        for location in options:
            if os.path.exists(os.path.join(location, 'firefox.exe')):
                found = True
        self.assertTrue(found)

    def test_find_geckodriver(self):
        user = os.path.expanduser('~')
        programs = os.path.join(user, 'AppData', 'Local', 'Programs')
        options = [
            os.getcwd(), user, programs,
            os.path.join(programs, 'Python', 'Python38-32'),
            os.path.join(programs, 'Python', 'Python38-32', 'Scripts'),
            os.path.join(programs, 'Python', 'Python38-32', 'Lib')]
        found = False
        for location in options:
            if os.path.exists(os.path.join(location, 'geckodriver.exe')):
                found = True
        self.assertTrue(found)

    def test_set_preferences(self):
        options = Options()
        preferences = {
            "browser.download.folderList": 2,
            "browser.download.manager.showWhenStarting": False,
            "browser.download.dir": os.getcwd(),
            "browser.helperApps.neverAsk.saveToDisk": "text/csv"}
        for pref in preferences:
            options.set_preference(pref, preferences.get(pref))
            self.assertEqual(
                options.__dict__['_preferences'][pref], preferences[pref])

    def test_set_headless(self):
        options = Options()
        options.headless = True
        self.assertIn('-headless', options.__dict__['_arguments'])

    def test_set_binary(self):
        options = Options()
        with r"C:\Program Files\Mozilla Firefox\firefox.exe" as binary:
            options.binary = binary
            self.assertTrue(bool(options.__dict__['_binary']))
        
if __name__ == '__main__':
    unittest.main()
