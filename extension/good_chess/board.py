import time
from enum import Enum, IntEnum
import random
from random import shuffle

from chessmaker.chess.base import Square as cmSquare
from samples import *





class Piece:
    def __init__(self,piecetype,player):
        self.piecetype = piecetype
        self.player = player
    def __str__(self):
        if self.piecetype is None:
            return "NONE"
        else:
            return (self.player.name + " " + self.piecetype.name)

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

    def enemy(self):
        return Player(1 - self)

    def __str__(self):
        return {0:"WHITE",1:"BLACK"}[self]

class Move:
    def __init__(self, piece:Piece, position:(int,int), destination:(int, int), capture: PieceType | None, promotion: PieceType | None):
        self.piece = piece
        self.position = position
        self.destination = destination
        self.capture = capture
        self.promotion = promotion

    def __str__(self):
        s = str(self.piece.player.name + " " + self.piece.piecetype.name + " to " + str(self.destination))
        if self.capture is not None:
            s += ", capturing " + self.capture.name
        if self.promotion is not None:
            s += ", promoting to " + self.promotion.name
        return s


class Board:
    _chessmakerPieceConverter =  {"Pawn":PieceType.PAWN, "Knight":PieceType.KNIGHT, "Right":PieceType.RIGHT, "Bishop":PieceType.BISHOP, "Queen":PieceType.QUEEN, "King":PieceType.KING}
    _chessmakerColourConverter = {"white":Player.WHITE, "black":Player.BLACK}
    def __init__(self, inputboard:list[list[cmSquare]]=None):
        #raise NotImplemented
        if inputboard is None:
            self.board = [[Piece(None,None) for x in range(5)] for y in range(5)]
        else:
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
    def __str__(self):
        s = len(self.board)
        out = "v 0 1 2 3 4\n"
        for i in range(s):
            line = str(i) + " "
            for j in range(s):
                p = self.board[i][j]
                if p.piecetype is None:
                    line = line + ". "
                elif p.player == Player.WHITE:
                    line = line + self._prettyprintdict[p.piecetype] + " "
                else:
                    line = line + self._prettyprintdict[p.piecetype].lower() + " "
            out += line + "\n"
        return out

    def __getitem__(self,i):
        return self.board[i]

    def _piecemoves(self) -> [Move]:
        """returns a list of moves formatted like:
        piece, piece position, piece destination, captured piece, promotion"""
        s = len(self.board)
        o = []
        for i in range(s):
            for j in range(s):
                pos=(i,j)
                p = self.board[i][j]
                if p.player is not None:
                    enemy = Player(p.player.enemy())
                    capset = [None, enemy]
                match p.piecetype:
                    case None:
                        pass
                    case PieceType.PAWN:
                        if p.player==Player.WHITE:
                            c=1
                        else:
                            c=-1
                        o += self._checkmove(p, pos, (i-(1*c), j), [None])[0]

                        o += self._checkmove(p, pos, (i-(1*c), j-1), [enemy])[0]
                        o += self._checkmove(p, pos, (i-(1*c), j+1), [enemy])[0]
                    case PieceType.RIGHT:
                        #rook-like movement
                        n = 1
                        while True:
                            m,b = self._checkmove(p,pos,(i+n,j),capset)
                            o += m
                            if b:
                                n+=1
                            else:
                                break
                        n = 1
                        while True:
                            m,b = self._checkmove(p,pos,(i-n,j),capset)
                            o += m
                            if b:
                                n+=1
                            else:
                                break
                        n = 1
                        while True:
                            m, b = self._checkmove(p, pos, (i, j+n), capset)
                            o += m
                            if b:
                                n += 1
                            else:
                                break
                        n = 1
                        while True:
                            m, b = self._checkmove(p, pos, (i, j-n), capset)
                            o += m
                            if b:
                                n += 1
                            else:
                                break

                        #knightlike movement
                        o +=  self._checkmove(p,pos,(i+1,j+2),capset)[0]
                        o +=  self._checkmove(p,pos,(i+1,j-2),capset)[0]
                        o +=  self._checkmove(p,pos,(i-1,j+2),capset)[0]
                        o +=  self._checkmove(p,pos,(i-1,j-2),capset)[0]
                        o +=  self._checkmove(p,pos,(i+2,j+1),capset)[0]
                        o +=  self._checkmove(p,pos,(i+2,j-1),capset)[0]
                        o +=  self._checkmove(p,pos,(i-2,j+1),capset)[0]
                        o +=  self._checkmove(p,pos,(i-2,j-1),capset)[0]
                    case PieceType.KNIGHT:
                        o +=  self._checkmove(p,pos,(i+1,j+2),capset)[0]
                        o +=  self._checkmove(p,pos,(i+1,j-2),capset)[0]
                        o +=  self._checkmove(p,pos,(i-1,j+2),capset)[0]
                        o +=  self._checkmove(p,pos,(i-1,j-2),capset)[0]
                        o +=  self._checkmove(p,pos,(i+2,j+1),capset)[0]
                        o +=  self._checkmove(p,pos,(i+2,j-1),capset)[0]
                        o +=  self._checkmove(p,pos,(i-2,j+1),capset)[0]
                        o +=  self._checkmove(p,pos,(i-2,j-1),capset)[0]
                    case PieceType.BISHOP:
                        n = 1
                        while True:
                            m,b = self._checkmove(p,pos,(i+n,j+n),capset)
                            o += m
                            if b:
                                n+=1
                            else:
                                break
                        n = 1
                        while True:
                            m,b = self._checkmove(p,pos,(i+n,j-n),capset)
                            o += m
                            if b:
                                n+=1
                            else:
                                break
                        n = 1
                        while True:
                            m,b = self._checkmove(p,pos,(i-n,j+n),capset)
                            o += m
                            if b:
                                n+=1
                            else:
                                break
                        n = 1
                        while True:
                            m,b = self._checkmove(p,pos,(i-n,j-n),capset)
                            o += m
                            if b:
                                n+=1
                            else:
                                break
                    case PieceType.QUEEN:
                        #rook-like movement
                        n = 1
                        while True:
                            m,b = self._checkmove(p,pos,(i+n,j),capset)
                            o += m
                            if b:
                                n+=1
                            else:
                                break
                        n = 1
                        while True:
                            m,b = self._checkmove(p,pos,(i-n,j),capset)
                            o += m
                            if b:
                                n+=1
                            else:
                                break
                        n = 1
                        while True:
                            m, b = self._checkmove(p, pos, (i, j+n), capset)
                            o += m
                            if b:
                                n += 1
                            else:
                                break
                        n = 1
                        while True:
                            m, b = self._checkmove(p, pos, (i, j-n), capset)
                            o += m
                            if b:
                                n += 1
                            else:
                                break

                        #bishop-like movement
                        n = 1
                        while True:
                            m,b = self._checkmove(p,pos,(i+n,j+n),capset)
                            o += m
                            if b:
                                n+=1
                            else:
                                break
                        n = 1
                        while True:
                            m,b = self._checkmove(p,pos,(i+n,j-n),capset)
                            o += m
                            if b:
                                n+=1
                            else:
                                break
                        n = 1
                        while True:
                            m,b = self._checkmove(p,pos,(i-n,j+n),capset)
                            o += m
                            if b:
                                n+=1
                            else:
                                break
                        n = 1
                        while True:
                            m,b = self._checkmove(p,pos,(i-n,j-n),capset)
                            o += m
                            if b:
                                n+=1
                            else:
                                break
                    case PieceType.KING:
                        o +=  self._checkmove(p,pos,(i+1,j+1),capset)[0]
                        o +=  self._checkmove(p,pos,(i+1,j-1),capset)[0]
                        o +=  self._checkmove(p,pos,(i-1,j+1),capset)[0]
                        o +=  self._checkmove(p,pos,(i-1,j-1),capset)[0]
                        o +=  self._checkmove(p,pos,(i+1,j),capset)[0]
                        o +=  self._checkmove(p,pos,(i,j+1),capset)[0]
                        o +=  self._checkmove(p,pos,(i-1,j),capset)[0]
                        o +=  self._checkmove(p,pos,(i,j-1),capset)[0]

        return o

    def legalplayerpiecemoves(self,player:Player):
        ms = self._playerpiecemoves(player)
        #fms = list(filter((lambda m : self.copymove(m).check() is None),ms))
        fms = []
        for m in ms:
            b2 = self.copymove(m)
            c = b2.check()
            if player not in c:
                fms += [m]
        return fms

    def copymove(self, move:Move):
        y,x = move.position
        dy,dx = move.destination
        b2 = Board()
        b2.board = []
        for i in range(len(self.board)):
            b2.board += [self.board[i].copy()]

        b2.board[y][x] = Piece(None,None)
        b2.board[dy][dx] = move.piece
        if move.promotion:
            b2.board[dy][dx].piecetype = move.promotion
        return b2

    def _playerpiecemoves(self,player:Player):
        ms = self._piecemoves()
        pms = list(filter((lambda x : x.piece.player == player),ms))
        return pms



    def _checkmove(self, p, pos, dest, validLandingOccupants:list[Player|None]) -> tuple[list[Move],bool]:
        """checks if the given position is a valid landing space as defined in validLandingOccupants and returns the move and True if it is
        note this method does NOT check if a move is valid for a piece - this should be handled by external code"""
        if        ((dest[0] not in range(len(self.board)))
                or (dest[1] not in range(len(self.board)))
                or self.board[dest[0]][dest[1]].player not in validLandingOccupants):
            return [],False
        else:
            target: Piece = self.board[dest[0]][dest[1]]

            if p.piecetype == PieceType.PAWN and (dest[0] == 0 or dest[0] == len(self.board) - 1):
                return [Move(p, pos, dest, target.piecetype, PieceType.QUEEN)],False
            else:
                return [Move(p, pos, dest, target.piecetype, None)],(target.piecetype is None)

    def check(self) -> set[Player]:
        ms = self._piecemoves()
        fms = list(filter((lambda m : m.capture == PieceType.KING),ms))
        inchecks = set()
        # return fms[0].piece.player.enemy()
        for m in fms:
            inchecks.add(m.piece.player.enemy())
        return inchecks

b = Board(sample0)
print(b)
mover = Player.BLACK
print(b.check())

# fmls = b.legalplayerpiecemoves(Player.BLACK)
# shuffle(fmls)
# for m in fmls: print(m)
s = time.perf_counter()
print("seed:",s)
random.seed(s)
n=1
while True:
    lms = b.legalplayerpiecemoves(mover)
    shuffle(lms)
    print("turn",n)
    n+=1
    if lms:
        b = b.copymove(lms[0])
        print(mover.name +"'s move")
        print(b)
    else:
        print(mover.name + " cannot move")
        break
    mover = mover.enemy()

print(b.check())