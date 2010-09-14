import board

c = board.Board(5,5)

c.add(1, 1, "*")
c.add(1, 2, "*")
c.add(1, 3, "*")
c.add(1, 4, "*")
c.update(1)
print c
c.rotate(1,1,0)

for i in range(5):
    print c
    c.update(1)
