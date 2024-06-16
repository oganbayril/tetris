import pygame

BLACK, WHITE, LIGHT_GREY, GREY, DARK_GREY, DARK_GREEN = (0, 0, 0), (255, 255, 255), (128, 128, 128), (100, 100, 100), (58, 58, 58), (0, 100, 0)
LIGHT_BLUE, DARK_BLUE, ORANGE, YELLOW, GREEN, PURPLE, RED = (0, 255, 255), (0, 0, 153), (255, 153, 51), (255, 255, 0), (0, 255, 0), (153, 51, 255), (255, 0, 0)
WIDTH, HEIGHT = 800, 600
SQUARE = 20

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
pygame.font.init()
font = pygame.font.SysFont(None, SQUARE)

PLAY_SCREEN_X_START, PLAY_SCREEN_Y_START, PLAY_SCREEN_X_END, PLAY_SCREEN_Y_END = 300, 100, 500, 500
PLAY_SCREEN = pygame.Rect(PLAY_SCREEN_X_START, PLAY_SCREEN_Y_START, PLAY_SCREEN_X_END - PLAY_SCREEN_X_START, PLAY_SCREEN_Y_END - PLAY_SCREEN_Y_START)

NEXT_SCREEN_X_START, NEXT_SCREEN_Y_START, NEXT_SCREEN_X_END, NEXT_SCREEN_Y_END = 600, 100, 720, 220
NEXT_SCREEN = pygame.Rect(NEXT_SCREEN_X_START, NEXT_SCREEN_Y_START, NEXT_SCREEN_X_END - NEXT_SCREEN_X_START, NEXT_SCREEN_Y_END - NEXT_SCREEN_Y_START)

HOLD_SCREEN_X_START, HOLD_SCREEN_Y_START, HOLD_SCREEN_X_END, HOLD_SCREEN_Y_END = 80, 100, 200, 220
HOLD_SCREEN = pygame.Rect(HOLD_SCREEN_X_START, HOLD_SCREEN_Y_START, HOLD_SCREEN_X_END - HOLD_SCREEN_X_START, HOLD_SCREEN_Y_END - HOLD_SCREEN_Y_START)

SCORE_SCREEN_X_START, SCORE_SCREEN_Y_START, SCORE_SCREEN_X_END, SCORE_SCREEN_Y_END = 80, 280, 200, 500
SCORE_SCREEN = pygame.Rect(SCORE_SCREEN_X_START, SCORE_SCREEN_Y_START, SCORE_SCREEN_X_END - SCORE_SCREEN_X_START, SCORE_SCREEN_Y_END - SCORE_SCREEN_Y_START)

PAUSE_SCREEN_WIDTH, PAUSE_SCREEN_HEIGHT = 180, 300
PAUSE_SCREEN = pygame.Surface((PAUSE_SCREEN_WIDTH, PAUSE_SCREEN_HEIGHT))
PAUSE_SCREEN_RECT = PAUSE_SCREEN.get_rect(center=(WIDTH // 2, HEIGHT // 2))

OPTIONS_SCREEN_WIDTH, OPTIONS_SCREEN_HEIGHT = 300, 400
OPTIONS_SCREEN = pygame.Surface((OPTIONS_SCREEN_WIDTH, OPTIONS_SCREEN_HEIGHT))
OPTIONS_SCREEN_RECT = OPTIONS_SCREEN.get_rect(center=(WIDTH // 2, HEIGHT // 2))

KEYBIND_SCREEN_WIDTH, KEYBIND_SCREEN_HEIGHT = 250, 200
KEYBIND_SCREEN = pygame.Surface((KEYBIND_SCREEN_WIDTH, KEYBIND_SCREEN_HEIGHT))
KEYBIND_SCREEN_RECT = KEYBIND_SCREEN.get_rect(center=(WIDTH // 2, HEIGHT // 2))

RESET_OPTIONS_SCREEN_WIDTH, RESET_OPTIONS_SCREEN_HEIGHT = 200, 160
RESET_OPTIONS_SCREEN = pygame.Surface((RESET_OPTIONS_SCREEN_WIDTH, RESET_OPTIONS_SCREEN_HEIGHT))
RESET_OPTIONS_SCREEN_RECT = RESET_OPTIONS_SCREEN.get_rect(center=(WIDTH // 2, HEIGHT // 2))

GAME_OVER_SCREEN_WIDTH, GAME_OVER_SCREEN_HEIGHT = 240, 240
GAME_OVER_SCREEN = pygame.Surface((GAME_OVER_SCREEN_WIDTH, GAME_OVER_SCREEN_HEIGHT))
GAME_OVER_SCREEN_RECT = GAME_OVER_SCREEN.get_rect(center=(WIDTH // 2, HEIGHT // 2))

I = [['.....',
      '.0000',
      '.....',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..']]

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

O = [['.....',
      '..00.',
      '..00.',
      '.....',
      '.....']]

S = [['.....',
      '..00.',
      '.00.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
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

Z = [['.....',
      '.00..',
      '..00.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]