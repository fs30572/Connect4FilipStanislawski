from app.board import AI_PIECE, EMPTY, PLAYER_PIECE, Board


def test_board_initial_state():
    board = Board()
    for row in board.grid:
        assert all(cell == EMPTY for cell in row)


def test_drop_piece_lands_at_bottom():
    board = Board()
    board.drop_piece(0, PLAYER_PIECE)
    assert board.grid[5][0] == PLAYER_PIECE


def test_drop_piece_stacks():
    board = Board()
    board.drop_piece(0, PLAYER_PIECE)
    board.drop_piece(0, AI_PIECE)
    assert board.grid[4][0] == AI_PIECE


def test_is_valid_col_full_column():
    board = Board()
    for _ in range(6):
        board.drop_piece(0, PLAYER_PIECE)
    assert not board.is_valid_col(0)


def test_get_valid_cols_full_board():
    board = Board()
    for c in range(7):
        for _ in range(6):
            board.drop_piece(c, PLAYER_PIECE)
    assert board.get_valid_cols() == []


def test_check_winner_horizontal():
    board = Board()
    for c in range(4):
        board.drop_piece(c, PLAYER_PIECE)
    assert board.check_winner(PLAYER_PIECE)


def test_check_winner_vertical():
    board = Board()
    for _ in range(4):
        board.drop_piece(0, AI_PIECE)
    assert board.check_winner(AI_PIECE)


def test_check_winner_diagonal():
    board = Board()
    for col in range(4):
        for _ in range(col):
            board.drop_piece(col, AI_PIECE)
        board.drop_piece(col, PLAYER_PIECE)
    assert board.check_winner(PLAYER_PIECE)


def test_no_false_winner():
    board = Board()
    board.drop_piece(0, PLAYER_PIECE)
    board.drop_piece(0, AI_PIECE)
    assert not board.check_winner(PLAYER_PIECE)
    assert not board.check_winner(AI_PIECE)


def test_is_terminal_node_win():
    board = Board()
    for c in range(4):
        board.drop_piece(c, AI_PIECE)
    assert board.is_terminal_node()


def test_is_terminal_node_empty_board():
    board = Board()
    assert not board.is_terminal_node()


def test_copy_is_independent():
    board = Board()
    board.drop_piece(0, PLAYER_PIECE)
    clone = board.copy()
    clone.drop_piece(1, AI_PIECE)
    assert board.grid[5][1] == EMPTY


def test_display_output(capsys):
    board = Board()
    board.display()
    captured = capsys.readouterr()
    assert "1 2 3 4 5 6 7" in captured.out
