import math
import secrets

from app.board import AI_PIECE, COL_COUNT, EMPTY, PLAYER_PIECE, ROW_COUNT, WINDOW_LENGTH, Board

AI_DEPTH = 5


def score_window(window: list[int], piece: int) -> int:
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE
    count = window.count(piece)
    empty = window.count(EMPTY)
    opp_count = window.count(opp_piece)
    score = 0

    if count == 4:
        score += 100
    elif count == 3 and empty == 1:
        score += 5
    elif count == 2 and empty == 2:
        score += 2

    if opp_count == 3 and empty == 1:
        score -= 4

    return score


def _score_direction(board: Board, piece: int, dr: int, dc: int) -> int:
    score = 0
    for r in range(ROW_COUNT):
        for c in range(COL_COUNT):
            window = []
            for i in range(WINDOW_LENGTH):
                nr, nc = r + dr * i, c + dc * i
                if 0 <= nr < ROW_COUNT and 0 <= nc < COL_COUNT:
                    window.append(board.grid[nr][nc])
            if len(window) == WINDOW_LENGTH:
                score += score_window(window, piece)
    return score


def score_position(board: Board, piece: int) -> int:
    center_col = [board.grid[r][COL_COUNT // 2] for r in range(ROW_COUNT)]
    score = center_col.count(piece) * 3

    for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
        score += _score_direction(board, piece, dr, dc)

    return score


def _terminal_score(board: Board) -> float | None:
    if board.check_winner(AI_PIECE):
        return 1_000_000.0
    if board.check_winner(PLAYER_PIECE):
        return -1_000_000.0
    if not board.get_valid_cols():
        return 0.0
    return None


def minimax(  # noqa: C901
    board: Board,
    depth: int,
    alpha: float,
    beta: float,
    maximizing: bool,
) -> tuple[int | None, float]:
    terminal = _terminal_score(board)
    if terminal is not None:
        return None, terminal
    if depth == 0:
        return None, float(score_position(board, AI_PIECE))

    valid_cols = board.get_valid_cols()
    best_col: int = secrets.choice(valid_cols)

    if maximizing:
        value = -math.inf
        for col in valid_cols:
            new_board = board.copy()
            new_board.drop_piece(col, AI_PIECE)
            _, new_score = minimax(new_board, depth - 1, alpha, beta, False)
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value

    value = math.inf
    for col in valid_cols:
        new_board = board.copy()
        new_board.drop_piece(col, PLAYER_PIECE)
        _, new_score = minimax(new_board, depth - 1, alpha, beta, True)
        if new_score < value:
            value = new_score
            best_col = col
        beta = min(beta, value)
        if alpha >= beta:
            break
    return best_col, value
