Raport – Connect 4 AI (Minimax z Alpha-Beta Pruning)

1. Opis problemu

Celem projektu jest stworzenie agenta AI zdolnego do gry w **Connect 4** (Cztery w rzędzie)
na wysokim poziomie. Gra toczy się na planszy 6×7, gdzie dwóch graczy na przemian wrzuca
żetony do wybranych kolumn. Żeton spada na najniższe wolne miejsce. Wygrywa ten, kto jako
pierwszy ułoży cztery żetony w rzędzie – poziomo, pionowo lub po skosie.

Problem należy do klasy **gier dwuosobowych o sumie zerowej z pełną informacją** –
każdy gracz widzi cały stan planszy, a zysk jednej strony jest stratą drugiej. Jest to
klasyczny przypadek dla algorytmu **Minimax**.

---
2. Opis danych

Projekt nie korzysta z zewnętrznych zbiorów danych. Stan gry jest w pełni opisany przez
planszę 6×7 (42 komórki), gdzie każda komórka przyjmuje wartość:
- `0` – puste pole
- `1` – żeton gracza
- `2` – żeton AI

Dane wejściowe to ruch gracza (numer kolumny 1–7). Dane wyjściowe to ruch AI
wyznaczony przez algorytm Minimax.

---
3. Uzasadnienie wyboru algorytmu

**Minimax** jest algorytmem dedykowanym do gier dwuosobowych o sumie zerowej.
Modeluje grę jako drzewo decyzji, gdzie jeden gracz maksymalizuje swój wynik (AI),
a drugi minimalizuje go (człowiek). Dla Connect 4 istnieje skończone drzewo gry,
co czyni Minimax bezpośrednio stosowalnym.

**Dlaczego nie inne algorytmy?**

| Algorytm | Problem |
|----------|---------|
| BFS / DFS | Nie obsługują naturalnie gier z dwoma graczami |
| Perceptron / Sieć neuronowa | Wymagają danych treningowych, trudniejsze do weryfikacji |
| A* | Dedykowany do pathfindingu, nie do gier strategicznych |
| **Minimax + Alpha-Beta** | Idealny dla gier 2-osobowych, deterministyczny, łatwy do analizy |

**Alpha-Beta pruning** redukuje liczbę węzłów do przeszukania z O(b^d) do O(b^(d/2)),
pozwalając na głębsze przeszukiwanie w tym samym czasie bez utraty jakości decyzji.

---

4. Wyjaśnienie działania metody
4.1 Minimax

Algorytm buduje drzewo decyzji do zadanej głębokości (`AI_DEPTH = 5`).
W węzłach terminalnych przypisywany jest wynik:

| Stan | Wynik |
|------|-------|
| AI wygrywa | +1 000 000 |
| Gracz wygrywa | −1 000 000 |
| Remis | 0 |
| Limit głębokości | wynik heurystyczny |

Węzeł **maksymalizujący** (AI) wybiera ruch dający najwyższy wynik.
Węzeł **minimalizujący** (gracz) wybiera ruch dający najniższy wynik.

4.2 Alpha-Beta Pruning

Parametry α i β ograniczają zakres poszukiwań:
- **α** – najlepsza wartość gwarantowana dla AI (maksimum)
- **β** – najlepsza wartość gwarantowana dla gracza (minimum)

Jeśli w danej gałęzi `α ≥ β`, dalsza eksploracja jest zbędna – gałąź jest odcinana.

4.3 Funkcja heurystyczna (`score_position`)

Ocena stanu planszy przy limicie głębokości:

- **Preferencja środkowej kolumny**: +3 za każdy żeton AI w kolumnie 3
  (centrum daje więcej możliwości łączenia)
- **Ocena okien 4-komórkowych** we wszystkich kierunkach (→, ↓, ↘, ↙):

| Zawartość okna | Punkty |
|----------------|--------|
| 4 × AI | +100 |
| 3 × AI + puste | +5 |
| 2 × AI + 2 puste | +2 |
| 3 × Gracz + puste | −4 |

---

5. Opis przeprowadzonych testów

Projekt zawiera **21 testów jednostkowych** (`pytest`) w dwóch modułach:

`tests/test_board.py` (13 testów)

| Test | Co sprawdza |
|------|-------------|
| `test_board_initial_state` | Pusta plansza po inicjalizacji |
| `test_drop_piece_lands_at_bottom` | Żeton spada na dno kolumny |
| `test_drop_piece_stacks` | Żetony układają się w stos |
| `test_is_valid_col_full_column` | Pełna kolumna jest niedostępna |
| `test_get_valid_cols_full_board` | Brak wolnych kolumn na pełnej planszy |
| `test_check_winner_horizontal` | Wykrywanie wygranej poziomej |
| `test_check_winner_vertical` | Wykrywanie wygranej pionowej |
| `test_check_winner_diagonal` | Wykrywanie wygranej po skosie |
| `test_no_false_winner` | Brak fałszywych wygranych |
| `test_is_terminal_node_win` | Terminal node po wygranej |
| `test_is_terminal_node_empty_board` | Pusta plansza nie jest terminalem |
| `test_copy_is_independent` | Kopia planszy jest niezależna |
| `test_display_output` | Poprawny format wyświetlania |

`tests/test_ai.py` (8 testów)

| Test | Co sprawdza |
|------|-------------|
| `test_score_window_four_in_row` | 4 × AI = 100 punktów |
| `test_score_window_three_and_empty` | 3 × AI + puste = 5 punktów |
| `test_score_window_blocks_opponent` | 3 × Gracz = ujemny wynik |
| `test_score_position_empty_board` | Pusta plansza = 0 punktów |
| `test_minimax_picks_winning_move` | AI wybiera natychmiastową wygraną |
| `test_minimax_blocks_opponent` | AI blokuje groźbę gracza |
| `test_minimax_returns_valid_column` | Minimax zwraca legalną kolumnę |
| `test_minimax_terminal_ai_wins` | Wynik terminalny dla wygranej AI |

---

6. Uzyskane wyniki

| Metryka | Wynik |
|---------|-------|
| Testy jednostkowe | 21 / 21 ✅ |
| Pokrycie kodu (`app/`) | ~88% |
| Walidacja ruff | 0 błędów ✅ |
| Czas ruchu AI (głębokość 5) | < 2 s |
| AI vs losowy gracz (100 gier) | 100% wygranych |

---

7. Wnioski

Algorytm Minimax z Alpha-Beta pruning doskonale sprawdza się w grach deterministycznych
o pełnej informacji. Przy głębokości 5 AI jest bardzo silnym przeciwnikiem – blokuje
zagrożenia i szuka wieloruchowych kombinacji wygrywających.

Heurystyka oceniająca okna 4-komórkowe okazała się wystarczająca do osiągnięcia
wysokiej jakości gry przy umiarkowanym czasie obliczeń.

**Możliwe usprawnienia:**
- Zwiększenie głębokości przeszukiwania kosztem czasu obliczeniowego
- Iteracyjne pogłębianie (IDDFS) z limitem czasu na ruch
- Tablica transpozycji (cache stanów planszy) – znaczne przyspieszenie
- Lepsza kolejność sprawdzania ruchów (najpierw środkowe kolumny)
