import math
import random
import sys
import time
import multiprocessing as mp
from itertools import cycle, repeat
from operator import truediv
from random import shuffle

from chessmaker.chess.pieces import *
from chessmaker.chess.results import checkmate, stalemate

from samples import *
from chessmaker.chess.base import MoveOption, move_option, piece, Piece, Player, Position, player
from opponent import opponent
from extension.board_utils import list_legal_moves_for, take_notes, copy_piece_move, print_board_ascii
import chessmaker

def agent(board, player, var):
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
    global test
    test = False

    s = time.perf_counter()
    depth = 3
    customvar = [var[0],var[1],time.perf_counter()+var[1],depth]

    abm = funny_ab_minimax_map(board,player,player,customvar,-math.inf,math.inf,depth,1)
    take_notes("heuristic val: " + str(abm[0]))
    piece, move_opt = abm[1][0]
    take_notes("thought for:"+str(time.perf_counter()-s))
    return piece, move_opt


def board_piece_move_eval (info,move):
    board,piece,player,colour = info
    tempb = board.clone()
    tempb, tempp, tempm = copy_piece_move(tempb, piece, move)
    tempp.move(tempm)
    return colour*evalheuristic(tempb,player),(piece,move)
def funny_ab_minimax_map(board, player, turn, var,a,b,depth,colour,pool) -> (int,[piece,move_option]):
    legal = list_legal_moves_for_map(board, turn,pool)
    shuffle(legal)
    global leaves
    global culls
    global test
    if turn.name == "white":
        nextturn = black
    else:
        nextturn = white

    #print_board_ascii(board)

    if (legal!=[]) & (depth > 0):
        chosenMove = None, None
        pms = []


        for lpm in legal:
            p=lpm[0]
            if lpm[1]:
                val = -math.inf
                shuffle(lpm[1])
                if depth>1:
                    for m in lpm[1]:
                        tempb = board.clone()
                        tempb, tempp, tempm = copy_piece_move(tempb, p,m)
                        tempp.move(tempm)
                        ra, rpms = funny_ab_minimax_map(tempb,player,nextturn,var,-b,-a,depth-1, colour*-1,pool)
                        val,chosenMove,pms = max((-ra,(p,m),rpms),(val,chosenMove,pms),key=lambda x : x[0])
                        a = max(a,val)
                        if a>=b or (time.perf_counter() >= var[2]-0.5 and not test):
                            return a,([(p,m)]+pms)
                else:
                    vs = pool.starmap(board_piece_move_eval,zip(repeat((board,p,player,-1*colour)),lpm[1]))
                    mv = max(vs+[(val,chosenMove)],key=lambda x : x[0])
                    val,chosenMove = mv
                    a = max(a, val)
                    if a >= b or (time.perf_counter() >= var[2] - 0.5 and not test):
                        return a, ([chosenMove] + pms)


        return a,([(chosenMove[0], chosenMove[1])]+pms)
    else:
        eh = colour * evalheuristic(board, player, var)
        return eh, []


def captures_for(board,player):
    ls = list_legal_moves_for(board,player)
    fs = filter(lambda m : m[1].captures!=set(),ls)
    return fs

def list_legal_moves_for_map(board, player, pool):
    # (!) this is still slow. improve
    pieces = board.get_player_pieces(player)
    return list(pool.map(pair_piece_with_moves,pieces))
def pair_piece_with_moves(piece):
    return (piece,piece.get_move_options())


def evalheuristic(board,player):
    #consider each player's pieces, their worth, and the pieces each player has in danger. perhaps depth of pawns, promotion??
    #consider forks? amount of possible moves?

    global htime
    global amtime
    s = time.perf_counter()
    global leaves
    global lmtime
    global test
    #leaves += 1
    piecepoints = {"Pawn":1, "Right":6, "Knight":3, "Bishop":3, "Queen":9, "King":9}
    #right and king approximated in points
    #right does not exist in normal chess
    #king has no point value in normal chess
    #do mess with these if it's bad

    if player.name=="white":
        opponent = board.players[1]
    else:
        opponent = board.players[0]
    score = 0

    ps = board.get_player_pieces(player)
    for p in ps:
        score += piecepoints[p.name]
        for m in p.get_move_options():
            for c in m.captures:
                score += piecepoints[board[c].piece.name]
    ops = board.get_player_pieces(opponent)
    for p in ops:
        score -= piecepoints[p.name]
        for m in p.get_move_options():
            for c in m.captures:
                score -= piecepoints[board[c].piece.name]


    #pawn depth scoring




    #endgame status scoring
    if checkmate(board) == f"Checkmate - {player.name} loses":
        score -= 1000
    if checkmate(board) == f"Checkmate - {opponent.name} loses":
        score += 1000
    if stalemate(board):
        score -= 500
    #htime += time.perf_counter() - s
    return score

if __name__ == '__main__':
    global leaves
    leaves = 0
    global culls
    culls = 0
    global htime
    htime = 0
    global amtime
    amtime = 0
    global lmtime
    lmtime = 0
    global test
    test = True
    pool = mp.Pool()
    players = [white,black]
    board = chessmaker.chess.base.Board(hellsample,players, cycle(players))
    print_board_ascii(board)
    legals = list_legal_moves_for_map(board, white,pool)
    print(legals)
    print("num of initial moves:",sum(len(m[1]) for m in legals))
    starttime = time.perf_counter()
    #board,piece,move = copy_piece_move(board,pms[0][0],pms[0][1])
    #piece.move(move)
    #print_board_ascii(board)
    d = 3
    starttime = time.perf_counter()
    h, pms = funny_ab_minimax_map(board, white, white, [d, 14, time.perf_counter()+14,d], -math.inf, math.inf, d, 1,pool)
    pool.close()
    print("----- map ver done -----")
    print("depth:", d)
    ttime = time.perf_counter() - starttime
    print(h, pms)
    print("leaves:", leaves)
    print("culls:", culls)
    print("thinking time:", ttime)
    print("total time in heuristics:",htime)
    print("   attack/material scoring:", amtime)
    print("                           ", str(100*amtime/htime) + "%")
    print("      legal move finding:  ", lmtime)
    print("                           ", str(100*lmtime/htime) + "%")
    print("                     avg:  ", str(1000*lmtime/leaves)+"ms")
    print("total time NOT in heuristics:",ttime-htime)
    print("average heuristic time:", str(1000*htime/leaves)+"ms")