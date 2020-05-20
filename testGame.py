from game import Game as t
import unittest


class TestFindChain(unittest.TestCase):
    def test_rhombus(self):
        game = t((3, 3))
        game.game_matrix[0][1].change_color('Red')
        game.game_matrix[1][0].change_color('Red')
        game.game_matrix[1][2].change_color('Red')
        game.game_matrix[2][1].change_color('Red')

        self.assertTrue(game.get_chain((0, 1)) in [
            [(0, 1), (1, 2), (2, 1), (1, 0)],
            [(0, 1), (1, 0), (2, 1), (1, 2)]
        ])

    def test_square(self):
        game = t((2, 2))
        game.game_matrix[0][0].change_color('Red')
        game.game_matrix[1][0].change_color('Red')
        game.game_matrix[1][1].change_color('Red')
        game.game_matrix[0][1].change_color('Red')

        self.assertTrue(game.get_chain((0, 1)) in [
            [(0, 1), (1, 1), (1, 0), (0, 0)],
            [(0, 1), (0, 0), (1, 0), (1, 1)],
            [(0, 1), (1, 1)],
            [(0, 0), (1, 1)]
        ])


class TestGetNeighbours(unittest.TestCase):
    def _check(self, field, dot, chain):
        self.assertSetEqual(t(field).get_neighbours(dot), chain)

    def test_one_dot(self):
        self._check((1, 1), (0, 0), set())

    def test_double_double(self):
        self._check((2, 2), (0, 0), {(0, 1), (1, 0), (1, 1)})
        self._check((2, 2), (1, 1), {(0, 1), (1, 0), (0, 0)})
        self._check((2, 2), (1, 0), {(0, 1), (0, 0), (1, 1)})
        self._check((2, 2), (0, 1), {(0, 0), (1, 0), (1, 1)})

    def test_three_three(self):
        self._check((3, 3), (1, 1), {
            (0, 0), (0, 1), (0, 2),
            (1, 0),         (1, 2),
            (2, 0), (2, 1), (2, 2)})
