#! python
# test_class_fangraphs.py

import unittest

import bs4
import requests

class TestClassFanGraphs(unittest.TestCase):
    def test_addresses(self):
        addresses = (
            "https://fangraphs.com/leaders.aspx",
            "https://fangraphs.com/projections.aspx")
        results = []
        for address in addresses:
            res = requests.get(address)
            results.append(res.status_code == 200)
        self.assertTrue(all(results))
