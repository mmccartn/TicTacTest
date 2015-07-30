# TicTacTest
A simple tictactoe game with computer opponent and accompanying unittest tests

### Purpose
I wrote this as a primer to python's unittest library, while following along to Ned Batchelder's awesome PyCon14 talk: [Getting Started Testing](https://youtu.be/FxSsnHeWQBY). Why TicTacToe? Well, I've noticed that it comes up quite often during oral exams. YRMV.

#### TL;DW Ned's talk
* Testing is important and can save you time
* It's is non-trivial, though easier than debugging
* `unittest` is a basic testing tool for python, but its the standard, with a JUnit-like interface
* Use inheritance in designing your tests to avoid boilerplate
* For external dependencies, `mock` can be used to make a non-deterministic method predicable
* `coverage` can be used to give you an idea of how much of the source file gets tested
* Don't be ashamed of having to test tests written in a Don't Repeat Yourself (DRY) manner 


### Usage:
#### Playing
Simply run `tictactoe.py` and follow onscreen instructions

Either you (x's) or the computer (o's) will get a chance to place your marker on the board first, depending on the results of a coin flip.

Specify the row and column you wish to place your maker.

The game terminates when someone has won (3 in a row horizontally, vertically, or diagonally), or a stalemate has occured.

Here's a demo:
```
_______
| , , |
| , , |
| , , |
¯¯¯¯¯¯¯
Player x's turn.
Row: 1
Column: 1
_______
| , , |
| ,x, |
| , , |
¯¯¯¯¯¯¯
Player o's turn.
_______
|o, , |
| ,x, |
| , , |
¯¯¯¯¯¯¯
Player x's turn.
Row: 1
Column: 0
_______
|o, , |
|x,x, |
| , , |
¯¯¯¯¯¯¯
Player o's turn.
_______
|o, , |
|x,x, |
|o, , |
¯¯¯¯¯¯¯
Player x's turn.
Row: 1
Column: 2
_______
|o, , |
|x,x,x|
|o, , |
¯¯¯¯¯¯¯
Player x has won.
```

#### Testing
The unittest command line interface can be invoked with:
`unittest -b test_tictactoe`
Output should look something like this:
```
.....................
----------------------------------------------------------------------
Ran 21 tests in 0.002s
```
