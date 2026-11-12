from chessmaker.chess.base import Player
from chessmaker.chess.pieces import King, Bishop, Knight, Queen
from extension.piece_right import Right
from extension.piece_pawn import Pawn_Q
from chessmaker.chess.base import Square

white = Player("white")
black = Player("black")

sample0 = [
        [Square(Knight(black)), Square(Queen(black)), Square(King(black)), Square(Bishop(black)), Square(Right(black))],
        [Square(Pawn_Q(black)), Square(Pawn_Q(black)), Square(Pawn_Q(black)), Square(Pawn_Q(black)),Square(Pawn_Q(black))],
        [Square(), Square(), Square(), Square(),Square()],
        [Square(Pawn_Q(white)), Square(Pawn_Q(white)), Square(Pawn_Q(white)), Square(Pawn_Q(white)),Square(Pawn_Q(white))],
        [Square(Right(white)), Square(Bishop(white)),  Square(King(white)), Square(Queen(white)), Square(Knight(white))],
        ]

sample1 = [
        [Square(Right(black)), Square(Queen(black)), Square(King(black)), Square(Knight(black)), Square(Bishop(black))],
        [Square(Pawn_Q(black)), Square(Pawn_Q(black)), Square(Pawn_Q(black)), Square(Pawn_Q(black)),Square(Pawn_Q(black))],
        [Square(), Square(), Square(), Square(),Square()],
        [Square(Pawn_Q(white)), Square(Pawn_Q(white)), Square(Pawn_Q(white)), Square(Pawn_Q(white)),Square(Pawn_Q(white))],
        [Square(Bishop(white)), Square(Knight(white)),  Square(King(white)), Square(Queen(white)), Square(Right(white))],
        ]

o = Square()
q = Square(Queen(black))
Q = Square(Queen(white))
k = Square(King(black))
K = Square(King(white))
b = Square(Bishop(black))
B = Square(Bishop(white))
r = Square(Right(black))
R = Square(Right(white))
n = Square(Knight(black))
N = Square(Knight(white))
p = Square(Pawn_Q(black))
P = Square(Pawn_Q(white))

hellsample = [
        [o,q,k,b,r],
        [p,p,n,p,p],
        [o,o,o,p,o],
        [P,P,P,P,P],
        [R,B,K,o,Q]
]