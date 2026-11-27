import math
import random
import time
from enum import Enum, IntEnum
import multiprocessing as mp
from random import shuffle
import copy
from typing import NamedTuple

from chessmaker.chess.base import MoveOption as cmMoveOption, Piece as cmPiece, Square as cmSquare, Board as cmBoard, Position as cmPosition
from extension.board_utils import list_legal_moves_for, take_notes, copy_piece_move
import chessmaker
def agent(board:cmBoard, player, var):
    """"
    This is an example of your designed Agent

    Parameters
    ----------
    board: the current chess board
    player: your assigned player role (white or black)
    var:  [ply, THINKING_TIME_BUDGET] a list cotaining the ply ID and the thinking_time_budget (secs)

    Returns
    -------
    piece: your selected chess piece
    move_opt: your selected move of your selected chess piece
    
    Hints:
    -----
    - List of players on the current board game: list(board.players) - default list: [Player (white), Player (black)]
    - board.players[0].name = "white" and board.players[1].name = "black"
    - Name of the player assigned to the Agent (either "white" or "black"): player.name
    - list of pieces of the current player: list(board.get_player_pieces(player))
    - List of pieces and corresponding moves for each pieces of the player: piece, move_opt = list_legal_moves_for(board, player)
    - From var: ply ID = var[0], timeout = var[1]
    - Use the timeout variable together with time.perf_counter()
    to ensure the agent returns its best move before the time limit expires.
    """
    piece, move_opt = None, None
    print(f"Ply: {var[0]}")
    take_notes("\n----- ply " + str(var[0]) + " -----")

    #test
    s = time.perf_counter()

    panicmargin = 0.2
    test = False
    customboard = Board()
    piecetypeconvert = {"Pawn":PieceType.PAWN,"Right":PieceType.RIGHT,"Knight":PieceType.KNIGHT,"Bishop":PieceType.BISHOP,"Queen":PieceType.QUEEN,"King":PieceType.KING}
    playerconvert = {"white":Player.WHITE,"black":Player.BLACK}
    for y in range(5):
        for x in range(5):
            p:cmPiece = board[cmPosition(x,y)].piece
            if p is not None:
                pt, pl = p.name, p.player.name
                customboard.board[y][x] = Piece(piecetypeconvert[pt],playerconvert[pl])
    #print(customboard)
    customplayer = playerconvert[player.name]
    tt={}
    depth = 2
    abm = (-math.inf, Move(None,None,None,None,None))
    customvar = [var[0],var[1],time.perf_counter()+var[1],depth,panicmargin,test]

    pettinessthreshold = 0
    while time.perf_counter() <= customvar[2] - customvar[4] and abm[0] < pettinessthreshold:
        depth+=1
        customvar[3] = depth
        tbm = funny_ab_minimax_map(customboard,customplayer,customplayer,customvar,-math.inf,math.inf,depth,1,{})
        abm = max(tbm,abm,key=lambda x : x[0])


    take_notes("heuristic val: " + str(abm[0]))
    take_notes("transposition table entries:"+str(len(tt)))
    take_notes("max depth reached:"+str(depth))

    #convert Move to MoveOption
    m:Move = abm[1]
    piece = board[cmPosition(m.position[1], m.position[0])].piece
    move_opt = cmMoveOption(cmPosition(m.destination[1],m.destination[0]),set([cmPosition(m.destination[1],m.destination[0])]))

    take_notes("thought for:"+str(time.perf_counter()-s))



    return piece, move_opt

