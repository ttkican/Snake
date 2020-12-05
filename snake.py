import pygame, sys, random

screen_size = width, height = 600, 600


class Snake(object):
    def __init__(self):
        self.direction = pygame.K_RIGHT
        self.body = []
        for x in range(5):
            self.eatnode()

    def eatnode(self):
        left, top = (0, 0)
        if self.body:
            left, top = (self.body[0].left, self.body[0].top)
        node = pygame.Rect(left, top, 25, 25)
        if self.direction == pygame.K_LEFT:
            node.left -= 25
        elif self.direction == pygame.K_RIGHT:
            node.left += 25
        elif self.direction == pygame.K_UP:
            node.top -= 25
        elif self.direction == pygame.K_DOWN:
            node.top += 25
        self.body.insert(0, node)

    def delnode(self):
        self.body.pop()

    def isdead(self):
        if self.body[0].x not in range(width):
            return True
        if self.body[0].y not in range(height):
            return True
        if self.body[0] in self.body[1:]:
            return True
        return False

    def move(self):
        self.eatnode()
        self.delnode()

    def changedirection(self, curkey):
        LR = [pygame.K_LEFT, pygame.K_RIGHT]
        UD = [pygame.K_UP, pygame.K_DOWN]
        # 防止蛇的运动方向逆向改变
        if curkey in LR + UD:
            if (curkey in LR) and (self.direction in LR):
                return
            if (curkey in UD) and (self.direction in UD):
                return
            self.direction = curkey


class Food(object):
    def __init__(self):
        self.rect = pygame.Rect(-25, 0, 25, 25)

    def remove(self):
        self.rect.x = -25

    def set(self):
        if self.rect.x == -25:
            allpos = []
            for pos in range(25, width - 25, 25):
                allpos.append(pos)
            self.rect.left = random.choice(allpos)
            self.rect.top = random.choice(allpos)
            print(self.rect)


def show_text(screen, pos, text, color, font_bold=False, font_size=60, font_italic=False):
    # 获取系统文字，设置字体大小
    cur_font = pygame.font.SysFont("宋体", font_size)
    # 是否加粗
    cur_font.set_bold(font_bold)
    # 是否斜体
    cur_font.set_italic(font_italic)
    # 文字内容
    text_fmt = cur_font.render(text, 1, color)
    # 绘制文字
    screen.blit(text_fmt, pos)


def main():
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("snake")
    clock = pygame.time.Clock()
    score = 0
    isdead = False
    snake = Snake()
    food = Food()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                snake.changedirection(event.key)
                if event.key == pygame.K_SPACE and isdead:
                    return main()
        screen.fill((255, 255, 255))
        if not isdead:
            snake.move()
        for rect in snake.body:
            pygame.draw.rect(screen, (20, 220, 39), rect, 0)
        isdead = snake.isdead()

        if isdead:
            show_text(screen, (100, 200), "YOU DEAD!", (227, 29, 18), False, 100)
            show_text(screen, (150, 260), "press space to try again...", (0, 0, 22), False, 30)
        # 食物的处理，食物与蛇头是否重叠
        if food.rect == snake.body[0]:
            score += 50
            food.remove()
            snake.eatnode()
        food.set()
        pygame.draw.rect(screen, (136, 0, 24), food.rect, 0)
        # 显示分数
        show_text(screen, (50, 500), "Score:" + str(score), (223, 223, 223))
        pygame.display.update()
        clock.tick(8)


if __name__ == '__main__':
    main()
