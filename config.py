import pygame
import os
from databases import options

os.environ["SDL_VIDEO_CENTERED"] = "1" # Makes sure the window is centered after resolution change

BLACK, WHITE, LIGHT_GREY, GREY, DARK_GREY, DARK_GREEN = (0, 0, 0), (255, 255, 255), (128, 128, 128), (100, 100, 100), (58, 58, 58), (0, 100, 0)
LIGHT_BLUE, DARK_BLUE, ORANGE, YELLOW, GREEN, PURPLE, RED = (0, 255, 255), (0, 0, 153), (255, 153, 51), (255, 255, 0), (0, 255, 0), (153, 51, 255), (255, 0, 0) # Colors for tetrominos

BASE_WIDTH, BASE_HEIGHT = 320, 180 # Base resolution to scale from
RESOLUTION_SCALING_MULTIPLIERS = [2, 3, 4, 5, 6, 8, 10, 12] # Respectively 640x360, 960x540, 1280x720, 1600x900, 1920x1080, 2560x1440, 3200x1800, 3840x2160

USER_CHOICE_SCALE = options["resolution_scale_index"] # 1 IS DEFAULT (960x540)

pygame.font.init()

def update_resolution(scale_index):
      global CELL_EDGE, RESOLUTION_DISPLAY, CENTER, PREDEFINED_POSITIONS, WINDOW, FONT
      multiplier = RESOLUTION_SCALING_MULTIPLIERS[scale_index]
      
      width = BASE_WIDTH * multiplier
      height = BASE_HEIGHT * multiplier
      CELL_EDGE = 8 * multiplier  # Scale the grid size
      RESOLUTION_DISPLAY = {"width": width,
                              "height": height}
      WINDOW = pygame.display.set_mode((RESOLUTION_DISPLAY["width"], RESOLUTION_DISPLAY["height"]))
      FONT = pygame.font.SysFont(None, CELL_EDGE)
      CENTER = RESOLUTION_DISPLAY["width"] // 2, RESOLUTION_DISPLAY["height"] // 2
      PREDEFINED_POSITIONS = {
            "CENTER": lambda: CENTER,
      }

update_resolution(USER_CHOICE_SCALE)

pygame.display.set_caption("Tetris")

class Element:
      def __init__(self, num_cells_width: int, num_cells_height: int, cell_edge: int, surface=False, center=None, **kwargs):
            """
            Initializes a pygame.Rect or pygame.Surface element with the given dimensions.
            
            Parameters:
                  num_cells_width (int): The width of the element in terms of the number of cells.
                  num_cells_height (int): The height of the element in terms of the number of cells.
                  cell_edge (int): Size of a cell's edge, used to scale the element.
                  surface (bool): If True, create a pygame.Surface; otherwise, create a pygame.Rect.
                  center (tuple[int, int], optional): Center coordinates (x, y). Defaults to None.
                  kwargs (dict): Additional keyword arguments to modify the element attributes.
            """
            self.cell_edge = cell_edge
            self.num_cells_width = num_cells_width
            self.num_cells_height = num_cells_height
            self.element = surface
            self.center = center
            self.center_str = False
            self.kwargs = kwargs
            
            # Calculate width and height
            self.width = self.num_cells_width * self.cell_edge
            self.height = self.num_cells_height * self.cell_edge
            
            # Resolve center if it's a predefined string
            if self.element and isinstance(center, str) and center in PREDEFINED_POSITIONS:
                  self.center_str = self.center
                  self.center = PREDEFINED_POSITIONS[center]()
            else:
                  self.center = center  # If it's already a tuple, just use it
            
            # Create either a Rect or Surface depending on the 'surface' flag
            if self.element:
                  self.element = pygame.Surface((self.width, self.height))
                  self.rect = self.element.get_rect(center=self.center)
            else:
                  self.element = pygame.Rect(0, 0, self.width, self.height)
                  if self.center:
                        self.kwargs["center"] = self.center
            
            # Apply additional attributes if any
            for attr, expr in self.kwargs.items():
                  setattr(self.element, attr, eval(expr, globals(), locals()))

      def update(self, cell_edge: int) -> None:
            """Updates the element's size and position"""
            self.cell_edge = cell_edge
            self.width = self.num_cells_width * self.cell_edge
            self.height = self.num_cells_height * self.cell_edge
            
            if self.center and self.center_str:
                  self.center = PREDEFINED_POSITIONS[self.center_str]()
            
            # Check the type of the element to update either Rect or Surface accordingly
            if isinstance(self.element, pygame.Surface):
                  self.element = pygame.Surface((self.width, self.height))
                  # If center is passed, update it; otherwise, keep the previous center
                  if self.center:
                        self.rect = self.element.get_rect(center=self.center)  # Update the rect with the new center
                  else:
                        self.rect = self.element.get_rect()  # Use default positioning if no center is given
            elif isinstance(self.element, pygame.Rect):
                  self.element = pygame.Rect(0, 0, self.width, self.height)
            
            for attr, expr in self.kwargs.items():
                  setattr(self.element, attr, eval(expr, globals(), locals()))

      def draw(self, screen) -> None:
            """Draw the element if it's a surface."""
            if self.element:
                  screen.blit(self.element, self.rect)