# EXPORTED BOARD CLASS STARTS HERE!!!
class Piece:
    def __init__(self,piecetype,player):
        self.piecetype = piecetype
        self.player = player
    def __str__(self):
        if self.piecetype is None:
            return "NONE"
        else:
            return (self.player.name + " " + self.piecetype.name)
    def indexOf(self):
        return self.piecetype.value + (self.player.value * 6)

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

    _zobristTable = [[[random.randint(0,2**64) for i in range(12)] for i in range(5)] for j in range(5)]

    def __hash__(self) -> int:
        h = 0
        for y in range(5):
            for x in range(5):
                p = self[y][x]
                if p.piecetype is not None:
                    h ^= Board._zobristTable[y][x][p.indexOf()]
        return h

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

    def _pospiecemoves(self,pos:tuple[int,int]):
        i,j = pos
        o=[]
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

    def _piecemoves(self) -> [Move]:
        """returns a list of moves formatted like:
        piece, piece position, piece destination, captured piece, promotion"""
        s = len(self.board)
        o = []
        for i in range(s):
            for j in range(s):
                o+=self._pospiecemoves((i,j))

        return o

    def legalplayerpiecemoves(self,player:Player):
        ms = self._playerpiecemoves(player)
        fms = list(filter((lambda m : player not in self.copymove(m).check()),ms))
        return fms

    def legalpiecemoves(self):
        ms = self._piecemoves()
        fms = list(filter((lambda m : m.piece.player not in self.copymove(m).check()),ms))
        return fms

    def legalpospiecemoves(self, pos:tuple[int,int]):
        ms = self._pospiecemoves(pos)
        fms = list(filter((lambda m : m.piece.player not in self.copymove(m).check()),ms))
        return fms

    def copymove(self, move:Move):
        y,x = move.position
        dy,dx = move.destination
        b2 = Board()
        b2.board = copy.deepcopy(self.board)

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
        """returns a set of all players currently in check"""
        ms = self._piecemoves()
        fms = list(filter((lambda m : m.capture == PieceType.KING),ms))
        inchecks = set()
        # return fms[0].piece.player.enemy()
        for m in fms:
            inchecks.add(m.piece.player.enemy())
        return inchecks

    def checkmate(self):
        """returns a set of all players that would be in checkmate if it was their turn"""
        inchecks = self.check()
        incheckmates = set()
        for p in inchecks:
            if self.legalplayerpiecemoves(p) == []:
                incheckmates.add(p)
        return incheckmates

    def stalemate(self):
        """returns a set of all players that would be in stalemate if it was their turn (including checkmates)"""
        instalemates = set()
        for p in Player:
            if self.legalplayerpiecemoves(p) == []:
                instalemates.add(p)
        return instalemates

# EXPORTED BOARD CLASS ENDS HERE!!!


# def board_piece_move_eval (info,move):
#     board,piece,player,colour,var,testing = info
#     if time.perf_counter() >= var[2] - var[4] and not testing:
#         return colour * math.inf * -1, (piece,move) #idk if it needs to be *-1 i'm scared help
#     tempb = board.clone()
#     tempb, tempp, tempm = copy_piece_move(tempb, piece, move)
#     tempp.move(tempm)
#     return colour*evalheuristic(tempb,player),(piece,move)

class TTableFlag(Enum):
    EXACT = 0
    LOWERBOUND = 1
    UPPERBOUND = 2

class TTableEntry(NamedTuple):
    value: int
    pm: Move
    depth: int
    flag: TTableFlag


def funny_ab_minimax_map(board:Board, player:Player, turn:Player, var,a,b,depth,colour,ttable) -> tuple[int,Move]:
    test = var[5]
    aInit = a
    if hash(board) in ttable:
        e = ttable[hash(board)]
        if e.depth >= depth:
            #print("ping")
            if e.flag == TTableFlag.EXACT:
                return (e.value, e.pm)
            elif e.flag == TTableFlag.LOWERBOUND and e.value >= b:
                return (e.value, e.pm)
            elif e.flag == TTableFlag.UPPERBOUND and e.value <= a:
                return (e.value, e.pm)


    legal:list[Move] = board.legalplayerpiecemoves(turn)
    #global htime
    next_turn = turn.enemy()
    if not((legal!=[]) & (depth > 0)):
        t = time.perf_counter()
        eh = colour * evalheuristic(board, player, next_turn)
        #htime += time.perf_counter() - t
        return eh, []

    shuffle(legal)
    legal.sort(key=lambda mov : {None:0,PieceType.PAWN:1, PieceType.RIGHT:10, PieceType.KNIGHT:3, PieceType.BISHOP:3, PieceType.QUEEN:9, PieceType.KING:15}[mov.capture])


    chosen_move = None
    val = -math.inf
    for m in legal:
        board2 = board.copymove(m)
        ra, rpm = funny_ab_minimax_map(board2,player,next_turn,var,-b,-a,depth-1, colour*-1, ttable)
        val,chosen_move = max((-ra,m),(val,chosen_move),key=lambda x : x[0])
        a = max(a,val)
        if a>=b or (time.perf_counter() >= var[2] - var[4] and not test):
            break


    if val <= aInit:
        f = TTableFlag.UPPERBOUND
    elif val >= b:
        f = TTableFlag.LOWERBOUND
    else:
        f = TTableFlag.EXACT

    ttable[hash(board)] = TTableEntry(val,chosen_move,depth,f)
    return val, chosen_move


# def captures_for(board,player):
#     ls = list_legal_moves_for(board,player)
#     fs = filter(lambda m : m[1].captures!=set(),ls)
#     return fs
# def list_legal_moves_for_map(board, player, pool):
#     # (!) this is still slow. improve
#     pieces = board.get_player_pieces(player)
#     return list(pool.map(pair_piece_with_moves,pieces))
# def pair_piece_with_moves(piece):
#     return (piece,piece.get_move_options())


