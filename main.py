import pygame
import sys
import math

# ---------- CONFIG ----------
WIDTH, HEIGHT = 900, 900
ROWS, COLS = 200, 200   # High resolution internal grid
CELL_W = WIDTH / COLS
CELL_H = HEIGHT / ROWS

BG_COLOR = (245, 245, 245)
OBSTACLE_COLOR = (30, 30, 30)

BRUSH_RADIUS = 12  # pixels

# ---------- INIT ----------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Continuous Obstacle Editor")
clock = pygame.time.Clock()

# Occupancy grid: 0 = free, 1 = obstacle
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# ---------- FUNCTIONS ----------
def world_to_grid(x, y):
    col = int(x / CELL_W)
    row = int(y / CELL_H)
    return row, col

def draw_obstacles():
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c]:
                pygame.draw.rect(
                    screen,
                    OBSTACLE_COLOR,
                    (c * CELL_W, r * CELL_H, CELL_W + 1, CELL_H + 1)
                )

def paint_circle(pos, value):
    mx, my = pos
    grid_r, grid_c = world_to_grid(mx, my)

    brush_cells_x = int(BRUSH_RADIUS / CELL_W) + 1
    brush_cells_y = int(BRUSH_RADIUS / CELL_H) + 1

    for dr in range(-brush_cells_y, brush_cells_y + 1):
        for dc in range(-brush_cells_x, brush_cells_x + 1):
            r = grid_r + dr
            c = grid_c + dc

            if 0 <= r < ROWS and 0 <= c < COLS:
                cx = (c + 0.5) * CELL_W
                cy = (r + 0.5) * CELL_H

                if math.hypot(cx - mx, cy - my) <= BRUSH_RADIUS:
                    grid[r][c] = value

# ---------- MAIN LOOP ----------
running = True
while running:
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_buttons = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    if mouse_buttons[0]:      # Left click → draw obstacle
        paint_circle(mouse_pos, 1)
    elif mouse_buttons[2]:    # Right click → erase
        paint_circle(mouse_pos, 0)

    draw_obstacles()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
