import time
import pygame
import sys
from point import Point
import random
from button import Button


class Again:
    def __init__(self):
        pygame.init()
        # 窗口大小
        self.W = 800
        self.H = 600
        # 背景颜色
        self.bg_color = 'pink'
        self.point = Point
        # 渲染一个窗口
        self.screen = pygame.display.set_mode((self.W, self.H))
        # 设置标题
        pygame.display.set_caption("贪吃蛇")
        # 设置行数及列数
        self.ROW = 30
        self.COL = 40
        # 设置食物初始位置
        self.food = self.point(self.ROW // 2, self.COL // 2)
        # 设置初始方向
        self.move_flag = 'right'
        # 初始速度
        self.move_again_speed = 3
        # 倍率
        self.speed = 1.1
        # 设置一个时间
        self.time1 = time.time()
        self.clock = pygame.time.Clock()
        self.eat = False

        # 设置头部坐标
        self.head = self.point(row=0, col=3)
        # 创建一个变量 判断头部位置是否发生了变化
        self.head_copy = self.point(0, 0)
        # 设置蛇身体坐标
        self.body_all = [self.point(row=0, col=2), self.point(row=0, col=1), self.point(row=0, col=0)]
        # 游戏状态
        self.game_active = False
        self.play_button = Button(self, 'play')

    def run(self):
        # 游戏主循环
        while True:
            self.clock.tick(60)#固定一秒6帧率
            self.check_event()
            if self.game_active:
                self.handle_events()
            self.update_screen()

    def create_food(self):
        while True:
            food = self.point(row=random.randint(0, self.ROW - 1), col=random.randint(0, self.COL - 1))
            # 判断食物是否出现在了蛇首处
            if self.check_touch(self.head, food):
                continue
            # 判断食物是否出现在了蛇身处
            for point in self.body_all:
                if self.check_touch(point, food):
                    break
            else:
                return food
            continue

    def check_play_button(self, mouse_pos):
        # 按下按钮之后 开始游戏
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.game_active = True

    def draw_rect(self, point, color, type_='body'):
        cell_w = self.W // self.COL
        cell_h = self.H // self.ROW
        top = cell_h * point.row
        left = cell_w * point.col
        if type_ == 'body':
            pygame.draw.rect(self.screen, color=color, rect=(left, top, cell_w, cell_h))
        elif type_ == 'head':
            x = left + cell_w / 2
            y = top + cell_h / 2
            pygame.draw.circle(self.screen, color=color, center=(x, y), radius=cell_h / 2)

    def handle_events(self):
        # 移动蛇
        # 设置速度
        time_1 = 1 / self.move_again_speed
        time_2 = time.time() - self.time1
        if time_2 >= time_1:
            self.move_snake()

            self.time1 = time.time()

        # 吃东西检测
        if self.check_touch(self.head, self.food):
            self.eat = True
            self.move_again_speed *= self.speed
            # 生成新的食物
            # 如果是长度占所有格子的2/3 则换为另一种创造食物的方式
            if not (len(self.body_all) * 1.5 >= self.COL * self.ROW):
                self.food = self.create_food()
            else:
                self.food = self.create_food_plus()
            print(self.food.col, self.food.row)

        # 头碰到结界检测
        self.check_edge()
        # 头碰到自身检测
        self.check_touch_body()

    def update_screen(self):

        # 更新屏幕背景色
        pygame.draw.rect(self.screen, self.bg_color, self.screen.get_rect())

        # 绘制蛇身
        for body in self.body_all:
            self.draw_rect(body, (255, 0, 0))

        # 绘制蛇头
        self.draw_rect(self.head, (0, 0, 255), type_='head')

        # 绘制食物
        self.draw_rect(self.food, (0, 255, 0), type_='head')

        # 如果游戏处于非活动状态，就绘制play按钮。
        if not self.game_active:
            self.play_button.draw_button()

        # 更新屏幕
        pygame.display.flip()

    def check_touch(self, p1: Point, p2: Point):
        if p1.col == p2.col and p1.row == p2.row:
            return True
        else:
            return False

    def check_touch_body(self):
        for body in self.body_all:
            if self.check_touch(body, self.head):
                self.check_die()

    def move_head(self):

        if self.move_flag == 'right':
            self.head.col += 1
        elif self.move_flag == 'left':
            self.head.col -= 1
        elif self.move_flag == 'up':
            self.head.row -= 1
        elif self.move_flag == 'down':
            self.head.row += 1

    def create_food_plus(self):
        all_point = []
        for row in range(self.ROW):
            for col in range(self.COL):
                point = Point(row, col)
                if not (self.check_touch(point, self.head)):
                    for body in self.body_all:
                        if not (self.check_touch(point, body)):
                            continue
                        else:
                            break
                    else:
                        all_point.append(Point(row=row, col=col))
        # 判断是否还有空余
        if len(all_point) > 0:
            food = random.choice(all_point)
            return food
        else:
            print('没有了')
            pygame.quit()
            sys.exit()

    def check_event(self):
        for event in pygame.event.get():
            # 判断是否点击了退出
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:

                self.check_event_keydown(event)
            elif event.type == pygame.KEYUP:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_play_button(mouse_pos)

    def move_body(self):
        snake_body = self.head.copy()
        self.body_all.insert(0, snake_body)
        if self.eat:
            self.eat = False
            return
        self.body_all.pop()

    def move_snake(self):

        # 移动蛇身
        self.move_body()
        # 移动蛇头
        self.move_head()

    def check_event_keydown(self, event):

        # 设置一个按键锁 防止连续两次转弯之后转到了相对方向
        if self.head.row == self.head_copy.row and self.head.col == self.head_copy.col:
            return
        self.head_copy = self.head.copy()
        if event.key == pygame.K_RIGHT:
            if self.move_flag != 'left':
                self.move_flag = 'right'
        elif event.key == pygame.K_LEFT:
            if self.move_flag != 'right':
                self.move_flag = 'left'
        elif event.key == pygame.K_UP:
            if self.move_flag != 'down':
                self.move_flag = 'up'
        elif event.key == pygame.K_DOWN:
            if self.move_flag != 'up':
                self.move_flag = 'down'

    def check_die(self):
        '''重置游戏'''
        # 设置头部坐标
        self.head = self.point(row=0, col=3)
        # 创建一个变量 判断头部位置是否发生了变化
        self.head_copy = self.point(0, 0)
        # 设置蛇身体坐标
        self.body_all = [self.point(row=0, col=2), self.point(row=0, col=1), self.point(row=0, col=0)]
        # 游戏状态
        self.game_active = False
        self.play_button = Button(self, 'play')
        # 设置食物初始位置
        self.food = self.point(self.ROW // 2, self.COL // 2)
        # 设置初始方向
        self.move_flag = 'right'
        # 初始速度
        self.move_again_speed = 3

    def check_edge(self):
        head = self.head
        if head.col < 0 or head.row < 0 or head.row >= self.ROW or head.col >= self.COL:
            self.check_die()


if __name__ == '__main__':
    ai_game = Again()
    ai_game.run()
