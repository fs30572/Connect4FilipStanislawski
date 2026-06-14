import math

from app.ai import AI_DEPTH, minimax
from app.board import AI_PIECE, PLAYER_PIECE, Board


def _get_player_move(board: Board) -> int:
    valid_cols = board.get_valid_cols()
    while True:
        raw = input("Twój ruch (1–7) lub x aby wyjść: ")
        if raw.lower() == "x":
            exit()
        try:
            col = int(raw) - 1
        except ValueError:
            print("Podaj liczbę od 1 do 7 lub x aby wyjść.")
            continue
        if col in valid_cols:
            return col
        print(f"Kolumna {col + 1} jest zajęta lub nieprawidłowa. Wybierz inną.")


def _player_turn(board: Board) -> bool:
    col = _get_player_move(board)
    board.drop_piece(col, PLAYER_PIECE)
    return board.check_winner(PLAYER_PIECE)


def _ai_turn(board: Board) -> bool:
    col, _ = minimax(board, AI_DEPTH, -math.inf, math.inf, True)
    if col is not None:
        board.drop_piece(col, AI_PIECE)
        print(f"AI wybrało kolumnę {col + 1}.")
    return board.check_winner(AI_PIECE)


def run_game() -> None:
    board = Board()
    board.display()
    turn = PLAYER_PIECE

    while True:
        if turn == PLAYER_PIECE:
            won = _player_turn(board)
            winner_msg = "Wygrałeś! Gratulacje!"
        else:
            won = _ai_turn(board)
            winner_msg = "AI wygrało. Spróbuj ponownie!"

        board.display()

        if won:
            print(winner_msg)
            break

        if not board.get_valid_cols():
            print("Remis! Plansza jest pełna.")
            break

        turn = AI_PIECE if turn == PLAYER_PIECE else PLAYER_PIECE
