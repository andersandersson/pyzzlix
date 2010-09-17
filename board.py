from block import *

STATUS_NONE = 0
STATUS_MOVING = 1
STATUS_WEIGHTLESS = 2
STATUS_IN_CIRCLE = 4

DEFAULT_GRAVITY_DELAY = 2

EVENT_CIRCLE_FOUND = USEREVENT
EVENT_GAME_OVER = USEREVENT+1

def TriangleArea(a, b, c):
    return (b[0]-a[0]) * (c[1]-a[1]) - (c[0]-a[0])*(b[1]-a[1])

def PolygonArea(points):
    start = points[0]
    prev = points[1]
    area = 0

    for p in points[2:]:
        area += TriangleArea(start, prev, p)
        prev = p

    return area

class Board:
    def __init__(self, width=30, height=20):
        self.width = width
        self.height = height

        self.reset()

    def __str__(self):
        val = ""
        for x in range(self.width):
            val = "%s _" % (val)
        val = "%s\n" % (val)
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[x][y]:
                    val = "%s|%d" % (val, self.grid[x][y]['status'])
                else:
                    val = "%s|_" % (val)
            val = val + "|\n"
        return val

    def reset(self):
        self.last_rotated = []
        self.grid = []
        self.gameOver = False

        for x in range(self.width):
            self.grid.append([])
            for y in range(self.height):
                self.grid[x].append(None)        

    def add(self, x, y, type, block, gravity_delay=DEFAULT_GRAVITY_DELAY, status=STATUS_NONE):
        self.grid[x][y] = {'type': type, 'block': block, 'gravity_delay': gravity_delay, 'status': status}

    def clear(self, x, y):
        self.grid[x][y] = None

    def updateGameOver(self):
        for rows in self.grid:
            for tile in rows:
                if not tile:
                    return

        self.gameOver = True        
        pygame.event.post(pygame.event.Event(EVENT_GAME_OVER))

    def handleCircle(self, points):
        # If the points are oriented counterclockwise, change it.
        if PolygonArea(points) < 0:
            points.reverse()

        blocks = []

        last_point = None
        for point in points:
            x = point[0]
            y = point[1]

            self.grid[x][y]['status'] |= STATUS_IN_CIRCLE

            if self.grid[x][y]['block'] not in blocks:
                blocks.append(self.grid[x][y]['block'])

            if last_point:
                x_dir = 0
                y_dir = 0

                if point[1] - last_point[1] == 1:
                    x_dir = -1

                if point[1] - last_point[1] == -1:
                    x_dir = 1

                if point[0] - last_point[0] == 1:
                    y_dir = 1

                if point[0] - last_point[0] == -1:
                    y_dir = -1
                
                while (x+x_dir, y+y_dir) not in points:
                    x = x+x_dir
                    y = y+y_dir
                    self.grid[x][y]['status'] |= STATUS_IN_CIRCLE
                    if self.grid[x][y]['block'] not in blocks:
                        blocks.append(self.grid[x][y]['block'])

            last_point = point

        pygame.event.post(pygame.event.Event(EVENT_CIRCLE_FOUND, blocks=blocks))

    def findCircle(self, points):        
        if self.gameOver:
            return

        def finder(x, y, path, first_point, type):
            if x < 0 or y < 0 or x >= self.width or y >= self.height:
                return None

            if not self.grid[x][y]:
                return None

            if not self.grid[x][y]['type'] == type:
                return None

            if self.grid[x][y]['status'] & STATUS_MOVING or self.grid[x][y]['status'] & STATUS_IN_CIRCLE:
                return None

            if path and x == first_point[0] and y == first_point[1]:
                return path

            if (x, y) in path:
                return None

            paths = []
            paths += [finder(x, y+1, path + [(x,y)], first_point, type)]
            paths += [finder(x+1, y, path + [(x,y)], first_point, type)]
            paths += [finder(x-1, y, path + [(x,y)], first_point, type)]
            paths += [finder(x, y-1, path + [(x,y)], first_point, type)]

            new_path = []
            for pa in paths:
                if pa and len(pa) > len(new_path):
                    new_path = pa
            
            return new_path
            
        for p in points:
            if self.grid[p[0]][p[1]]:
                circle = finder(p[0], p[1], [], p, self.grid[p[0]][p[1]]['type'])
                if circle and len(circle) >= 4:
                    self.handleCircle(circle)

    def rotate(self, x, y, direction, radius):
        if self.gameOver:
            return False

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
        points = zip(xs, ys)

        tile = None
        next_tile = None

        # Go through the generated list of points and check if anyone
        # is locked, in which case we will return false
        for p in points:
            next_tile = self.grid[p[0]+x][p[1]+y]
            if next_tile and (next_tile['status'] & STATUS_MOVING or next_tile['status'] & STATUS_IN_CIRCLE):
                return False

        tile = None
        self.last_rotated = []

        # Go through the generated list of points and switch them
        # along the circle
        for p in points:
            xx = p[0]+x
            yy = p[1]+y

            self.last_rotated += [(xx, yy)]

            next_tile = self.grid[xx][yy]
            self.grid[xx][yy] = tile

            try:
                if tile:
                    tile["block"].moveTo(xx, yy)
                    tile['status'] |= STATUS_MOVING
            except (AttributeError, TypeError):
                pass

            tile = next_tile

        return True

    def update(self):
        if self.gameOver:
            return

        points = self.last_rotated

        for y in reversed(range(self.height-1)):
            for x in range(self.width):
                tile_over = self.grid[x][y]
                tile_under = self.grid[x][y+1]
                    
                if tile_under and y+1 == self.height-1:
                    if 0 == tile_under['gravity_delay']:
                        points.append( (x, y+1) )

                    tile_under['gravity_delay'] = DEFAULT_GRAVITY_DELAY
                    tile_under['status'] &= ~STATUS_MOVING
                    
                if tile_over and not tile_under:
                    if tile_over and not tile_over['status'] & STATUS_WEIGHTLESS and not tile_over['status'] & STATUS_IN_CIRCLE:
                        if tile_over['gravity_delay'] <= 0:
                            self.grid[x][y+1] = tile_over
                            self.grid[x][y] = None
                            tile_over['gravity_delay'] = 0
                            tile_over['status'] |= STATUS_MOVING

                            try:
                                tile_over['block'].moveTo(x, y+1)
                            except (AttributeError, TypeError):
                                pass
                            
                        else:
                            tile_over['gravity_delay'] -= 1

                elif tile_over and tile_under:
                    if 0 == tile_over['gravity_delay'] and not 0 == tile_under['gravity_delay']:
                        points.append( (x, y) )
                    
                    tile_over['gravity_delay'] = tile_under['gravity_delay']

                    if tile_under['status'] & STATUS_MOVING:
                        tile_over['status'] |= STATUS_MOVING
                    else:
                        tile_over['status'] &= ~STATUS_MOVING

        if points:
            self.findCircle(points)

        self.last_rotated = []
        self.updateGameOver()