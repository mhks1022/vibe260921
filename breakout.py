"""
tkinter로 만든 벽돌깨기(블럭깨기) 게임
- 방향키 좌/우 또는 마우스 이동으로 패들 조작
- 스페이스바로 시작/재시작
"""
import tkinter as tk
import random

WIDTH = 600
HEIGHT = 500

PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
PADDLE_Y = HEIGHT - 40
PADDLE_SPEED = 25

BALL_SIZE = 15
BALL_SPEED = 5

ROWS = 5
COLS = 8
BRICK_WIDTH = 65
BRICK_HEIGHT = 20
BRICK_TOP_MARGIN = 50
BRICK_GAP = 5

BRICK_COLORS = ["#e74c3c", "#e67e22", "#f1c40f", "#2ecc71", "#3498db"]


class BreakoutGame:
    def __init__(self, root):
        self.root = root
        self.root.title("벽돌깨기")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        self.lives = 3
        self.score = 0
        self.game_running = False
        self.game_over = False

        # 패들
        self.paddle = self.canvas.create_rectangle(
            WIDTH / 2 - PADDLE_WIDTH / 2, PADDLE_Y,
            WIDTH / 2 + PADDLE_WIDTH / 2, PADDLE_Y + PADDLE_HEIGHT,
            fill="white"
        )

        # 공
        self.ball = self.canvas.create_oval(
            WIDTH / 2 - BALL_SIZE / 2, PADDLE_Y - BALL_SIZE,
            WIDTH / 2 + BALL_SIZE / 2, PADDLE_Y,
            fill="yellow"
        )
        self.ball_dx = 0
        self.ball_dy = 0

        # 점수, 목숨 표시
        self.score_text = self.canvas.create_text(
            60, 15, text=f"점수: {self.score}", fill="white", font=("Arial", 12)
        )
        self.lives_text = self.canvas.create_text(
            WIDTH - 60, 15, text=f"목숨: {self.lives}", fill="white", font=("Arial", 12)
        )
        self.message_text = self.canvas.create_text(
            WIDTH / 2, HEIGHT / 2,
            text="스페이스바를 눌러 시작하세요",
            fill="white", font=("Arial", 16)
        )

        self.bricks = {}
        self.create_bricks()

        # 키 이벤트 바인딩
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<space>", self.start_game)
        self.canvas.bind("<Motion>", self.move_paddle_mouse)

        self.update()

    def create_bricks(self):
        for row in range(ROWS):
            for col in range(COLS):
                x1 = col * (BRICK_WIDTH + BRICK_GAP) + BRICK_GAP
                y1 = row * (BRICK_HEIGHT + BRICK_GAP) + BRICK_TOP_MARGIN
                x2 = x1 + BRICK_WIDTH
                y2 = y1 + BRICK_HEIGHT
                color = BRICK_COLORS[row % len(BRICK_COLORS)]
                brick = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                self.bricks[brick] = True

    def move_left(self, event=None):
        coords = self.canvas.coords(self.paddle)
        if coords[0] > 0:
            self.canvas.move(self.paddle, -PADDLE_SPEED, 0)

    def move_right(self, event=None):
        coords = self.canvas.coords(self.paddle)
        if coords[2] < WIDTH:
            self.canvas.move(self.paddle, PADDLE_SPEED, 0)

    def move_paddle_mouse(self, event):
        coords = self.canvas.coords(self.paddle)
        paddle_w = coords[2] - coords[0]
        new_x1 = event.x - paddle_w / 2
        new_x1 = max(0, min(WIDTH - paddle_w, new_x1))
        self.canvas.coords(self.paddle, new_x1, coords[1], new_x1 + paddle_w, coords[3])

    def start_game(self, event=None):
        if self.game_running:
            return

        if self.game_over:
            self.reset_game()

        self.game_running = True
        self.canvas.itemconfig(self.message_text, text="")
        self.ball_dx = random.choice([-1, 1]) * BALL_SPEED
        self.ball_dy = -BALL_SPEED

    def reset_game(self):
        for brick in list(self.bricks.keys()):
            self.canvas.delete(brick)
        self.bricks.clear()
        self.create_bricks()

        self.lives = 3
        self.score = 0
        self.game_over = False
        self.canvas.itemconfig(self.score_text, text=f"점수: {self.score}")
        self.canvas.itemconfig(self.lives_text, text=f"목숨: {self.lives}")

        self.canvas.coords(
            self.paddle,
            WIDTH / 2 - PADDLE_WIDTH / 2, PADDLE_Y,
            WIDTH / 2 + PADDLE_WIDTH / 2, PADDLE_Y + PADDLE_HEIGHT
        )
        self.reset_ball()

    def reset_ball(self):
        self.canvas.coords(
            self.ball,
            WIDTH / 2 - BALL_SIZE / 2, PADDLE_Y - BALL_SIZE,
            WIDTH / 2 + BALL_SIZE / 2, PADDLE_Y
        )
        self.ball_dx = 0
        self.ball_dy = 0
        self.game_running = False

    def update(self):
        if self.game_running:
            self.move_ball()
            self.check_collisions()

        self.root.after(16, self.update)

    def move_ball(self):
        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)

    def check_collisions(self):
        ball_coords = self.canvas.coords(self.ball)
        x1, y1, x2, y2 = ball_coords

        # 좌우 벽 충돌
        if x1 <= 0 or x2 >= WIDTH:
            self.ball_dx *= -1

        # 위쪽 벽 충돌
        if y1 <= 0:
            self.ball_dy *= -1

        # 바닥에 닿으면 목숨 감소
        if y2 >= HEIGHT:
            self.lose_life()
            return

        # 패들 충돌
        paddle_coords = self.canvas.coords(self.paddle)
        if self.rects_overlap(ball_coords, paddle_coords) and self.ball_dy > 0:
            # 패들에 맞은 위치에 따라 반사 각도 변경
            paddle_center = (paddle_coords[0] + paddle_coords[2]) / 2
            ball_center = (x1 + x2) / 2
            offset = (ball_center - paddle_center) / (PADDLE_WIDTH / 2)
            self.ball_dx = offset * BALL_SPEED
            self.ball_dy = -abs(self.ball_dy)

        # 벽돌 충돌 검사
        overlapping = self.canvas.find_overlapping(x1, y1, x2, y2)
        for item in overlapping:
            if item in self.bricks:
                brick_coords = self.canvas.coords(item)
                self.canvas.delete(item)
                del self.bricks[item]
                self.score += 10
                self.canvas.itemconfig(self.score_text, text=f"점수: {self.score}")

                # 공이 벽돌의 위/아래에서 왔는지, 좌/우에서 왔는지 판단
                ball_center_x = (x1 + x2) / 2
                ball_center_y = (y1 + y2) / 2
                brick_center_x = (brick_coords[0] + brick_coords[2]) / 2
                brick_center_y = (brick_coords[1] + brick_coords[3]) / 2

                dx = ball_center_x - brick_center_x
                dy = ball_center_y - brick_center_y

                if abs(dx) > abs(dy):
                    self.ball_dx *= -1
                else:
                    self.ball_dy *= -1
                break

        # 모든 벽돌을 깼는지 확인
        if not self.bricks:
            self.win_game()

    @staticmethod
    def rects_overlap(r1, r2):
        return r1[0] < r2[2] and r1[2] > r2[0] and r1[1] < r2[3] and r1[3] > r2[1]

    def lose_life(self):
        self.lives -= 1
        self.canvas.itemconfig(self.lives_text, text=f"목숨: {self.lives}")

        if self.lives <= 0:
            self.game_over = True
            self.canvas.itemconfig(
                self.message_text,
                text=f"게임 오버! 점수: {self.score}\n스페이스바를 눌러 재시작"
            )
            self.reset_ball()
        else:
            self.reset_ball()
            self.canvas.itemconfig(self.message_text, text="스페이스바를 눌러 계속하세요")

    def win_game(self):
        self.game_over = True
        self.canvas.itemconfig(
            self.message_text,
            text=f"승리! 점수: {self.score}\n스페이스바를 눌러 재시작"
        )
        self.reset_ball()


def main():
    root = tk.Tk()
    game = BreakoutGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
