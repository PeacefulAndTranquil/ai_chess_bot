from enum import Enum, IntEnum
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

class Player(IntEnum):
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
        self.board = [[Piece(None,None) for x in range(s)] for y in range(s)]
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
                if p.piecetype is None:
                    str = str + "  "
                elif p.player == Player.WHITE:
                    str = str + self._prettyprintdict[p.piecetype] + " "
                else:
                    str = str + self._prettyprintdict[p.piecetype].lower() + " "
            print(str)


    def piecemoves(self) -> [Move]:
        """returns a list of moves formatted like:
        piece, piece position, piece destination, captured piece, promotion"""
        s = len(self.board)
        o = []
        for i in range(s):
            for j in range(s):
                pos=(i,j)
                p = self.board[i][j]
                match p.piecetype:
                    case None:
                        pass
                    case PieceType.PAWN:
                        if p.player==Player.WHITE:
                            c=1
                        else:
                            c=-1
                        o += self._checkmove(p, pos, (i, j-(1*c)), [None])
                        if i==s-2:
                            o += self._checkmove(p, pos, (i, j-(2*c)), [None])

                        o += self._checkmove(p, pos, (i-1, j-(1*c)), [Player(not p.player)])
                        o += self._checkmove(p, pos, (i+1, j-(1*c)), [Player(not p.player)])
                    case PieceType.RIGHT:
                        pass
                    case PieceType.KNIGHT:
                        pass
                    case PieceType.BISHOP:
                        pass
                    case PieceType.QUEEN:
                        pass
                    case PieceType.KING:
                        pass
        raise NotImplementedError




    def _checkmove(self, p, pos, dest, validLandingOccupants:list[Player|None]) -> list[Move]:
        if        ((dest[0] not in range(len(self.board)))
                or (dest[1] not in range(len(self.board)))
                or self.board[dest[0]][dest[1]].player not in validLandingOccupants):
            return []
        else:
            target: Piece = self.board[dest[0]][dest[1]]
            if p.piecetype == PieceType.PAWN and (pos[1] == 0 or pos[1] == len(self.board) - 1):
                return [Move(p, pos, dest, target.piecetype, PieceType.QUEEN)]
            else:
                return [Move(p, pos, dest, target.piecetype, None)]


b = Board(sample0)
b.prettyprint()