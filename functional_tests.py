#! python3
# functional_tests.py

import os
import unittest

import fgexporter

class TestModuleFunctionality(unittest.TestCase):

    def test_invalid_setting_raises_error(self):
        self.assertRaises(
            fgexporter.InvalidSettingError,
            fgexporter.FanGraphs,
            setting='')

    def test_set_setting_to_leaders(self):
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
        for cat in num_options:
            self.assertEqual(
                len(self.fangraphs.get_options(cat)),
                num_options[cat],
                cat)
            self.assertTrue(
                all([
                    isinstance(o, bool) or bool(o)
                    for o in self.fangraphs.get_options(cat)]),
                self.fangraphs.get_options(cat))

        #User checks which options are currently selected
        sel_options = {
            "group": "Player Stats", "stats": "Batting",
            "league": "All Leagues", "team": "All Teams", "split_teams": False,
            "active_roster": False, "hof": False, "position": "All",
            "split": "Full Season", "min": "Qualified", "season": "2020",
            "split_season": False, "rookies": False, "season1": "2020",
            "season2": "2020", "age1": "14", "age2": "58"}
        for cat in sel_options:
            self.assertEqual(
                self.fangraphs.get_current(cat),
                sel_options[cat],
                cat)

        #User exports data on page
        self.fangraphs.export()
        self.assertTrue(os.path.exists(self.fangraphs.filenames[1]))

        self.fangraphs.end_task()

        os.remove(self.fangraphs.filenames[1])

if __name__ == '__main__':
    unittest.main()
