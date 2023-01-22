
# Python chess with minimax AI

## Simple and extremely buggy Chess with graphics and Minimax Algorithm for playing (AI)

## APPLICATION OF THE MINIMAX DECISION-MAKING METHOD IN GAME MODELS

### Authors: A.V. Saganenko, A.A. Kuksin, A.V. Dagaev

#### Saint Petersburg State University of Telecommunications

### Description

The project was created to prove the applicability of the Minimax method in game models. For this, work was carried out to formalize chess, develop the game itself in Python, and write an algorithm for the game based on the Minimax decision-making method. The algorithm uses game board weighting and the Alpha-Beta pruning optimization method.

### Launch conditions

Be sure to have packages listed in requirements.txt installed. Use any IDE able to interpret Python code. Launch from main.py.

``` python3
python main.py
```

### Packages list

* PyGame is used to visualize chess, chessboard.
* Numpy to effectively weight the board.
* Screeninfo to get information about display, so the game window will be fit in.

### Released algorithms

* PvP - player vs player
* Difficulty 0 - player vs random choice AI - 0.5 sec for solution
* Difficulty 1 - player vs best choice AI (best move, simple weighing) - 1 sec for solution
* Difficulty 2 - player vs best choice AI (Iterative Minimax depth 2 turn, advanced weighing) - 2-3 sec for solution
* Difficulty 3 - player vs best choice AI (Recursive Minimax depth 3 turn, advanced weighing, Alpha-Beta pruning) - 6-9 sec for solution

### Configuration

For configuration use config.txt

* game_mode=X (0 - PvP, 1 - PvE),
* difficulty=X (0, 1, 2, 3 - difficulty),
* visual_set=X (subfolder name - alternative visual set),
* freeze_time=X (0..10 - delay before game starts),
* time_restriction=X (0.5f..60000 - time limit)

### Ongoing unfixed bugs

* Player can eat enemy figure by king, and if this will lead to check, king will return to previous position (fixable)
