import _collections


class Referee:
    """
    :return tuple of surrounded dots and free dots
    """

    @staticmethod
    def check_surrounded(game_matrix, current_color):
        surrounded = set()
        active = set()
        checking_not_complete = True
        for x in range(len(game_matrix)):
            for y in range(len(game_matrix[0])):
                if game_matrix[x][y].color == current_color:
                    continue
                if (x, y) in surrounded.union(active):
                    continue
                if Referee.is_boundary(game_matrix, x, y):
                    active.add((x, y))
                    continue
                checking_not_complete = True
                current_dots = _collections.deque()
                current_dots.append((x, y))
                visited = set()
                while len(current_dots) > 0 and checking_not_complete:
                    current = current_dots.pop()
                    visited.add(current)
                    neighbours = Referee.get_neighbours(game_matrix, current_color, current[0], current[1], visited)
                    for dot in neighbours:
                        if dot == (-1, -1):
                            active = active.union(visited)
                            checking_not_complete = False
                            break
                        current_dots.append(dot)
                if checking_not_complete:
                    surrounded = surrounded.union(visited)

        return surrounded, active

    @staticmethod
    def get_neighbours(game_matrix, color, x, y, visited):
        result = set()
        outer_grounded = Referee.get_diagonal_through_opponent(game_matrix, color, x, y)
        for i in range(-1, 2):
            for j in range(-1, 2):
                x_n = x + i
                y_n = y + j
                if (x_n, y_n) in outer_grounded or game_matrix[x_n][y_n].color == color:
                    continue
                if Referee.is_boundary(game_matrix, x_n, y_n):
                    return [(-1, -1)]
                elif not (x_n, y_n) in visited:
                    result.add((x_n, y_n))

        return result

    @staticmethod
    def is_boundary(game_matrix, x, y):
        w = len(game_matrix) - 1
        h = len(game_matrix[0]) - 1
        return x == 0 or x == w or y == 0 or y == h

    @staticmethod
    def get_diagonal_through_opponent(game_matrix, color, x, y):
        result = set()
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                if game_matrix[x + i][y].color == color and game_matrix[x][y + j].color == color:
                    result.add((x + i, y + j))

        return result
