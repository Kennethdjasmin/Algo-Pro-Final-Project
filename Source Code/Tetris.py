import pygame
import random

pygame.font.init()
pygame.init()


s_width = 800
s_height = 700
play_width = 300
play_height = 600
block_size = 30
img1_old = pygame.image.load(r'1.png')
img1 = pygame.transform.scale(img1_old, (30, 30))
img2_old = pygame.image.load(r'2.png')
img2 = pygame.transform.scale(img2_old, (30, 30))
img3_old = pygame.image.load(r'3.png')
img3 = pygame.transform.scale(img3_old, (30, 30))
img4_old = pygame.image.load(r'4.png')
img4 = pygame.transform.scale(img4_old, (30, 30))
bg_img = pygame.image.load(r'background.jpeg')
row_clear_sound = pygame.mixer.Sound("ES_Magic Chime - SFX Producer.wav")
row_clear_sound.set_volume(0.5)
lose_sound = pygame.mixer.Sound("ES_Video Game Descend 8 - SFX Producer.wav")
pygame.mixer.music.load("ES_Caracal - Leah Ryder.mp3")
pygame.mixer.music.set_volume(0.1)

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height



S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [img1, img2, img3, img4, img4, img2, img3]



class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_pos={}):
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

    # len(grid) is the row on the grid (y-axis), len(grid[i]) is the column (x-axis)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j,i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("couriernew", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    # len(grid) is the row on the grid (y-axis), len(grid[i]) is the column (x-axis)
    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size), (sx+play_width, sy+ i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size, sy),(sx + j*block_size, sy + play_height))


def clear_rows(grid, locked):

    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            ind = i
            pygame.mixer.Sound.play(row_clear_sound)
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc


def draw_next_shape(shape, surface):
    z = 0
    num = 0
    ex = [30, 15, 0, -15, -20]
    font = pygame.font.SysFont('couriernew', 30, bold = True)
    label = font.render('Next Shape', 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        if line == O[0][i]:
            z=z+1
            num = z-1

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                win.blit(shape.color, (sx + j * block_size + 15,sy + i * block_size + ex[num]))

    surface.blit(label, (sx + 10, sy - 30))


def update_score(nscore):
    score = max_score()

    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score


def draw_window(surface, grid, score=0, last_score = 0):
    win.blit(bg_img,(0,0))

    pygame.font.init()
    font = pygame.font.SysFont('couriernew', 60, bold = True)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 10))


    font = pygame.font.SysFont('couriernew', 30, bold = True)
    label = font.render('Score: ' + str(score), 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    surface.blit(label, (sx + 20, sy + 160))


    font = pygame.font.SysFont('couriernew', 25, bold=True)
    label = font.render('High Score: ' + last_score, 1, (255,255,255))

    sx = top_left_x - 250
    sy = top_left_y + 100

    surface.blit(label, (sx + 10, sy + 160))

    # len(grid) is the row on the grid (y-axis), len(grid[i]) is the column (x-axis)
    # extends to 20
    for i in range(len(grid)):
        # extends to 10
        for j in range(len(grid[i])):
            if grid[i][j] in shape_colors:
                win.blit(grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size))
            else:
                pygame.draw.rect(surface, grid[i][j],
                (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

    # white rectangle surrounding the grid
    pygame.draw.rect(surface, (255, 255, 255), (top_left_x-10, top_left_y-10, play_width+20, play_height+20), 10, 10)

    draw_grid(surface, grid)



def main(win):
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                fall_speed = 0.05
            else:
                fall_speed = 0.27
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        draw_window(win, grid, score, last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(win, "YOU LOST!", 80, (255,255,255))
            pygame.display.update()
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(lose_sound)
            pygame.time.delay(1500)
            run = False
            update_score(score)


def main_menu(win):
    run = True
    pygame.mixer.music.play(-1)
    while run:
        win.blit(bg_img,(0,0))
        draw_text_middle(win, 'Press Any Key To Play', 60, (255,255,255))
        pygame.display.update()
        if pygame.mixer.music.get_busy():
            pass
        else:
            pygame.mixer.music.play(-1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)