PLAYFIELD_FRAME = Element(10, 20, CELL_EDGE, center="CENTER")
NEXT_FRAME = Element(6, 6, CELL_EDGE, top="PLAYFIELD_FRAME.element.top", centerx="(RESOLUTION_DISPLAY['width'] + PLAYFIELD_FRAME.element.right) // 2")
HOLD_FRAME = Element(6, 6, CELL_EDGE, top="PLAYFIELD_FRAME.element.top", centerx="PLAYFIELD_FRAME.element.left // 2")
SCORE_FRAME = Element(6, 12, CELL_EDGE, bottom="PLAYFIELD_FRAME.element.bottom", centerx="PLAYFIELD_FRAME.element.left // 2")

PAUSE_OVERLAY = Element(6, 15, CELL_EDGE, surface=True, center="CENTER")
OPTIONS_OVERLAY = Element(6, 15, CELL_EDGE, surface=True, center="CENTER")
KEY_MAPPING_OVERLAY = Element(15, 20, CELL_EDGE, surface=True, center="CENTER")
KEYBIND_OVERLAY = Element(9, 9, CELL_EDGE, surface=True, center="CENTER")
RESET_KEY_MAPPING_OVERLAY = Element(9, 9, CELL_EDGE, surface=True, center="CENTER")
RESOLUTIONS_OVERLAY = Element(8, 16, CELL_EDGE, surface=True, center="CENTER")
GAME_OVER_OVERLAY = Element(12, 12, CELL_EDGE, surface=True, center="CENTER")
KEEP_CHANGES_OVERLAY = Element(7, 7, CELL_EDGE, surface=True, center="CENTER")

FRAMES = [
      PLAYFIELD_FRAME,
      NEXT_FRAME,
      HOLD_FRAME,
      SCORE_FRAME,
]

OVERLAYS = [
      PAUSE_OVERLAY,
      OPTIONS_OVERLAY,
      KEY_MAPPING_OVERLAY,
      KEYBIND_OVERLAY,
      RESET_KEY_MAPPING_OVERLAY,
      RESOLUTIONS_OVERLAY,
      GAME_OVER_OVERLAY,
      KEEP_CHANGES_OVERLAY,
]

# Tetromino shapes as lists of strings, "0" represents filled cell, "." represents empty cell.
# These shapes follow the SRS (Super Rotation System) standard used in Tetris, https://tetris.wiki/images/3/3d/SRS-pieces.png is the source for my shapes.
# I and O tetrominos are 4x4, others are 3x3

I = [["....",
      "0000",
      "....",
      "...."],
     ["..0.",
      "..0.",
      "..0.",
      "..0."],
     ["....",
      "....",
      "0000",
      "...."],
     [".0..",
      ".0..",
      ".0..",
      ".0.."]]

J = [["0..",
      "000",
      "..."],
     [".00",
      ".0.",
      ".0."],
     ["...",
      "000",
      "..0"],
     [".0.",
      ".0.",
      "00."]]

L = [["..0",
      "000",
      "..."],
     [".0.",
      ".0.",
      ".00"],
     ["...",
      "000",
      "0.."],
     ["00.",
      ".0.",
      ".0."]]

O = [[".00.",
      ".00.",
      "...."],
     [".00.",
      ".00.",
      "...."],
     [".00.",
      ".00.",
      "...."],
     [".00.",
      ".00.",
      "...."]]

S = [[".00",
      "00.",
      "..."],
     [".0.",
      ".00",
      "..0"],
     ["...",
      ".00",
      "00."],
     ["0..",
      "00.",
      ".0."]]

T = [[".0.",
      "000",
      "..."],
     [".0.",
      ".00",
      ".0."],
     ["...",
      "000",
      ".0."],
     [".0.",
      "00.",
      ".0."]]

Z = [["00.",
      ".00",
      "..."],
     ["..0",
      ".00",
      ".0."],
     ["...",
      "00.",
      ".00"],
     [".0.",
      "00.",
      "0.."]]

# Used for wall kicks
STANDARD_KICKS = {
    (0, 1): [(0, 0), (-1, 0), (-1, +1), (0, -2), (-1, -2)],
    (1, 0): [(0, 0), (+1, 0), (+1, -1), (0, +2), (+1, +2)],
    (1, 2): [(0, 0), (+1, 0), (+1, -1), (0, +2), (+1, +2)],
    (2, 1): [(0, 0), (-1, 0), (-1, +1), (0, -2), (-1, -2)],
    (2, 3): [(0, 0), (+1, 0), (+1, +1), (0, -2), (+1, -2)],
    (3, 2): [(0, 0), (-1, 0), (-1, -1), (0, +2), (-1, +2)],
    (3, 0): [(0, 0), (-1, 0), (-1, -1), (0, +2), (-1, +2)],
    (0, 3): [(0, 0), (+1, 0), (+1, +1), (0, -2), (+1, -2)],
}

I_KICKS = {
    (0, 1): [(0, 0), (-2, 0), (+1, 0), (-2, -1), (+1, +2)],
    (1, 0): [(0, 0), (+2, 0), (-1, 0), (+2, +1), (-1, -2)],
    (1, 2): [(0, 0), (-1, 0), (+2, 0), (-1, +2), (+2, -1)],
    (2, 1): [(0, 0), (+1, 0), (-2, 0), (+1, -2), (-2, +1)],
    (2, 3): [(0, 0), (+2, 0), (-1, 0), (+2, +1), (-1, -2)],
    (3, 2): [(0, 0), (-2, 0), (+1, 0), (-2, -1), (+1, +2)],
    (3, 0): [(0, 0), (+1, 0), (-2, 0), (+1, -2), (-2, +1)],
    (0, 3): [(0, 0), (-1, 0), (+2, 0), (-1, +2), (+2, -1)],
}
