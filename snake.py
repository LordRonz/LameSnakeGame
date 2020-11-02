import random
import curses

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self, initBody, initDir):
        self.body = initBody
        self.direction = initDir
        self.isDead = False

    def take_step(self, pos, ate=False):
        if not ate:
            if pos in self.body[1:]:
                self.isDead = True
            else:
                self.body = self.body[1:] + [pos]
        else:
            if pos in self.body[1:]:
                self.isDead = True
            else:
                self.body = self.body + [pos]

    def set_direction(self, dir):
        self.direction = dir

    def head(self):
        return self.body[-1]


class Apple:
    def __init__(self, initPos):
        self.pos = initPos

    def set_pos(self, pos):
        self.pos = pos


class Game:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.snake = Snake([(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)], RIGHT)
        self.isDead = self.snake.isDead
        applePos = (
            random.randint(0, self.width - 1),
            random.randint(0, self.height - 1),
        )
        while applePos in self.snake.body:
            applePos = (
                random.randint(0, self.width - 1),
                random.randint(0, self.height - 1),
            )
        self.apple = Apple(applePos)
        self.score = 0

    def board_matrix(self):
        matrix = []
        temp = "+" + "-" * self.width + "+"
        matrix.append(list(temp))
        pos = self.snake.body
        for i in range(self.height):
            temp = "|"
            for j in range(self.width):
                body = False
                for a in pos:
                    if a[0] == j and a[1] == i:
                        temp += "X" if a == self.snake.head() else "O"
                        body = True
                if self.apple.pos[0] == j and self.apple.pos[1] == i and not body:
                    temp += "*"
                elif not body:
                    temp += " "
            temp += "|"
            matrix.append(list(temp))

        temp = "+" + "-" * self.width + "+"
        matrix.append(list(temp))
        return matrix

    def update(self, direction):
        head = self.snake.head()
        ate = False
        if direction == "W":
            if self.snake.direction != DOWN:
                step = (
                    head[0] + UP[0],
                    head[1] + UP[1] if head[1] + UP[1] >= 0 else self.height - 1,
                )
                if step == self.apple.pos:
                    ate = True
                self.snake.take_step(step, ate)
                self.snake.set_direction(UP)
            else: direction = ""
        elif direction == "S":
            if self.snake.direction != UP:
                step = (
                    head[0] + DOWN[0],
                    head[1] + DOWN[1] if head[1] + DOWN[1] < self.height else 0,
                )
                if step == self.apple.pos:
                    ate = True
                self.snake.take_step(step, ate)
                self.snake.set_direction(DOWN)
            else: direction = ""
        elif direction == "A":
            if self.snake.direction != RIGHT:
                step = (
                    head[0] + LEFT[0] if head[0] + LEFT[0] >= 0 else self.width - 1,
                    head[1] + LEFT[1],
                )
                if step == self.apple.pos:
                    ate = True
                self.snake.take_step(step, ate)
                self.snake.set_direction(LEFT)
            else: direction = ""
        elif direction == "D":
            if self.snake.direction != LEFT:
                step = (
                    head[0] + RIGHT[0] if head[0] + RIGHT[0] < self.width else 0,
                    head[1] + RIGHT[1],
                )
                if step == self.apple.pos:
                    ate = True
                self.snake.take_step(step, ate)
                self.snake.set_direction(RIGHT)
            else: direction = ""
        if direction == "":
            if self.snake.direction == UP:
                self.update("W")
            elif self.snake.direction == DOWN:
                self.update("S")
            elif self.snake.direction == LEFT:
                self.update("A")
            elif self.snake.direction == RIGHT:
                self.update("D")

        if ate:
            self.score += 1
            applePos = (
                random.randint(0, self.width - 1),
                random.randint(0, self.height - 1),
            )
            while applePos in self.snake.body:
                applePos = (
                    random.randint(0, self.width - 1),
                    random.randint(0, self.height - 1),
                )
            self.apple.set_pos(applePos)
        self.isDead = self.snake.isDead

    def render(self):
        matrix = self.board_matrix()
        return "\n".join(["".join(c) for c in matrix])


def play(stdscr: "curses._CursesWindow", highscore: int):
    score = 0
    game = Game(10, 20)
    while not game.isDead:
        stdscr.timeout(max(100, 1000 - score * 20))
        stdscr.refresh()
        stdscr.addstr(0, 0, f"Score : {score}\n")
        stdscr.addstr(game.render())
        try:
            direction = stdscr.getkey().upper()
        except curses.error:
            direction = ""
        while direction not in ("W", "S", "A", "D", "", "Q"):
            try:
                direction = stdscr.getkey().upper()
            except curses.error:
                direction = ""
        if direction == "Q":
            curses.endwin()
            return menu(highscore)
        game.update(direction)
        score = game.score
    curses.endwin()
    highscore = max(score, highscore)
    print(f"Your Score : {score}")
    print(f"Highscore : {highscore}")
    print("Oh wow, you're fucking dead motherfucker!")
    return menu(highscore)


def menu(highscore = 0):
    howTo = """
    Move your snake with WASD key.
    Eat the motherfucking apples to grow your snake(or dick)
    Each time you eat an apple, your score will be increased by 1.
    Good luck nibba!
    """
    print("Welcome, motherfucker !")
    print("This is Snake-The Game")
    # print("Wanna play motherfucker ? (y/n)")
    print("1. Play\n2. How to play\n3. Exit")
    ans = input().strip()
    while ans not in ["1", "2", "3"]:
        ans = input().strip()
    if ans == "1":
        print("Let's go motherfucker !")
        curses.wrapper(play, highscore)
    elif ans == "2":
        print(howTo)
        print('Press enter to continue')
        input()
        menu()


def main():
    menu()
    print("Fuck you!")


if __name__ == "__main__":
    main()
