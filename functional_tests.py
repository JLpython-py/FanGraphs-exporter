#! python3
# functional_tests.py

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
        fangraphs = fgexporter.FanGraphs(setting="leaders")

        #User triggers fgexporter.FanGraphs.InvalidCategoryError
        self.assertRaises(
            fgexporter.FanGraphs.InvalidCategoryError,
            fangraphs.get_options,
            category='')

        #User lists the available options for each category
        num_options = {
            "group": 3, "stats": 3, "league": 3, "team": 31, "split_teams": 2,
            "active_roster": 2, "hof": 2, "position": 13, "season": 150,
            "split": 67, "min": 60, "split_season": 2, "rookies": 2,
            "season1": 150, "season2": 150, "age1": 45, "age2": 45}
        for opt in num_options:
            self.assertEqual(
                len(fangraphs.get_options(opt)),
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
                fangraphs.get_current(opt),
                sel_options[opt],
                opt)

if __name__ == '__main__':
    unittest.main()
