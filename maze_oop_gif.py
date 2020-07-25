# a maze builder in oop
# using the recursive backtracking with next cell is newest cell
# refs:
# http://weblog.jamisbuck.org/2011/1/27/maze-generation-growing-tree-algorithm
# http://rosettacode.org/wiki/Maze_generation#Python
# https://github.com/ravenkls/Maze-Generator-and-Solver
# and wikipedia: https://en.wikipedia.org/wiki/Maze_generation_algorithm

from random import randint, shuffle
from PIL import Image

class Maze():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.stack = []
        self.visited = []
        self.maze = [[Cell(i,j) for j in range(self.height)] for i in
                     range(self.width)]

    def add2Stack(self, x, y):
        self.stack.append(self.maze[x][y])
        self.visited.append(self.maze[x][y])

    def next2Stack(self):
        exit = False
        while not exit:
            dead_end = False
            deadend = 0
            list_n = [1, 2, 3, 4]
            shuffle(list_n)
            while not dead_end:
                n = list_n.pop()
                if n == 1: dx = 0; dy = -1; fromwall = 'N'; towall = 'S'
                if n == 2: dx = 1; dy = 0; fromwall = 'E'; towall = 'W'
                if n == 3: dx = 0; dy = 1; fromwall = 'S'; towall = 'N'
                if n == 4: dx = -1; dy = 0; fromwall = 'W'; towall = 'E'
                newx = self.stack[-1].x + dx
                newy = self.stack[-1].y + dy
                # we check if we are not out of the maze
                if newx < 0 or newx > self.width - 1 or newy < 0 or newy > (self.height - 1):
                    deadend += 1
                else:
                    # we check if the next cell is already in the stack
                    if self.maze[newx][newy] not in self.visited:
                        # we update the walls, cell we're coming from
                        self.maze[self.stack[-1].x][self.stack[-1].y].digWall(fromwall)
                        # and cell we're going to
                        self.maze[newx][newy].digWall(towall)
                        #we had the new cell in the stack
                        self.add2Stack(newx, newy)
                        exit, dead_end = True, True
                    else:
                        deadend += 1
                if deadend >= 4:
                    # dead_end > 4 therefore dead end we remove the cell from the stack
                    self.stack.pop()
                    exit, dead_end = True, True

    def makeMaze(self):
        self.add2Stack(randint(0, self.width - 1),randint(0, self.height - 1))
        while self.stack:
            self.next2Stack()

    def showMazeASCII(self):
        print('+--' * self.width, '+', sep='')
        for j in range(self.height):
            for i in range(self.width):
                if self.maze[i][j].W: print('|  ', sep='', end='')
                else: print('   ', sep='', end='')
            print('|')
            for i in range(self.width):
                if not self.maze[i][j].S: print('+  ', sep='', end='')
                else: print('+--', sep='', end='')
            print('+')

    def MazeGIF(self):
        frames = []
        laby_image = Image.new('RGB', (self.width * 5, self.height * 5),
                               'black')
        frames.append(laby_image)

        for i in range(len(self.visited)):
            new_image = frames[-1].copy()
            pixels = new_image.load()

            sx = self.visited[i].x
            sy = self.visited[i].y
            wall_color = (0, 0, 0)
            visited_color = (255, 255, 255)

            # first line of the sprite (check if North wall is open)
            if not self.visited[i].N:
                pixels[sx * 5, sy * 5] = wall_color
                for k in range(1,4):
                    pixels[sx * 5 + k, sy * 5] = visited_color
                pixels[sx * 5 + 4, sy * 5] = wall_color
            else:
                for k in range(5):
                    pixels[sx * 5 + k, sy * 5] = wall_color

            # lines 2, 3 and 4 of the sprite (check if East and West walls are
            # open)
            for j in range(1,4):
                if not self.visited[i].W:
                    pixels[sx * 5, sy * 5 + j] = visited_color
                else:
                    pixels[sx * 5, sy * 5 + j] = wall_color

                for k in range(1,4):
                    pixels[sx * 5 + k, sy * 5 + j] = visited_color

                if not self.visited[i].E:
                    pixels[sx * 5 + 4, sy * 5 + j] = visited_color
                else:
                    pixels[sx * 5 + 4, sy * 5 + j] = wall_color


            # last (5th) line (check if South wall is open)
            if not self.visited[i].S:
                pixels[sx * 5, sy * 5 + 4] = wall_color
                for k in range(1,4):
                    pixels[sx * 5 + k, sy * 5 + 4] = visited_color
                pixels[sx * 5 + 4, sy * 5 + 4] = wall_color
            else:
                for k in range(5):
                    pixels[sx * 5 + k, sy * 5 + 4] = wall_color

            frames.append(new_image)

        frames[0].save('laby_construct.gif', format='GIF', save_all=True,
                            append_images=frames[1:], optimize=False,
                            duration=100, loop=0)
        frames[-1].save('laby.jpg', format='JPEG')


class Cell():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.N = True
        self.S = True
        self.W = True
        self.E = True

    def showCell(self):
        if self.N: walln = 'N'
        else: walln = '.'
        if self.S: walls = 'S'
        else: walls = '.'
        if self.E: walle = 'E'
        else: walle = '.'
        if self.W: wallw = 'W'
        else: wallw = '.'
        print('Cell ({: >2d},{: >2d}) - walls: {}{}{}{}'.format(self.x, self.y,
                                                      walln, walls, walle,
                                                      wallw))

    def digWall(self, wall):
        # wall = N, S, E or W
        if wall == 'N': self.N = False
        if wall == 'S': self.S = False
        if wall == 'E': self.E = False
        if wall == 'W': self.W = False


if __name__ == '__main__':
    laby = Maze(26, 11)
    laby.makeMaze()

    # list all cells with walls
    for i in range(laby.width):
        for j in range(laby.height):
            laby.maze[i][j].showCell()

    print('len(visited):', len(laby.visited))
    # list visited cells
    for i in range(len(laby.visited)):
        laby.visited[i].showCell()

    # print in ascii
    laby.showMazeASCII()

    # show image
    laby.MazeGIF()
