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

    def add2stack(self, x, y):
        self.stack.append(self.maze[x][y])
        self.visited.append(self.maze[x][y])

    def next2stack_GIF(self, image):
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
                        self.maze[self.stack[-1].x][self.stack[-1].y].dig_wall(fromwall)
                        self.maze[self.stack[-1].x][self.stack[-1].y].make_sprite((153, 255, 153), image)
                        # and cell we're going to
                        self.maze[newx][newy].dig_wall(towall)
                        self.maze[newx][newy].make_sprite((153, 255, 153), image)
                        #we had the new cell in the stack
                        self.add2stack(newx, newy)
                        exit, dead_end = True, True
                    else:
                        deadend += 1
                if deadend >= 4:
                    # dead_end > 4 therefore dead end we remove the cell from the stack
                    if self.stack:
                        self.maze[self.stack[-1].x][self.stack[-1].y].make_sprite((255,255,255), image)
                    self.stack.pop()
                    if self.stack:
                        self.maze[self.stack[-1].x][self.stack[-1].y].make_sprite((255,255,255), image)
                    exit, dead_end = True, True

        return image

    def make_maze_GIF(self):
        frames = []
        frames.append(Image.new('RGB', (self.width * 5, self.height * 5),
                                'black'))

        self.add2stack(randint(0, self.width - 1),randint(0, self.height - 1))
        while self.stack:
            new_image = frames[-1].copy()
            new_image = self.next2stack_GIF(new_image)
            frames.append(new_image)

        frames[0].save('laby_contruct_backtrack.gif', format='GIF',
                       save_all=True, append_images=frames[1:], optimize=False,
                       duration=100, loop=0)
        frames[-1].save('laby_bis.jpg', format='JPEG')


class Cell():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.N = True
        self.S = True
        self.W = True
        self.E = True

    def show_cell(self):
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

    def dig_wall(self, wall):
        # wall = N, S, E or W
        if wall == 'N': self.N = False
        if wall == 'S': self.S = False
        if wall == 'E': self.E = False
        if wall == 'W': self.W = False

    def make_sprite(self, color, image):
        sx = self.x
        sy = self.y
        wall_color = (0, 0, 0)
        pixels = image.load()

        # first line (with north wall)
        if not self.N:
            pixels[sx * 5, sy *5] = wall_color
            for i in range(1,4): pixels[sx * 5 + i, sy * 5] = color
            pixels[sx * 5 + 4, sy *5] = wall_color
        else:
            for i in range(5): pixels[sx * 5 + i, sy * 5] = wall_color

        # lines 2,3,4 (with west and east walls)
        for j in range(1,4):
            if not self.W:
                pixels[sx * 5, sy * 5 + j] = color
            else:
                pixels[sx * 5, sy * 5 + j] = wall_color

            if not self.E:
                pixels[sx * 5 + 4, sy * 5 + j] = color
            else:
                pixels[sx * 5 + 4, sy * 5 + j] = wall_color

            for i in range(1,4):
                pixels[sx * 5 + i, sy * 5 + j] = color

        # fifth line (with south wall)
        if not self.S:
            pixels[sx * 5, sy *5 + 4] = wall_color
            for i in range(1,4): pixels[sx * 5 + i, sy * 5 + 4] = color
            pixels[sx * 5 + 4, sy *5 + 4] = wall_color
        else:
            for i in range(5): pixels[sx * 5 + i, sy * 5 + 4] = wall_color


if __name__ == '__main__':
    laby = Maze(20, 20)
    laby.make_maze_GIF()

    # list all cells with walls
    for i in range(laby.width):
        for j in range(laby.height):
            laby.maze[i][j].show_cell()
