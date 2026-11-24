import math
import random
import sys
import time
import multiprocessing as mp
from itertools import cycle, repeat
from random import shuffle
from chessmaker.chess.pieces import *
from chessmaker.chess.results import checkmate, stalemate

from samples import white,black

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

    pool = mp.Pool()
    #test
    s = time.perf_counter()
    depth = 3
    panicmargin = 0.5
    test = False
    customvar = [var[0],var[1],time.perf_counter()+var[1],depth,panicmargin,test]
    abm = funny_ab_minimax_map(board,player,player,customvar,-math.inf,math.inf,depth,1,pool)
    pool.close()
    pool.join()
    take_notes("heuristic val: " + str(abm[0]))
    piece, move_opt = abm[1][0]
    take_notes("thought for:"+str(time.perf_counter()-s))
    return piece, move_opt


def board_piece_move_eval (info,move):
    board,piece,player,colour,var,testing = info
    if time.perf_counter() >= var[2] - var[4] and not testing:
        return colour * math.inf * -1, (piece,move) #idk if it needs to be *-1 i'm scared help
    tempb = board.clone()
    tempb, tempp, tempm = copy_piece_move(tempb, piece, move)
    tempp.move(tempm)
    return colour*evalheuristic(tempb,player),(piece,move)
def funny_ab_minimax_map(board, player, turn, var,a,b,depth,colour,pool) -> (int,[piece,move_option]):
    test = var[5]
    legal = list_legal_moves_for_map(board, turn,pool)
    shuffle(legal)
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
                        if a>=b or (time.perf_counter() >= var[2] - var[4] and not test):
                            if test:
                                culls += 1
                            return a,([(p,m)]+pms)
                else:
                    vs = pool.starmap(board_piece_move_eval,zip(repeat((board,p,player,-1*colour,var,test)),lpm[1]))
                    mv = max(vs+[(val,chosenMove)],key=lambda x : x[0])
                    val,chosenMove = mv
                    a = max(a, val)
                    if a >= b or (time.perf_counter() >= var[2] - var[4] and not test):
                        if test:
                            culls += 1
                        return a, ([chosenMove] + pms)


        return a,([(chosenMove[0], chosenMove[1])]+pms)
    else:
        eh = colour * evalheuristic(board, player)
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
    piecepoints = {"Pawn":1, "Right":10, "Knight":3, "Bishop":3, "Queen":9, "King":15}
    #right and king approximated in points
    #right does not exist in normal chess
    #king has no point value in normal chess
    #do mess with these if it's bad
    pawnpospoints = {0:9,1:6,2:3,3:0}

    weights = [8,1,2]
    #weights for material, capture options, pawn depth

    if player.name=="white":
        opponent = board.players[1]
    else:
        opponent = board.players[0]
    score = 0

    ps = board.get_player_pieces(player)
    for p in ps:
        score += piecepoints[p.name] * weights[0]
        if p.name == "Pawn":
            score += pawnpospoints[p.position.y] * weights[2]
        for m in p.get_move_options():
            for c in m.captures:
                score += piecepoints[board[c].piece.name] * weights[1]
    ops = board.get_player_pieces(opponent)
    for p in ops:
        score -= piecepoints[p.name] * weights[0]
        if p.name == "Pawn":
            score -= pawnpospoints[board.size[1]-p.position.y-1] * weights[2]
        for m in p.get_move_options():
            for c in m.captures:
                score -= piecepoints[board[c].piece.name] * weights[1]






    #endgame status scoring
    if checkmate(board) == f"Checkmate - {player.name} loses":
        score -= 1000
    if checkmate(board) == f"Checkmate - {opponent.name} loses":
        score += 1000
    if stalemate(board):
        score -= 500
    return score

if __name__ == '__main__':
    from samples import *
    global leaves
    leaves = 0
    global culls
    culls = 0

    #test without time limits?

    test = False
    pool = mp.Pool()
    players = [white,black]
    board = chessmaker.chess.base.Board(d4failsample,players, cycle(players))
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
    h, pms = funny_ab_minimax_map(board, white, white, [d, 14, time.perf_counter()+14,d,0.5,test], -math.inf, math.inf, d, 1,pool)
    pool.close()
    print("----- done -----")
    print("depth:", d)
    ttime = time.perf_counter() - starttime
    print(h, pms)
    print("culls:", culls)
    print("thinking time:", ttime)
    #print("average heuristic time:", str(1000*htime/leaves)+"ms")


#all on hellsample
#NO PAWN DEPTH
#depth 3
#value 12
#18.13, 7.62, 19.43, 10.58, 11.42, 13.92, 7.37, 8.36, 18.76, 11.47

#WITH PAWN DEPTH
#depth 3
#value 17
#7.46, 10.94, 20.33, 9.42, 11.93, 18.34, 17.32, 14.04,
