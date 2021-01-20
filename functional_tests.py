#! python3
# functional_tests.py

import logging
import unittest

import fgexporter

class TestModuleFunctionality(unittest.TestCase):
        
    def test_set_setting_to_leaders(self):
        #User triggers fgexporter.InvalidSettingError
        self.assertRaises(
            fgexporter.InvalidSettingError,
            fgexporter.FanGraphs,
            setting='')

        #User sets FanGraphs search to leaders
        self.fangraphs = fgexporter.FanGraphs(setting="leaders")

        #User triggers fgexporter.FanGraphs.InvalidCategoryError
        self.assertRaises(
            fgexporter.FanGraphs.InvalidCategoryError,
            self.fangraphs.get_options,
            category='')

        #User lists the available options for each category
        num_options = {
            "group": 3, "stats": 3, "league": 3, "team": 31, "split_teams": 2,
            "active_roster": 2, "hof": 2, "position": 13, "season": 150,
            "split": 67, "min": 60, "split_season": 2, "rookies": 2,
            "season1": 150, "season2": 150, "age1": 45, "age2": 45}
        for opt in num_options:
            self.assertEqual(
                len(self.fangraphs.get_options(opt)),
                num_options[opt],
                opt)

        #User checks which options are currently selected
        sel_options = {
            "group": "Player Stats", "stats": "Batting",
            "league": "All Leagues", "team": "All Teams", "split_teams": False,
            "active_roster": False, "hof": False, "position": "All",
            "split": "Full Season", "min": "Qualified", "season": "2020",
            "split_season": False, "rookies": False, "season1": "2020",
            "season2": "2020", "age1": "14", "age2": "58"}
        for opt in sel_options:
            self.assertEqual(
                self.fangraphs.get_current(opt),
                sel_options[opt],
                opt)

        #User configures data results
        categories = [
            'group', 'stats', 'league', 'team', 'split_teams',
            'active_roster', 'hof', 'position', 'split', 'min', 'season',
            'split_season', 'rookies', 'season1', 'season2', 'age1', 'age2']
        for cat in categories:
            options = self.fangraphs.get_options(cat)
            for opt in options:
                self.fangraphs.config(**{cat: opt})
                if opt == self.fangraphs.get_current(cat):
                    self.assertLogs(
                        logging.DEBUG,
                        f"{cat} already set as {opt}")
                self.assertLogs(
                    logging.DEBUG,
                    f"Sucessfully set {cat} as {opt}")
                if cat in self.fangraphs.selectors['button']:
                    self.assertLogs(
                        logging.DEBUG,
                        f"Successfully submitted {cat} with button")
            self.fangraphs.reset()

if __name__ == '__main__':
    unittest.main()
