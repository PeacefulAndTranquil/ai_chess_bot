from itertools import cycle
from extension.board_utils import print_board_ascii

from chessmaker.chess.base import Player, Board
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

# o = Square()
# q = Square(Queen(black))
# Q = Square(Queen(white))
# k = Square(King(black))
# K = Square(King(white))
# b = Square(Bishop(black))
# B = Square(Bishop(white))
# r = Square(Right(black))
# R = Square(Right(white))
# n = Square(Knight(black))
# N = Square(Knight(white))
# p = Square(Pawn_Q(black))
# P = Square(Pawn_Q(white))

hellsample = [
        [Square(),Square(Queen(black)),Square(King(black)),Square(Bishop(black)),Square(Right(black))],
        [Square(Pawn_Q(black)),Square(Pawn_Q(black)),Square(Knight(black)),Square(Pawn_Q(black)),Square(Pawn_Q(black))],
        [Square(),Square(),Square(),Square(Pawn_Q(black)),Square()],
        [Square(Pawn_Q(white)),Square(Pawn_Q(white)),Square(Pawn_Q(white)),Square(Pawn_Q(white)),Square(Pawn_Q(white))],
        [Square(Right(white)),Square(Bishop(white)),Square(King(white)),Square(),Square(Queen(white))]
]
justaqueens = [
        [Square(),Square(),Square(),Square(),Square(Queen(black))],
        [Square(),Square(),Square(),Square(Pawn_Q(white)),Square()],
        [Square(),Square(),Square(Queen(white)),Square(),Square()],
        [Square(),Square(),Square(),Square(),Square()],
        [Square(),Square(),Square(),Square(),Square()],
]

inchecksample = [
        [Square(),Square(),Square(),Square(),Square()],
        [Square(),Square(),Square(),Square(),Square()],
        [Square(King(black)),Square(),Square(),Square(),Square(Queen(white))],
        [Square(),Square(),Square(),Square(),Square()],
        [Square(),Square(),Square(),Square(),Square()],
]

failsample = [
[Square(Knight(black)),Square(Queen(black)),Square(),Square(),Square()],
[Square(),Square(Pawn_Q(white)),Square(King(black)),Square(),Square()],
[Square(Pawn_Q(black)),Square(Pawn_Q(black)),Square(Pawn_Q(white)),Square(),Square(Pawn_Q(black))],
[Square(),Square(),Square(Bishop(black)),Square(),Square(Pawn_Q(white))],
[Square(),Square(),Square(),Square(),Square(King(white))]
]

timeoutsample = [
[Square(),Square(Queen(black)),Square(King(black)),Square(),Square(Right(black))],
[Square(Pawn_Q(black)),Square(),Square(Knight(black)),Square(Pawn_Q(black)),Square()],
[Square(Pawn_Q(white)),Square(Bishop(black)),Square(),Square(),Square(Pawn_Q(white))],
[Square(),Square(Pawn_Q(black)),Square(Bishop(white)),Square(),Square(Pawn_Q(black))],
[Square(),Square(King(white)),Square(),Square(Queen(white)),Square()]
]

d4failsample = [
[Square(),Square(Queen(black)),Square(King(black)),Square(Bishop(black)),Square()],
[Square(Pawn_Q(black)),Square(),Square(Knight(black)),Square(Pawn_Q(black)),Square()],
[Square(Pawn_Q(black)),Square(Pawn_Q(black)),Square(),Square(Queen(white)),Square(Pawn_Q(black))],
[Square(),Square(Pawn_Q(white)),Square(Pawn_Q(white)),Square(),Square(Pawn_Q(white))],
[Square(),Square(Bishop(white)),Square(),Square(King(white)),Square(Knight(white))]
]

falsecheckmatesample = [
[Square(),Square(Queen(black)),Square(King(black)),Square(),Square()],
[Square(Pawn_Q(black)),Square(Pawn_Q(black)),Square(Queen(white)),Square(),Square()],
[Square(Pawn_Q(white)),Square(),Square(),Square(Queen(white)),Square(Right(black))],
[Square(Bishop(white)),Square(King(white)),Square(),Square(),Square(Pawn_Q(white))],
[Square(),Square(),Square(),Square(),Square(Knight(white))]
]


def string2board(s):
        s=s.replace("[o","[Square()")
        s=s.replace(",o",",Square()")
        s=s.replace("[q","[Square(Queen(black))")
        s=s.replace(",q",",Square(Queen(black))")
        s=s.replace("[Q","[Square(Queen(white))")
        s=s.replace(",Q",",Square(Queen(white))")
        s=s.replace("[n", "[Square(Knight(black))")
        s=s.replace(",n", ",Square(Knight(black))")
        s=s.replace("[N", "[Square(Knight(white))")
        s=s.replace(",N", ",Square(Knight(white))")
        s=s.replace("[r", "[Square(Right(black))")
        s=s.replace(",r", ",Square(Right(black))")
        s=s.replace("[R", "[Square(Right(white))")
        s=s.replace(",R", ",Square(Right(white))")
        s=s.replace("[b", "[Square(Bishop(black))")
        s=s.replace(",b", ",Square(Bishop(black))")
        s=s.replace("[B", "[Square(Bishop(white))")
        s=s.replace(",B", ",Square(Bishop(white))")
        s=s.replace("[k", "[Square(King(black))")
        s=s.replace(",k", ",Square(King(black))")
        s=s.replace("[K", "[Square(King(white))")
        s=s.replace(",K", ",Square(King(white))")
        s=s.replace("[p", "[Square(Pawn_Q(black))")
        s=s.replace(",p", ",Square(Pawn_Q(black))")
        s=s.replace("[P", "[Square(Pawn_Q(white))")
        s=s.replace(",P", ",Square(Pawn_Q(white))")
        return s

fuck = [
[Square(),Square(King(black)),Square(),Square(Bishop(black)),Square(Right(black))],
[Square(),Square(),Square(),Square(Pawn_Q(white)),Square()],
[Square(Knight(black)),Square(),Square(),Square(),Square()],
[Square(),Square(),Square(Pawn_Q(black)),Square(),Square()],
[Square(Queen(black)),Square(Bishop(white)),Square(King(white)),Square(),Square()]
]

if __name__ == "__main__":
        print("wow")
        b = Board(hellsample, [white,black], cycle([white,black]))
        print_board_ascii(b)
        ps = b.get_player_pieces(white)
        for p in ps:
                print(p)
        funny = ("[\n"
                 "[o,k,o,b,r],\n"
                 "[o,o,o,P,o],\n"
                 "[n,o,o,o,o],\n"
                 "[o,o,p,o,o],\n"
                 "[q,B,K,o,o]\n"
                 "]")
        print(string2board(funny))