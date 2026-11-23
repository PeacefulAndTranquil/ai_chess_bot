from enum import Enum
from chessmaker.chess.base import Player, Board, Position
from chessmaker.chess.pieces import King, Bishop, Knight, Queen, Pawn
from extension.piece_right import Right
from extension.piece_pawn import Pawn_Q
from chessmaker.chess.base import Square
from samples import *






class Piece:
    def __init__(self,piecetype,player):
        self.piecetype = piecetype
        self.player = player

class PieceType(Enum):
    PAWN = 0
    KNIGHT = 1
    RIGHT = 2
    BISHOP = 3
    QUEEN = 4
    KING = 5

class Player(Enum):
    WHITE = 0
    BLACK = 1

class Move:
    def __init__(self,piec:Piece,pos:(int,int),dest:(int,int),capt:PieceType|None,prom:PieceType|None):
        self.piece = piec
        self.position = pos
        self.destination = dest
        self.captured = capt
        self.promotion = prom


class Board:
    _chessmakerPieceConverter =  {"Pawn":PieceType.PAWN, "Knight":PieceType.KNIGHT, "Right":PieceType.RIGHT, "Bishop":PieceType.BISHOP, "Queen":PieceType.QUEEN, "King":PieceType.KING}
    _chessmakerColourConverter = {"white":Player.WHITE, "black":Player.BLACK}
    def __init__(self, inputboard):
        #raise NotImplemented
        s = len(inputboard)
        self.board = [[None for x in range(s)] for y in range(s)]
        for i in range(s):
            for j in range(s):
                p = inputboard[i][j].piece
                if p is not None:
                    t = self._chessmakerPieceConverter[p.name]
                    c = self._chessmakerColourConverter[p.player.name]
                    self.board[i][j] = Piece(t,c)

    _prettyprintdict = {PieceType.PAWN:"P",PieceType.RIGHT:"R",PieceType.KNIGHT:"N",PieceType.BISHOP:"B",PieceType.QUEEN:"Q",PieceType.KING:"K"}
    def prettyprint(self):
        s = len(self.board)
        for i in range(s):
            str = ""
            for j in range(s):
                p = self.board[i][j]
                if p is None:
                    str = str + "  "
                elif p.player == Player.WHITE:
                    str = str + self._prettyprintdict[p.piecetype] + " "
                else:
                    str = str + self._prettyprintdict[p.piecetype].lower() + " "
            print(str)


    def piecemoves(self) -> [Move]:
        """returns a list of tuples formatted like:
        piece, piece position, piece destination, captured piece"""
        s = len(self.board)
        o = []
        for i in range(s):
            for j in range(s):
                p = self.board[i][j]
                if p is not None:
                    match p.piecetype:
                        case PieceType.PAWN:
                            if p.player==Player.WHITE and i==s-2:
                                o += Move(p,)


b = Board(sample0)
b.prettyprint()