Jason Bere Cis 3700 A2

This assignment was written python version 3.9.7 to run it please use a compatible powershell


useful info:
    this program uses manual input from the user in the form of x and y coordinates to play
    in a 3x3 game the coordinate x = 0, y = 0 is the top left corner
    in a 3x3 game the coordinate x = 2, y = 0 is the top right corner
    in a 3x3 game the coordinate x = 0, y = 2 is the bottom left corner
    

basic usage:
    to play 2 player tic-tac-toe use the following command in project directory:
python tictactoe.py

advanced usage:
    the -n -u -p -d -s flags can be used to alter the game from its basic form and do the following
        -n
            followed by a space and an int 3, 4, 5 will change the size of the game board
        -u
            followed by a space and either "Util1" or "Util2" will specify the utility function
            "Util1" for basic utility and "Util2" for advanced utility
        -p
            followed by a space and a 1 or a 2 can specify whether the player goes first or second
        -d
            followed by a space and a value 1,2,3,4,5,6,7,8, or 9 alters the depth of the search
        -s
            followed by a space and either "MiniMax" or "AlphaBeta" specifies the search algorithm  

Assignment inputs:
Q1:

python tictactoe.py -n 3 -s MinMax -u Util1 -d 9

python tictactoe.py -n 3 -s AlphaBeta -u Util1 -d 9

python tictactoe.py -n 3 -s MinMax -u Util2 -d 9

python tictactoe.py -n 3 -s AlphaBeta -u Util2 -d 9


python tictactoe.py -n 4 -s MinMax -u Util1 -d 5

python tictactoe.py -n 4 -s AlphaBeta -u Util1 -d 5

python tictactoe.py -n 4 -s AlphaBeta -u Util1 -d 7

python tictactoe.py -n 4 -s MinMax -u Util2 -d 5

python tictactoe.py -n 4 -s AlphaBeta -u Util2 -d 5

python tictactoe.py -n 4 -s AlphaBeta -u Util2 -d 7



python tictactoe.py -n 5 -s MinMax -u Util1 -d 3

python tictactoe.py -n 5 -s AlphaBeta -u Util1 -d 3

python tictactoe.py -n 5 -s AlphaBeta -u Util1 -d 4

python tictactoe.py -n 5 -s MinMax -u Util2 -d 3

python tictactoe.py -n 5 -s AlphaBeta -u Util2 -d 3

python tictactoe.py -n 5 -s AlphaBeta -u Util2 -d 4


Q2:

python tictactoe.py -n 3 -s AlphaBeta -u Util2 -d 9

python tictactoe.py -n 4 -s AlphaBeta -u Util2 -d 7

python tictactoe.py -n 5 -s AlphaBeta -u Util2 -d 4