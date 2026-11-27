from agent import *
import agent
from samples import *

if __name__ == "__main__":
    b = agent.Board(fuck)
    for m in b.legalplayerpiecemoves(agent.Player.WHITE):
        print(m)

