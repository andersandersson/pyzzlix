class Board:
    def __init__(self, width=30, height=20):
        self.width = width
        self.height = height
        self.grid = []

        for x in range(width):
            self.grid.append([])
            for y in range(height):
                self.grid[x].append(None)
                
    def __str__(self):
        val = ""
        for x in range(self.width):
            val = "%s _______" % (val)
        val = "%s\n" % (val)
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[x][y]:
                    val = "%s|(%s,%d,%d)" % (val, self.grid[x][y]['tile'],self.grid[x][y]['hover_time'],self.grid[x][y]['moving'])
                else:
                    val = "%s|_______" % (val)
            val = val + "|\n"
        return val

    def add(self, x, y, tile):
        self.grid[x][y] = {'tile': tile, 'hover_time': 0, 'moving': False}

    def findCircle(self, x, y):
        pass

    def rotate(self, x, y, direction):
        if x > self.width-2 or x < 0:
            return False
        if y > self.height-2 or y < 0:
            return False

        upper_left = self.grid[x][y]
        upper_right = self.grid[x+1][y]
        lower_left = self.grid[x][y+1]
        lower_right = self.grid[x+1][y+1]

        if (upper_left and upper_left['moving']) or (upper_right and upper_right['moving']) or (lower_left and lower_left['moving']) or (lower_right and lower_right['moving']):
            return False

        self.grid[x][y] = lower_left
        self.grid[x+1][y] = upper_left
        self.grid[x][y+1] = lower_right
        self.grid[x+1][y+1] = upper_right

        return True

    def update(self, deltaTime):
        for y in reversed(range(self.height-1)):
            for x in range(self.width):
                tile_over = self.grid[x][y]
                tile_under = self.grid[x][y+1]
                
                if tile_under and y+1 == self.height-1:
                    tile_under['hover_time'] = 2
                    tile_under['moving'] = False

                if tile_over and not tile_under:
                    if tile_over['hover_time'] <= 0:
                        self.grid[x][y+1] = tile_over
                        self.grid[x][y] = None
                        tile_over['hover_time'] = 0
                        tile_over['moving'] = True
                    else:
                        tile_over['hover_time'] -= deltaTime
                elif tile_over and tile_under:
                    tile_over['hover_time'] = tile_under['hover_time']
                    tile_over['moving'] = tile_under['moving']

