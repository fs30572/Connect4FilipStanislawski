# Connect 4 – AI Minimax

## Wymagania

- Python ≥ 3.14
- [`uv`](https://docs.astral.sh/uv/) – menadżer środowisk Python

## Instalacja i uruchomienie

```bash
# Klonowanie repozytorium
git clone <https://github.com/fs30572/Connect4FilipStanislawski>
cd connect4


# Instalacja
<.../connect4> uv venv
<.../connect4> uv pip install -e .
<.../connect4> uv sync --group dev
<.../connect4> uv pip install -e .

# Uruchomienie gry
<.../connect4> uv run connect4
```

## Uruchomienie testów

```bash
<>.../connect4> uv run pytest
```

## Sprawdzenie jakości kodu (linter)

```bash
<.../connect4>uv run ruff check app/ tests/
```

---

## Jak grać

Po uruchomieniu `uv run connect4` pojawi się plansza 6×7. Wpisz numer kolumny (1–7) i zatwierdź Enterem. AI odpowiada automatycznie.

```text
╔══════════════════════════════╗
║   Connect 4  –  AI Minimax   ║
║   Gracz (X)  vs  AI (O)      ║
╚══════════════════════════════╝

1 2 3 4 5 6 7
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .

Twój ruch (1–7):
```

| Symbol | Znaczenie |
|--------|-----------|
| `X`    | Gracz     |
| `O`    | AI        |
| `.`    | Puste pole|
