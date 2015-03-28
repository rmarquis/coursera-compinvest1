__author__ = 'baio'

import unittest

from w7 import tech_analizer
import datetime as dt

class TestTechAnalisers(unittest.TestCase):

    def test_bollinger_aapl_20(self):
        dt_start = dt.datetime(2008, 1, 1)
        dt_end = dt.datetime(2009, 12, 31)
        tech_analizer.bollinger(dt_start, dt_end, ["AAPL"], 20)

    def test_bollinger_msft_20(self):
        dt_start = dt.datetime(2008, 1, 1)
        dt_end = dt.datetime(2009, 12, 31)
        tech_analizer.bollinger(dt_start, dt_end, ["MSFT"], 20)

if __name__ == '__main__':
    unittest.main()