import board

c = board.Board(5,5)

c.add(1, 1, "*")
c.add(1, 2, "*", 0)
c.add(1, 3, "*")
c.add(1, 4, "*")
c.update()
print c

for i in range(5):
    c.rotate(1,1,1,3)
    print c
