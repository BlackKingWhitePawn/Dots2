import unittest

from tests.dot import Dot
from gameTools.referee import Referee

FIELD_1 = [
    [Dot(color='gray'), Dot(color='red'), Dot(color='gray')],
    [Dot(color='red'), Dot(color='blue'), Dot(color='red')],
    [Dot(color='gray'), Dot(color='red'), Dot(color='gray')],
]


class TestCheckSurrounded(unittest.TestCase):
    def _check(self, resulted_set, actual_set):
        self.assertSetEqual(resulted_set, actual_set)

    def test_romb(self):
        self._check({(1, 1)}, Referee.check_surrounded([
            [Dot(color='gray'), Dot(color='red'), Dot(color='gray')],
            [Dot(color='red'), Dot(color='blue'), Dot(color='red')],
            [Dot(color='gray'), Dot(color='red'), Dot(color='gray')]], 'red')[0])
        self._check({(1, 1)}, Referee.check_surrounded([
            [Dot(color='blue'), Dot(color='red'), Dot(color='gray')],
            [Dot(color='red'), Dot(color='blue'), Dot(color='red')],
            [Dot(color='gray'), Dot(color='red'), Dot(color='gray')]], 'red')[0])

    def test_empty(self):
        self._check(set(), Referee.check_surrounded([[]], 'red')[0])

    def test_one_dot(self):
        self._check(set(), Referee.check_surrounded([[Dot(color='red')]], 'red')[0])

    def test_grounded(self):
        self._check(set(), Referee.check_surrounded([
            [Dot(color='red'), Dot(color='blue'), Dot(color='red')],
            [Dot(color='red'), Dot(color='blue'), Dot(color='red')],
            [Dot(color='gray'), Dot(color='red'), Dot(color='gray')]], 'red')[0])
        self._check(set(), Referee.check_surrounded([
            [Dot(color='red'), Dot(color='red'), Dot(color='red'), Dot(color='red')],
            [Dot(color='blue'), Dot(color='blue'), Dot(color='red'), Dot(color='red')],
            [Dot(color='red'), Dot(color='red'), Dot(color='red'), Dot(color='red')],
            [Dot(color='gray'), Dot(color='red'), Dot(color='gray'), Dot(color='red')]], 'red')[0])

    def test_inside(self):
        self._check({(1, 2), (2, 1), (2, 3), (3, 2)}, Referee.check_surrounded([
            [Dot(color='gray'), Dot(color='gray'), Dot(color='blue'), Dot(color='gray'), Dot(color='gray')],
            [Dot(color='gray'), Dot(color='blue'), Dot(color='red'), Dot(color='blue'), Dot(color='gray')],
            [Dot(color='blue'), Dot(color='red'), Dot(color='blue'), Dot(color='red'), Dot(color='blue')],
            [Dot(color='gray'), Dot(color='blue'), Dot(color='red'), Dot(color='blue'), Dot(color='gray')],
            [Dot(color='gray'), Dot(color='gray'), Dot(color='blue'), Dot(color='gray'), Dot(color='gray')]], 'blue')[0])
