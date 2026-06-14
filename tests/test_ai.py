import math

from app.ai import minimax, score_position, score_window
from app.board import AI_PIECE, EMPTY, PLAYER_PIECE, Board


def test_score_window_four_in_row():
    window = [AI_PIECE, AI_PIECE, AI_PIECE, AI_PIECE]
    assert score_window(window, AI_PIECE) == 100


def test_score_window_three_and_empty():
    window = [AI_PIECE, AI_PIECE, AI_PIECE, EMPTY]
    assert score_window(window, AI_PIECE) == 5


def test_score_window_blocks_opponent():
    window = [PLAYER_PIECE, PLAYER_PIECE, PLAYER_PIECE, EMPTY]
    assert score_window(window, AI_PIECE) < 0


def test_score_position_empty_board():
    board = Board()
    assert score_position(board, AI_PIECE) == 0


def test_minimax_picks_winning_move():
    """AI must take the winning move when it can win in one step."""
    board = Board()
    for _ in range(3):
        board.drop_piece(0, AI_PIECE)   # 3 AI pieces vertically in col 0
    board.drop_piece(6, PLAYER_PIECE)   # player piece out of the way
    col, _ = minimax(board, 1, -math.inf, math.inf, True)
    assert col == 0


def test_minimax_blocks_opponent():
    """AI must block the player who has three in a row."""
    board = Board()
    for c in range(3):
        board.drop_piece(c, PLAYER_PIECE)  # player: row 5, cols 0-1-2
    board.drop_piece(6, AI_PIECE)          # single AI piece, no win available
    col, _ = minimax(board, 3, -math.inf, math.inf, True)
    assert col == 3


def test_minimax_returns_valid_column():
    board = Board()
    col, score = minimax(board, 3, -math.inf, math.inf, True)
    assert col in board.get_valid_cols()
    assert isinstance(score, float)


def test_minimax_terminal_ai_wins():
    """Score must be very high when AI has already won."""
    board = Board()
    for c in range(4):
        board.drop_piece(c, AI_PIECE)
    _, score = minimax(board, 3, -math.inf, math.inf, False)
    assert score > 0
