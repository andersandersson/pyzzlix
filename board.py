from block import *

LOCK_NONE = 0
LOCK_ROTATION = 1
LOCK_GRAVITY = 2

DEFAULT_GRAVITY_DELAY = 2

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
                    val = "%s|(%s,%d,%d)" % (val, self.grid[x][y]['block'],self.grid[x][y]['gravity_delay'],self.grid[x][y]['lock'])
                else:
                    val = "%s|_______" % (val)
            val = val + "|\n"
        return val

    def add(self, x, y, block, gravity_delay=DEFAULT_GRAVITY_DELAY, lock=LOCK_NONE):
        self.grid[x][y] = {'block': block, 'gravity_delay': gravity_delay, 'lock': lock}

    def findCircle(self, x, y):
        pass

    def rotate(self, x, y, direction, radius):
        # Just check that we are in a valid area
        if x > self.width-radius or x < 0:
            return False
        if y > self.height-radius or y < 0:
            return False

        # Generate a list with the x values for traversing a circular rectangle
        #
        # 0 -> 1 -> 2
        # |         |
        # 0         2  =>  0, 1, 2, 2, 2, 1, 0, 0, 0
        # |         |
        # 0 <- 1 <- 2
        #
        xs = range(radius)
        xs += [radius-1]*(radius-1)
        xs += range(radius-2, -1, -1)
        xs += [0]*(radius-1)

        # Clone xs to ys
        ys = xs[:]

        # Depending on direction, reverse either xs or ys
        if 1 == direction:
            ys.reverse()
        else:
            xs.reverse()

        # Combine the two lists into on list of tuples
        # [1 2], [1 2] => [(1,1), (2,2)]
        ps = zip(xs, ys)

        tile = None
        next_tile = None

        # Go through the generated list of points and check if anyone
        # is locked, in which case we will return false
        for p in ps:
            next_tile = self.grid[p[0]+x][p[1]+y]
            if next_tile and next_tile["lock"] & LOCK_ROTATION:
                return False

        tile = None

        # Go through the generated list of points and switch them
        # along the circle
        for p in ps:
            xx = p[0]+x
            yy = p[1]+y

            next_tile = self.grid[xx][yy]
            self.grid[xx][yy] = tile
            tile.moveTo(xx, yy)
            tile = next_tile

        return True

    def update(self):
        for y in reversed(range(self.height-1)):
            for x in range(self.width):
                tile_over = self.grid[x][y]

                if tile_over and not (tile_over['lock'] & LOCK_GRAVITY):
                    tile_under = self.grid[x][y+1]
                    
                    if tile_under and y+1 == self.height-1:
                        tile_under['gravity_delay'] = DEFAULT_GRAVITY_DELAY
                        tile_under['lock'] = tile_under['lock'] & (~LOCK_ROTATION)

                    if tile_over and not tile_under:
                        if tile_over['gravity_delay'] <= 0:
                            self.grid[x][y+1] = tile_over
                            self.grid[x][y] = None                            
                            tile_over['gravity_delay'] = 0
                            tile_over['lock'] |= LOCK_ROTATION
                        else:
                            tile_over['gravity_delay'] -= 1

                    elif tile_over and tile_under:
                        tile_over['gravity_delay'] = tile_under['gravity_delay']
                        tile_over['lock'] = tile_over['lock'] & (~LOCK_ROTATION)
                        tile_over['lock'] |= (tile_under['lock'] & LOCK_ROTATION)

