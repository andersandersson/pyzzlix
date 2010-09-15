import board
from block import *

c = board.Board(10,10)

for x in range(10):
    for y in range(10):
        c.add(x, y, ".", "bb")

c.add(1, 1, "a", "aa");
c.add(2, 1, "a", "aa");
c.add(2, 3, "a", "aa");
c.add(3, 3, "a", "aa");
c.add(3, 1, "a", "aa");
c.add(4, 1, "a", "aa");
c.add(4, 0, "a", "aa");
c.add(5, 1, "a", "aa");
c.add(5, 2, "a", "aa");
c.add(5, 3, "a", "aa");
c.add(4, 3, "a", "aa");
c.add(4, 4, "a", "aa");
c.add(4, 5, "a", "aa");
c.add(4, 6, "a", "aa");
c.add(3, 6, "a", "aa");
c.add(2, 6, "a", "aa");
c.add(1, 6, "a", "aa");
c.add(1, 5, "a", "aa");
c.add(1, 4, "a", "aa");
c.add(1, 3, "a", "aa");
c.add(1, 2, "a", "aa");
print c
c.findCircle( [(1,1)] )
print c