def evalheuristic(board:Board,player:Player, turn:Player):
    #consider each player's pieces, their worth, and the pieces each player has in danger. perhaps depth of pawns, promotion??
    #consider forks? amount of possible moves?
    piecepoints = {PieceType.PAWN:1, PieceType.RIGHT:10, PieceType.KNIGHT:3, PieceType.BISHOP:3, PieceType.QUEEN:9, PieceType.KING:15, None:0}
    #right and king approximated in points
    #right does not exist in normal chess
    #king has no point value in normal chess
    #do mess with these if it's bad
    pawnpospoints = {(0,Player.WHITE):9,(1,Player.WHITE):6,(2,Player.WHITE):3,(3,Player.WHITE):0,(4,Player.WHITE):0,
                     (4,Player.BLACK):9,(3,Player.BLACK):6,(2,Player.BLACK):3,(1,Player.BLACK):0,(0,Player.BLACK):0,
                     (0,None): 0,(1,None): 0,(2,None): 0,(3,None): 0,(4,None): 0,}



    weights = [10,1,2]
    #weights for material, capture options, pawn depth

    opponent = player.enemy()
    scorerdict = {player:1,opponent:-1,None:0}
    score = 0

    #endgame status scoring
    cms = board.checkmate()
    if player in cms:
        return -1000
    if opponent in cms:
        return 1000
    sms = board.stalemate()
    if player in sms and player == turn:
        return -500
    if opponent in sms and opponent == turn:
        return -500

    #scorer lambda
    board_pos_score = lambda board,y,x : (
            scorerdict[board[y][x].player]*( #factors in player
                (piecepoints[board[y][x].piecetype]*weights[0]) #material
                + ((board[y][x].piecetype==PieceType.PAWN)*pawnpospoints[(y, board[y][x].player)]) #pawn depth
                + sum((piecepoints[m.capture] + (pawnpospoints[(m.destination[0], board[m.destination[0]][m.destination[1]].player)] if m.capture==PieceType.PAWN else 0)) for m in board.legalpospiecemoves((y,x))) * weights[1] #captures
            )
    )

    #material & pawn depth scoring
    for y in range(len(board.board)):
        for x in range(len(board.board)):
            score += board_pos_score(board,y,x)
    #score = (
    # sum(map(lambda y :
    #     sum(map(lambda x :
    #         board_pos_score(board,y,x)
    #         , range(len(board.board))))
    #     , range(len(board.board)))))

        # for x in range(len(board.board)):
        #     p = board[y][x]
        #     if p.player == player:
        #         score += piecepoints[p.piecetype] * weights[0]
        #         if p.piecetype == PieceType.PAWN:
        #             score += pawnpospoints[y] * weights[2]
        #     elif p.player == opponent:
        #         score -= piecepoints[p.piecetype] * weights[0]
        #         if p.piecetype == PieceType.PAWN:
        #             score -= pawnpospoints[len(board.board)-y-1] * weights[2]
        #     else:
        #         pass
    #capture scoring
    # (!) is it worth keeping something this lightly weighted that takes this long? removing it takes the eval's time from ~80% to ~60%
    #
    # for cm in filter(lambda m : m.capture is not None,board.legalpiecemoves()):
    #     score += piecepoints[cm.capture] * weights[1] * scorerdict[cm.piece.player]




    return score

# if __name__ == '__main__':
#     from samples import sample0
#     s=time.perf_counter()
#     print("seed:",s)
#     random.seed(s)
#
#     #test without time limits?
#     test = True
#
#     board = Board(sample0)
#     print(board)
#     legals = board.legalplayerpiecemoves(Player.WHITE)
#     #for l in legals: print(l)
#     print("hash",hash(board))
#     print("hash",hash(board))
#     print("num of initial moves:",len(legals))
#     starttime = time.perf_counter()
#     d = 4
#     print("depth:",d)
#     starttime = time.perf_counter()
#
#     #global htime
#     #htime = 0
#     tt = {}
#     h, pm = funny_ab_minimax_map(board, Player.WHITE, Player.WHITE, [d, 14, time.perf_counter()+14,d,0.5,test], -math.inf, math.inf, d, 1, tt)
#
#     print("----- done -----")
#     print("depth:", d)
#     print("tt size:", len(tt))
#     ttime = time.perf_counter() - starttime
#     print(h, ",", pm)
#     print("thinking time:", round(ttime,2))
#     print("time in heuristic:", round(htime,2))
#     print("                  ", round(100*htime/ttime,2),"%")
#     print("time elsewhere:   ", round(ttime-htime,2))
#     print("                  ", round(100*(ttime-htime)/ttime,2),"%")

