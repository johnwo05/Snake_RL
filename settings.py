# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BODY = (255, 100, 0)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 800  # 16 * 48 or 32 * 24 or 64 * 12 768
FPS = 25
# FPS = 20

TITLE = "SNAKE_RL"
BGCOLOR = DARKGREY
SCORE_FILE = "score.txt"
GENERATION_FILE = 'generation.txt'
Q_FILE = "Q.txt"
saved_Q = "saved_Q.txt"

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE


#AI STATES
CLEAR_AHEAD = 0
CLEAR_LEFT = 0
CLEAR_RIGHT = 0

FOOD_AHEAD = 0
FOOD_LEFT = 0
FOOD_RIGHT = 0

WALL_AHEAD = 0
WALL_LEFT = 0
WALL_RIGHT = 0
