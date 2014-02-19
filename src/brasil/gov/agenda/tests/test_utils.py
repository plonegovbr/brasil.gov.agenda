# -*- coding: utf-8 -*-

from brasil.gov.agenda import utils
from datetime import date

import unittest


class TestUtils(unittest.TestCase):
    """ Testa funcoes do utils. Nao testamos as traducoes """

    def setUp(self):
        self.date = date(2014, 2, 19)

    def test_weekday_abbr(self):
        expected = 'wed'
        self.assertEqual(utils.weekday_abbr(self.date),
                         expected)

    def test_month_abbr(self):
        expected = 'feb'
        self.assertEqual(utils.month_abbr(self.date),
                         expected)

    def test_translate_weekday(self):
        expected = 'weekday_wed'
        self.assertEqual(utils.translate_weekday(self.date),
                         expected)

    def test_translate_month(self):
        expected = 'month_feb'
        self.assertEqual(utils.translate_month(self.date),
                         expected)

    def test_format_date(self):
        expected = 'weekday_wed, 19 de month_feb de 2014'
        self.assertEqual(utils.format_date(self.date),
                         expected)
