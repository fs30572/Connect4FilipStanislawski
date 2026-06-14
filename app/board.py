import copy

ROW_COUNT = 6
COL_COUNT = 7
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 4

_DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]
_SYMBOLS = {EMPTY: ".", PLAYER_PIECE: "X", AI_PIECE: "O"}


class Board:

    def __init__(self) -> None:
        self.grid: list[list[int]] = [[EMPTY] * COL_COUNT for _ in range(ROW_COUNT)]

    def is_valid_col(self, col: int) -> bool:
        return self.grid[0][col] == EMPTY

    def get_valid_cols(self) -> list[int]:
        return [c for c in range(COL_COUNT) if self.is_valid_col(c)]

    def drop_piece(self, col: int, piece: int) -> None:
        for row in range(ROW_COUNT - 1, -1, -1):
            if self.grid[row][col] == EMPTY:
                self.grid[row][col] = piece
                return

    def _check_line(self, r: int, c: int, dr: int, dc: int, piece: int) -> bool:
        return all(
            0 <= r + dr * i < ROW_COUNT
            and 0 <= c + dc * i < COL_COUNT
            and self.grid[r + dr * i][c + dc * i] == piece
            for i in range(WINDOW_LENGTH)
        )

    def check_winner(self, piece: int) -> bool:
        for r in range(ROW_COUNT):
            for c in range(COL_COUNT):
                for dr, dc in _DIRECTIONS:
                    if self._check_line(r, c, dr, dc, piece):
                        return True
        return False

    def is_terminal_node(self) -> bool:
        return (
            self.check_winner(PLAYER_PIECE)
            or self.check_winner(AI_PIECE)
            or not self.get_valid_cols()
        )

    def copy(self) -> "Board":
        new_board = Board()
        new_board.grid = copy.deepcopy(self.grid)
        return new_board

    def display(self) -> None:
        print("\n" + " ".join(str(c + 1) for c in range(COL_COUNT)))
        for row in self.grid:
            print(" ".join(_SYMBOLS[cell] for cell in row))
        print()
