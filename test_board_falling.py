import board
from block import *

c = board.Board(5,5)

c.add(4,0,"A",0,board.LOCK_GRAVITY)
c.add(0,1,"A")
c.add(0,2,"B")
c.add(1,2,"D")
c.add(1,4,"C")
c.add(3,0,"A")
c.add(3,1,"B")

for i in range(7):
    print c
    c.update()
