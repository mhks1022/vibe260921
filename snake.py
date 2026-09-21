"""
tkinter로 만든 뱀게임(Snake Game) - 사람 vs AI 대결 모드
- 방향키로 초록색 뱀(플레이어) 조작
- 파란색 뱀은 AI가 자동으로 조작 (사과를 향해 이동하며 충돌 회피)
- 같은 사과를 먼저 먹는 쪽이 점수 획득, 뱀 길이도 증가
- 벽/자기 몸/상대 뱀에 부딪히면 그 뱀은 게임 오버 (즉시 라운드 종료)
- 게임이 끝나면 점수가 더 높은 쪽이 승리
- 스페이스바로 시작/재시작
"""
import tkinter as tk
import random

WIDTH = 600
HEIGHT = 500
CELL_SIZE = 20

GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

MOVE_DELAY = 100  # ms

BG_COLOR = "black"

PLAYER_COLOR = "#2ecc71"
PLAYER_HEAD_COLOR = "#27ae60"

AI_COLOR = "#3498db"
AI_HEAD_COLOR = "#2980b9"

APPLE_COLOR = "#e74c3c"
TEXT_COLOR = "white"

DIRECTIONS = {
    "Up": (0, -1),
    "Down": (0, 1),
    "Left": (-1, 0),
    "Right": (1, 0),
}
OPPOSITE = {
    "Up": "Down",
    "Down": "Up",
    "Left": "Right",
    "Right": "Left",
}


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("뱀게임 - 사람 vs AI")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG_COLOR)
        self.canvas.pack()

        self.running = False
        self.after_id = None

        self.root.bind("<KeyPress>", self.on_key)

        self.reset()
        self.draw_start_screen()

    def reset(self):
        mid_y = GRID_HEIGHT // 2

        self.player_snake = [(3, mid_y), (4, mid_y), (5, mid_y)]
        self.player_direction = "Right"
        self.player_next_direction = "Right"
        self.player_score = 0
        self.player_dead = False

        ai_head_x = GRID_WIDTH - 6
        self.ai_snake = [(ai_head_x + 2, mid_y), (ai_head_x + 1, mid_y), (ai_head_x, mid_y)]
        self.ai_direction = "Left"
        self.ai_score = 0
        self.ai_dead = False

        self.spawn_apple()

    def spawn_apple(self):
        occupied = set(self.player_snake) | set(self.ai_snake)
        while True:
            pos = (random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))
            if pos not in occupied:
                self.apple = pos
                return

    def on_key(self, event):
        key = event.keysym
        if key == "space":
            if not self.running:
                self.reset()
                self.running = True
                self.game_loop()
            return

        if key in DIRECTIONS and self.running:
            if OPPOSITE[key] != self.player_direction:
                self.player_next_direction = key

    def compute_ai_direction(self):
        head = self.ai_snake[-1]
        candidates = [d for d in DIRECTIONS if d != OPPOSITE[self.ai_direction]]

        safe = []
        for d in candidates:
            dx, dy = DIRECTIONS[d]
            nx, ny = head[0] + dx, head[1] + dy
            if nx < 0 or nx >= GRID_WIDTH or ny < 0 or ny >= GRID_HEIGHT:
                continue
            if (nx, ny) in self.ai_snake[1:]:
                continue
            if (nx, ny) in self.player_snake[1:]:
                continue
            safe.append(d)

        if not safe:
            return self.ai_direction

        ax, ay = self.apple

        def distance(d):
            dx, dy = DIRECTIONS[d]
            nx, ny = head[0] + dx, head[1] + dy
            return abs(nx - ax) + abs(ny - ay)

        safe.sort(key=distance)
        return safe[0]

    def is_dead(self, head, own_body, own_growing, other_body, other_growing):
        x, y = head
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
            return True

        own_check = own_body if own_growing else own_body[1:]
        if head in own_check:
            return True

        other_check = other_body if other_growing else other_body[1:]
        if head in other_check:
            return True

        return False

    def game_loop(self):
        self.player_direction = self.player_next_direction
        self.ai_direction = self.compute_ai_direction()

        pdx, pdy = DIRECTIONS[self.player_direction]
        adx, ady = DIRECTIONS[self.ai_direction]

        p_head = self.player_snake[-1]
        a_head = self.ai_snake[-1]
        new_p_head = (p_head[0] + pdx, p_head[1] + pdy)
        new_a_head = (a_head[0] + adx, a_head[1] + ady)

        player_grow = new_p_head == self.apple
        ai_grow = new_a_head == self.apple
        head_on_crash = new_p_head == new_a_head

        player_dead = head_on_crash or self.is_dead(
            new_p_head, self.player_snake, player_grow, self.ai_snake, ai_grow
        )
        ai_dead = head_on_crash or self.is_dead(
            new_a_head, self.ai_snake, ai_grow, self.player_snake, player_grow
        )

        self.player_dead = player_dead
        self.ai_dead = ai_dead

        apple_eaten = False

        if not player_dead:
            self.player_snake.append(new_p_head)
            if player_grow:
                self.player_score += 1
                apple_eaten = True
            else:
                self.player_snake.pop(0)

        if not ai_dead:
            self.ai_snake.append(new_a_head)
            if ai_grow:
                self.ai_score += 1
                apple_eaten = True
            else:
                self.ai_snake.pop(0)

        if apple_eaten:
            self.spawn_apple()

        self.draw()

        if player_dead or ai_dead:
            self.running = False
            self.draw_game_over()
            return

        self.after_id = self.root.after(MOVE_DELAY, self.game_loop)

    def draw(self):
        self.canvas.delete("all")

        for i, (x, y) in enumerate(self.player_snake):
            color = PLAYER_HEAD_COLOR if i == len(self.player_snake) - 1 else PLAYER_COLOR
            self.draw_cell(x, y, color)

        for i, (x, y) in enumerate(self.ai_snake):
            color = AI_HEAD_COLOR if i == len(self.ai_snake) - 1 else AI_COLOR
            self.draw_cell(x, y, color)

        ax, ay = self.apple
        self.draw_cell(ax, ay, APPLE_COLOR)

        self.canvas.create_text(
            10, 10, anchor="nw", fill=PLAYER_COLOR,
            font=("Arial", 14, "bold"), text=f"플레이어: {self.player_score}",
        )
        self.canvas.create_text(
            WIDTH - 10, 10, anchor="ne", fill=AI_COLOR,
            font=("Arial", 14, "bold"), text=f"AI: {self.ai_score}",
        )

    def draw_cell(self, x, y, color):
        x0 = x * CELL_SIZE
        y0 = y * CELL_SIZE
        self.canvas.create_rectangle(
            x0, y0, x0 + CELL_SIZE, y0 + CELL_SIZE,
            fill=color, outline=BG_COLOR,
        )

    def draw_start_screen(self):
        self.canvas.delete("all")
        self.canvas.create_text(
            WIDTH / 2, HEIGHT / 2 - 50, fill=TEXT_COLOR,
            font=("Arial", 24, "bold"), text="뱀게임 - 사람 vs AI",
        )
        self.canvas.create_text(
            WIDTH / 2, HEIGHT / 2 - 15, fill=PLAYER_COLOR,
            font=("Arial", 13), text="방향키: 플레이어(초록) 조작",
        )
        self.canvas.create_text(
            WIDTH / 2, HEIGHT / 2 + 10, fill=AI_COLOR,
            font=("Arial", 13), text="AI(파랑)가 자동으로 사과를 먹으러 갑니다",
        )
        self.canvas.create_text(
            WIDTH / 2, HEIGHT / 2 + 45, fill=TEXT_COLOR,
            font=("Arial", 14), text="스페이스바를 눌러 시작하세요",
        )

    def get_winner_text(self):
        if self.player_score > self.ai_score:
            return "플레이어 승리!"
        if self.ai_score > self.player_score:
            return "AI 승리!"
        return "무승부!"

    def draw_game_over(self):
        self.canvas.create_rectangle(
            0, HEIGHT / 2 - 60, WIDTH, HEIGHT / 2 + 60, fill="black", stipple="gray50"
        )
        self.canvas.create_text(
            WIDTH / 2, HEIGHT / 2 - 25, fill=TEXT_COLOR,
            font=("Arial", 24, "bold"), text="게임 오버",
        )
        self.canvas.create_text(
            WIDTH / 2, HEIGHT / 2 + 5, fill=TEXT_COLOR,
            font=("Arial", 16, "bold"), text=self.get_winner_text(),
        )
        self.canvas.create_text(
            WIDTH / 2, HEIGHT / 2 + 30, fill=TEXT_COLOR,
            font=("Arial", 13),
            text=f"플레이어: {self.player_score}  |  AI: {self.ai_score}  (스페이스바로 재시작)",
        )


def main():
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
