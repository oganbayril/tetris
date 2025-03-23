import pygame
import random
import os
import sys
import json

from button import Button
import databases
import config as cfg

# Full path of your background image file (optional)
background_image_file = r"C:\Users\PC\Desktop\XDXD.jpg"

check_if_background_image_exists = os.path.exists(background_image_file)

if check_if_background_image_exists:
     BACKGROUND_IMAGE = pygame.image.load(os.path.join(databases.script_dir, background_image_file))
     BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (cfg.RESOLUTION_DISPLAY["width"], cfg.RESOLUTION_DISPLAY["height"]))

tetrominos = [cfg.I, cfg.J, cfg.L, cfg.O, cfg.S, cfg.T, cfg.Z]
tetromino_colors = [cfg.LIGHT_BLUE, cfg.DARK_BLUE,cfg.ORANGE, cfg.YELLOW, cfg.GREEN, cfg.PURPLE, cfg.RED]
current_keys = databases.keys
current_scores = databases.scores
starting_level = 1

class Tetris:
     def __init__(self):
          self.reset_game()

     def reset_game(self, level=1):
          self.x = cfg.PLAYFIELD_FRAME.element.left
          self.y = cfg.PLAYFIELD_FRAME.element.top
          self.rows = cfg.PLAYFIELD_FRAME.num_cells_width
          self.columns = 20
          self.rotation = 0
          self.bag = tetrominos.copy()
          self.tetromino = self.get_tetromino()
          self.next_tetromino = self.get_tetromino()
          self.hold_tetromino = [[]]
          self.score = 0
          self.level = level
          self.lines = 0
          self.board = [[0 for _ in range(self.rows)] for _ in range(self.columns)]
          
     def get_tetromino(self):
          if not self.bag:
               self.bag = tetrominos.copy()
          random_tetromino = self.bag[random.randint(0, len(self.bag) - 1)]
          self.bag.remove(random_tetromino)
          
          return random_tetromino
     
     def draw_window(self):
          cfg.WINDOW.fill(cfg.BLACK)
          if check_if_background_image_exists:
               cfg.WINDOW.blit(BACKGROUND, (0, 0))
          pygame.draw.rect(cfg.WINDOW, cfg.BLACK, cfg.PLAYFIELD_FRAME.element)
          pygame.draw.rect(cfg.WINDOW, cfg.BLACK, cfg.NEXT_FRAME.element)
          pygame.draw.rect(cfg.WINDOW, cfg.BLACK, cfg.HOLD_FRAME.element)
          pygame.draw.rect(cfg.WINDOW, cfg.BLACK, cfg.SCORE_FRAME.element)
          
          # Draw next tetromino screen
          pygame.draw.rect(cfg.WINDOW, cfg.LIGHT_GREY, cfg.NEXT_FRAME.element, width=1)
          next_text = cfg.font.render("NEXT", True, cfg.WHITE)
          next_rect = next_text.get_rect()
          next_rect.centerx = cfg.NEXT_FRAME.element.centerx
          next_rect.y = cfg.NEXT_FRAME.element.y + cfg.CELL_EDGE # Small increment so the text isn't directly on the border of the rectangle
          cfg.WINDOW.blit(next_text, next_rect)
          
          # Draw hold screen
          pygame.draw.rect(cfg.WINDOW, cfg.LIGHT_GREY, cfg.HOLD_FRAME.element, width=1)
          hold_text = cfg.font.render("HOLD", True, cfg.WHITE)
          hold_rect = hold_text.get_rect()
          hold_rect.centerx = cfg.HOLD_FRAME.element.centerx
          hold_rect.y = cfg.HOLD_FRAME.element.y + cfg.CELL_EDGE
          cfg.WINDOW.blit(hold_text, hold_rect)
          
          # Draw score screen
          pygame.draw.rect(cfg.WINDOW, cfg.LIGHT_GREY, cfg.SCORE_FRAME.element, width=1)
          score_text = cfg.font.render("SCORE", True, cfg.WHITE)
          level_text = cfg.font.render("LEVEL", True, cfg.WHITE)
          lines_text = cfg.font.render("LINES", True, cfg.WHITE)
          
          score_text_rect = score_text.get_rect()
          level_text_rect = level_text.get_rect()
          lines_text_rect = lines_text.get_rect()
          score_text_rect.centerx = level_text_rect.centerx = lines_text_rect.centerx = cfg.SCORE_FRAME.element.centerx
          score_text_rect.y = cfg.SCORE_FRAME.element.y + cfg.CELL_EDGE
          level_text_rect.y = cfg.SCORE_FRAME.element.y + cfg.CELL_EDGE * 5
          lines_text_rect.y = cfg.SCORE_FRAME.element.y + cfg.CELL_EDGE * 9
          
          cfg.WINDOW.blit(score_text, score_text_rect)
          cfg.WINDOW.blit(level_text, level_text_rect)
          cfg.WINDOW.blit(lines_text, lines_text_rect)
     
     def draw_gameloop(self):
          # Draw lines in the play screen
          line_x = cfg.PLAYFIELD_FRAME.element.left
          line_y = cfg.PLAYFIELD_FRAME.element.top
          
          for _ in range(self.rows+1):
               pygame.draw.line(cfg.WINDOW, cfg.GREY, (line_x, line_y), (line_x, cfg.PLAYFIELD_FRAME.element.bottom))
               for _ in range(self.columns + 1):
                    pygame.draw.line(cfg.WINDOW, cfg.GREY, (line_x, line_y), (cfg.PLAYFIELD_FRAME.element.right, line_y))
                    line_y += cfg.CELL_EDGE
               line_x += cfg.CELL_EDGE
               
               line_y = cfg.PLAYFIELD_FRAME.element.top
          line_x = cfg.PLAYFIELD_FRAME.element.left
          
          # Draw hold tetromino
          hold_x_positions = []
          hold_y_positions = []
          
          if len(self.hold_tetromino) == 4 or (len(self.hold_tetromino) == 2 and self.hold_tetromino != cfg.I):
               for i, string in enumerate(self.hold_tetromino[0], start=-2):
                    for j, tetromino_piece in enumerate(string, start=-2):
                         if tetromino_piece == "0":
                              x_position = (cfg.HOLD_FRAME.element.left + cfg.HOLD_FRAME.element.right) / 2 + j * cfg.CELL_EDGE - cfg.CELL_EDGE / 2
                              y_position = (cfg.HOLD_FRAME.element.top + cfg.HOLD_FRAME.element.bottom) / 2 + i * cfg.CELL_EDGE
                              hold_x_positions.append(x_position)
                              hold_y_positions.append(y_position)
          elif self.hold_tetromino == cfg.I:
               for i, string in enumerate(self.hold_tetromino[0], start=-2):
                    for j, tetromino_piece in enumerate(string, start=-2):
                         if tetromino_piece == "0":
                              x_position = (cfg.HOLD_FRAME.element.left + cfg.HOLD_FRAME.element.right) / 2 + (j - 1) * cfg.CELL_EDGE
                              y_position = (cfg.HOLD_FRAME.element.top + cfg.HOLD_FRAME.element.bottom) / 2 + (i + 1) * cfg.CELL_EDGE - cfg.CELL_EDGE / 2
                              hold_x_positions.append(x_position)
                              hold_y_positions.append(y_position)
          else:
               for i, string in enumerate(self.hold_tetromino[0], start=-2):
                    for j, tetromino_piece in enumerate(string, start=-2):
                         if tetromino_piece == "0":
                              x_position = (cfg.HOLD_FRAME.element.left + cfg.HOLD_FRAME.element.right) / 2 + (j - 1) * cfg.CELL_EDGE
                              y_position = (cfg.HOLD_FRAME.element.top + cfg.HOLD_FRAME.element.bottom) / 2 + i * cfg.CELL_EDGE
                              hold_x_positions.append(x_position)
                              hold_y_positions.append(y_position)

          for x, y in list(zip(hold_x_positions, hold_y_positions)):
               pygame.draw.rect(cfg.WINDOW, tetromino_colors[tetrominos.index(self.hold_tetromino)], (x, y, cfg.CELL_EDGE - 1, cfg.CELL_EDGE - 1))
          
          # Draw next tetromino
          next_x_positions = []
          next_y_positions = []
          
          if len(self.next_tetromino) == 4 or (len(self.next_tetromino) == 2 and self.next_tetromino != cfg.I):
               for i, string in enumerate(self.next_tetromino[0], start=-2):
                    for j, tetromino_piece in enumerate(string, start=-2):
                         if tetromino_piece == "0":
                              x_position = (cfg.NEXT_FRAME.element.left + cfg.NEXT_FRAME.element.right) / 2 + j * cfg.CELL_EDGE - cfg.CELL_EDGE / 2
                              y_position = (cfg.NEXT_FRAME.element.top + cfg.NEXT_FRAME.element.bottom) / 2 + i * cfg.CELL_EDGE
                              next_x_positions.append(x_position)
                              next_y_positions.append(y_position)
          elif self.next_tetromino == cfg.I:
               for i, string in enumerate(self.next_tetromino[0], start=-2):
                    for j, tetromino_piece in enumerate(string, start=-2):
                         if tetromino_piece == "0":
                              x_position = (cfg.NEXT_FRAME.element.left + cfg.NEXT_FRAME.element.right) / 2 + (j - 1) * cfg.CELL_EDGE
                              y_position = (cfg.NEXT_FRAME.element.top + cfg.NEXT_FRAME.element.bottom) / 2 + (i + 1) * cfg.CELL_EDGE - cfg.CELL_EDGE / 2
                              next_x_positions.append(x_position)
                              next_y_positions.append(y_position)
          else:
               for i, string in enumerate(self.next_tetromino[0], start=-2):
                    for j, tetromino_piece in enumerate(string, start=-2):
                         if tetromino_piece == "0":
                              x_position = (cfg.NEXT_FRAME.element.left + cfg.NEXT_FRAME.element.right) / 2 + (j - 1) * cfg.CELL_EDGE
                              y_position = (cfg.NEXT_FRAME.element.top + cfg.NEXT_FRAME.element.bottom) / 2 + i * cfg.CELL_EDGE
                              next_x_positions.append(x_position)
                              next_y_positions.append(y_position)

          for x, y in list(zip(next_x_positions, next_y_positions)):
               pygame.draw.rect(cfg.WINDOW, tetromino_colors[tetrominos.index(self.next_tetromino)], (x, y, cfg.CELL_EDGE - 1, cfg.CELL_EDGE - 1))
          
          # Draw placed tetrominos
          for y, row in enumerate(self.board):
               for x, val in enumerate(row):
                    if val != 0:
                         pygame.draw.rect(cfg.WINDOW, tetromino_colors[val - 1], (cfg.PLAYFIELD_FRAME.element.left + (x * cfg.CELL_EDGE), cfg.PLAYFIELD_FRAME.element.top + (y * cfg.CELL_EDGE), cfg.CELL_EDGE - 1, cfg.CELL_EDGE - 1))
          
          # Draw corresponding numbers in score screen
          score_number = cfg.font.render(str(self.score), True, cfg.WHITE)
          level_number = cfg.font.render(str(self.level), True, cfg.WHITE)
          lines_number = cfg.font.render(str(self.lines), True, cfg.WHITE)
          
          score_number_rect = score_number.get_rect()
          level_number_rect = level_number.get_rect()
          lines_number_rect = lines_number.get_rect()
          score_number_rect.centerx = level_number_rect.centerx = lines_number_rect.centerx = cfg.SCORE_FRAME.element.centerx
          score_number_rect.y = cfg.SCORE_FRAME.element.y + cfg.CELL_EDGE * 2
          level_number_rect.y = cfg.SCORE_FRAME.element.y + cfg.CELL_EDGE * 6
          lines_number_rect.y = cfg.SCORE_FRAME.element.y + cfg.CELL_EDGE * 10
          
          cfg.WINDOW.blit(score_number, score_number_rect)
          cfg.WINDOW.blit(level_number, level_number_rect)
          cfg.WINDOW.blit(lines_number, lines_number_rect)
          
     def draw_tetromino(self):
          global min_x, max_x, x_positions, y_positions
          min_x, max_x = cfg.PLAYFIELD_FRAME.element.right, cfg.PLAYFIELD_FRAME.element.left
          min_y, max_y = cfg.PLAYFIELD_FRAME.element.bottom, cfg.PLAYFIELD_FRAME.element.top
          x_positions, y_positions = [], []

          for i, string in enumerate(self.tetromino[self.rotation], start=-2):
               for j, tetromino_piece in enumerate(string, start=-2):
                    if tetromino_piece == "0":
                         x_position = (self.x + cfg.PLAYFIELD_FRAME.element.right) / 2 + (j - 1) * cfg.CELL_EDGE
                         y_position = self.y + (i + 1) * cfg.CELL_EDGE
                         min_x = min(min_x, x_position)
                         max_x = max(max_x, x_position + cfg.CELL_EDGE)
                         min_y = min(min_y, y_position)
                         max_y = max(max_y, y_position)
                         x_positions.append(x_position)
                         y_positions.append(y_position)
          
          # Implementing wall kick
          while min(x_positions) < cfg.PLAYFIELD_FRAME.element.left:
               x_positions = [x + cfg.CELL_EDGE for x in x_positions]
               self.x += 2 * cfg.CELL_EDGE
          while max(x_positions) >= cfg.PLAYFIELD_FRAME.element.right:
               x_positions = [x - cfg.CELL_EDGE for x in x_positions]
               self.x -= 2 * cfg.CELL_EDGE
          
          # Draw tetromino
          for x, y in zip(x_positions, y_positions):
               pygame.draw.rect(cfg.WINDOW, tetromino_colors[tetrominos.index(self.tetromino)], (x, y, cfg.CELL_EDGE - 1, cfg.CELL_EDGE - 1))

     
     def place_tetromino(self):
          # Update game board with tetromino and assign colors
          for i, string in enumerate(self.tetromino[self.rotation], start=-2):
               for j, tetromino_piece in enumerate(string, start=-2):
                    if tetromino_piece == "0":
                         x_position = int((self.x + cfg.PLAYFIELD_FRAME.element.right) / 2 + (j - 1) * cfg.CELL_EDGE)
                         y_position = self.y + (i + 1) * cfg.CELL_EDGE
                         grid_x = int((x_position - cfg.PLAYFIELD_FRAME.element.left) / cfg.CELL_EDGE)
                         grid_y = int((y_position - cfg.PLAYFIELD_FRAME.element.top) / cfg.CELL_EDGE)
                         self.board[grid_y][grid_x] = tetrominos.index(self.tetromino) + 1
          pygame.time.delay(10) # Added a small delay to remove any accidental inputs like 2 tetrominos hard dropping at the same time (i don't know if this actually works, might need to change later)
          
          
     def check_collision_y(self):
          # Check bottom collision
          if max(y_positions) == cfg.PLAYFIELD_FRAME.element.bottom-cfg.CELL_EDGE:
               return True
          
          # Check tetromino collision with other blocks
          for i, string in enumerate(self.tetromino[self.rotation], start=-2):
               for j, tetromino_piece in enumerate(string, start=-2):
                    if tetromino_piece == "0":
                         x_position = int((self.x + cfg.PLAYFIELD_FRAME.element.right) / 2 + (j - 1) * cfg.CELL_EDGE)
                         y_position = self.y + (i + 1) * cfg.CELL_EDGE
                         grid_x = int((x_position - cfg.PLAYFIELD_FRAME.element.left) / cfg.CELL_EDGE)
                         grid_y = int((y_position - cfg.PLAYFIELD_FRAME.element.top) / cfg.CELL_EDGE)
                         
                         if grid_y + 1 >= len(self.board):
                              return True
                         
                         if self.board[grid_y+1][grid_x] != 0:
                              return True
          return False
     
     def check_collision_x(self, direction):
          # Check left or right collision
          for i, string in enumerate(self.tetromino[self.rotation], start=-2):
               for j, tetromino_piece in enumerate(string, start=-2):
                    if tetromino_piece == "0":
                         x_position = (self.x + cfg.PLAYFIELD_FRAME.element.right) / 2 + (j - 1) * cfg.CELL_EDGE
                         y_position = self.y + (i + 1) * cfg.CELL_EDGE
                         grid_x = int((x_position - cfg.PLAYFIELD_FRAME.element.left) / cfg.CELL_EDGE)
                         grid_y = int((y_position - cfg.PLAYFIELD_FRAME.element.top) / cfg.CELL_EDGE)

                         if direction == "left" and grid_x <= 0:
                              return True
                         elif direction == "right" and grid_x >= self.rows-1:
                              return True
                         elif direction == "left" and self.board[grid_y][grid_x-1] != 0:
                              return True
                         elif direction == "right" and self.board[grid_y][grid_x+1] != 0:
                              return True
          return False
     
     def check_collision_rotation(self, value):
          # Check if there'll be collision after rotation
          new_rotation = (self.rotation + value) % len(self.tetromino)
          
          for i, string in enumerate(self.tetromino[new_rotation], start=-2):
               for j, tetromino_piece in enumerate(string, start=-2):
                    if tetromino_piece == "0":
                         x_position = (self.x + cfg.PLAYFIELD_FRAME.element.right) / 2 + (j - 1) * cfg.CELL_EDGE
                         y_position = self.y + (i + 1) * cfg.CELL_EDGE
                         grid_x = int((x_position - cfg.PLAYFIELD_FRAME.element.left) / cfg.CELL_EDGE)
                         grid_y = int((y_position - cfg.PLAYFIELD_FRAME.element.top) / cfg.CELL_EDGE)
                         
                         # Return false if the x position goes out of bounds, otherwise can't implement wall kick
                         if grid_x >= 10:
                              return False
                         # Return true if there's collision
                         if self.board[grid_y][grid_x] != 0:
                              return True
          return False
     
     def check_collision_ghost_piece(self, y):
          # Check bottom collision
          if y == cfg.PLAYFIELD_FRAME.element.bottom-cfg.CELL_EDGE:
               return True
          
          # Check tetromino collision with other blocks
          for i, string in enumerate(self.tetromino[self.rotation], start=-2):
               for j, tetromino_piece in enumerate(string, start=-2):
                    if tetromino_piece == "0":
                         x_position = int((self.x + cfg.PLAYFIELD_FRAME.element.right) / 2 + (j - 1) * cfg.CELL_EDGE)
                         y_position = y + (i + 1) * cfg.CELL_EDGE
                         grid_x = int((x_position - cfg.PLAYFIELD_FRAME.element.left) / cfg.CELL_EDGE)
                         grid_y = int((y_position - cfg.PLAYFIELD_FRAME.element.top) / cfg.CELL_EDGE)
                         
                         if grid_y + 1 >= len(self.board):
                              return True
                         
                         if self.board[grid_y+1][grid_x] != 0:
                              return True
          return False
     
     def clear_rows(self):
          rows_cleared = []
          
          # If row is a complete line, add corresponding row to the list
          for i, row in enumerate(self.board):
               if all(row):
                    rows_cleared.append(i)
          
          # Clear the corresponding rows from the board, drop rows before them by one block, recreate the first row
          for row in rows_cleared:
               for i in range(row, 0, -1):
                    self.board[i] = self.board[i - 1]
               self.board[0] = [0 for _ in range(self.rows)]
          
          # Increase score according to the amount of rows cleared in one move and the level
          if len(rows_cleared) == 1:
               self.score += 100 * (self.level + 1)
          elif len(rows_cleared) == 2:
               self.score += 300 * (self.level + 1)
          elif len(rows_cleared) == 3:
               self.score += 500 * (self.level + 1)
          elif len(rows_cleared) == 4:
               self.score += 800 * (self.level + 1)
          
          for i in range(len(rows_cleared)):
               self.lines += 1
               if self.lines % 10 == 0:
                    self.level += 1
     
     def hard_drop(self):
          # Drop tetromino until y collision
          while not self.check_collision_y():
               self.y += cfg.CELL_EDGE
               self.score += 2
          self.place_tetromino()
          
          # Reset tetromino position and get a new one
          self.x = cfg.PLAYFIELD_FRAME.element.left
          self.y = cfg.PLAYFIELD_FRAME.element.top
          self.rotation = 0
          self.tetromino = self.next_tetromino
          self.next_tetromino = self.get_tetromino()
     
     def ghost_piece(self, display_update=True):
          ghost_y = self.y
          
          while not self.check_collision_ghost_piece(ghost_y):
               ghost_y += cfg.CELL_EDGE
          
          ghost_min_x, ghost_max_x = cfg.PLAYFIELD_FRAME.element.right, cfg.PLAYFIELD_FRAME.element.left
          ghost_min_y, ghost_max_y = cfg.PLAYFIELD_FRAME.element.bottom, cfg.PLAYFIELD_FRAME.element.top
          ghost_x_positions, ghost_y_positions = [], []

          for i, string in enumerate(self.tetromino[self.rotation], start=-2):
               for j, tetromino_piece in enumerate(string, start=-2):
                    if tetromino_piece == "0":
                         x_position = (self.x + cfg.PLAYFIELD_FRAME.element.right) / 2 + (j - 1) * cfg.CELL_EDGE
                         y_position = ghost_y + (i + 1) * cfg.CELL_EDGE
                         ghost_min_x = min(ghost_min_x, x_position)
                         ghost_max_x = max(ghost_max_x, x_position + cfg.CELL_EDGE)
                         ghost_min_y = min(ghost_min_y, y_position)
                         ghost_max_y = max(ghost_max_y, y_position)
                         ghost_x_positions.append(x_position)
                         ghost_y_positions.append(y_position)
          
          # Draw ghost tetromino
          for x, y in zip(ghost_x_positions, ghost_y_positions):
               pygame.draw.rect(cfg.WINDOW, tetromino_colors[tetrominos.index(self.tetromino)], (x, y, cfg.CELL_EDGE - 1, cfg.CELL_EDGE - 1), 1)
          
          if display_update:
               pygame.display.update()
          

          
     def get_fall_delay(self, level):
          # Fall speed
          return max(50, 1100 - level * 100)
     
     
     def main_menu(self):
          global starting_level
               
          main_menu_bool = True
          # Change the level from current (key) to the desired level (value)
          starting_levels_dict = { 
               1: 3,
               3: 5,
               5: 7,
               7: 9,
               9: 11,
               11: 1
               }

          while main_menu_bool:
               self.draw_window()
               pygame.draw.rect(cfg.WINDOW, cfg.LIGHT_GREY, cfg.PLAYFIELD_FRAME.element, width=1)
               high_scores_rect = pygame.Rect(0, 0, cfg.CELL_EDGE * 6, cfg.CELL_EDGE * 6)
               high_scores_rect.center = cfg.RESOLUTION_DISPLAY["width"] // 2, cfg.RESOLUTION_DISPLAY["height"] // 2
               high_scores_text = cfg.font.render("HIGH SCORES", True, cfg.WHITE)
               high_scores_text_rect = high_scores_text.get_rect()
               high_scores_text_rect.centerx = high_scores_rect.centerx
               high_scores_text_rect.top = high_scores_rect.top + cfg.USER_CHOICE_SCALE # Small increment so the text doesn't touch the top of the rectangle
               pygame.draw.rect(cfg.WINDOW, cfg.LIGHT_GREY, high_scores_rect, width=1)
               cfg.WINDOW.blit(high_scores_text, high_scores_text_rect)
               
               for i, score in enumerate(current_scores):
                    # Drawing the initials
                    initial_to_draw = cfg.font.render(score[0], True, cfg.WHITE)
                    initial_to_draw_rect = pygame.Rect(0, 0, cfg.CELL_EDGE * 2, cfg.CELL_EDGE)
                    initial_to_draw_rect.left = high_scores_rect.left + cfg.USER_CHOICE_SCALE
                    initial_to_draw_rect.top = high_scores_rect.top + cfg.CELL_EDGE * (i + 1)
                    cfg.WINDOW.blit(initial_to_draw, initial_to_draw_rect)
                    
                    # Drawing the scores
                    score_to_draw = cfg.font.render(str(score[1]), True, cfg.WHITE)
                    score_to_draw_rect = score_to_draw.get_rect()
                    score_to_draw_rect.right = high_scores_rect.right - cfg.USER_CHOICE_SCALE
                    score_to_draw_rect.top = high_scores_rect.top + cfg.CELL_EDGE * (i + 1)
                    cfg.WINDOW.blit(score_to_draw, score_to_draw_rect)
               
               play_button = Button("PLAY", (4 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.font, (cfg.GREEN, cfg.DARK_GREEN))
               level_button = Button(f"LEVEL: {starting_level}", (4 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.font, (cfg.GREY, cfg.DARK_GREY))
               options_button = Button("OPTIONS", (4 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.font, (cfg.GREY, cfg.DARK_GREY))
               quit_button = Button("QUIT", (4 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.font, (cfg.GREY, cfg.DARK_GREY))
               
               play_button.center(cfg.RESOLUTION_DISPLAY["width"], (cfg.PLAYFIELD_FRAME.element.top + high_scores_rect.top) - cfg.CELL_EDGE * 2)
               level_button.center(cfg.RESOLUTION_DISPLAY["width"], (cfg.PLAYFIELD_FRAME.element.top + high_scores_rect.top) + cfg.CELL_EDGE * 2)
               options_button.center(cfg.RESOLUTION_DISPLAY["width"], (cfg.PLAYFIELD_FRAME.element.bottom + high_scores_rect.bottom) - cfg.CELL_EDGE * 2)
               quit_button.center(cfg.RESOLUTION_DISPLAY["width"], (cfg.PLAYFIELD_FRAME.element.bottom + high_scores_rect.bottom) + cfg.CELL_EDGE * 2)

               play_button.draw(cfg.WINDOW)
               options_button.draw(cfg.WINDOW)
               level_button.draw(cfg.WINDOW)
               quit_button.draw(cfg.WINDOW)
               
               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         pygame.quit()
                         sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                         if play_button.is_clicked(event):
                              main_menu_bool = False
                         elif options_button.is_clicked(event):
                              main_menu_bool = False
                              self.display_options_screen("main menu")
                         elif level_button.is_clicked(event):
                              starting_level = starting_levels_dict[self.level]
                              self.reset_game(starting_level)
               pygame.display.update()
     
     def display_pause_screen(self):
          pause_text = cfg.font.render("PAUSED", True, cfg.WHITE)
          pause_text_rect = pause_text.get_rect()
          pause_text_rect.top = cfg.CELL_EDGE
          pause_text_rect.centerx = cfg.PAUSE_OVERLAY.width // 2
          
          resume_button = Button("RESUME", (4 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.font, (cfg.GREEN, cfg.DARK_GREEN), cfg.PAUSE_OVERLAY.rect)
          options_button = Button("OPTIONS", (4 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.font, (cfg.LIGHT_GREY, cfg.DARK_GREY), cfg.PAUSE_OVERLAY.rect)
          quit_button = Button("QUIT", (4 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.font, (cfg.LIGHT_GREY, cfg.DARK_GREY), cfg.PAUSE_OVERLAY.rect)
          resume_button.center(cfg.PAUSE_OVERLAY.width, cfg.PAUSE_OVERLAY.height // 2)
          options_button.center(cfg.PAUSE_OVERLAY.width, cfg.PAUSE_OVERLAY.height)
          quit_button.center(cfg.PAUSE_OVERLAY.width, 3 * cfg.PAUSE_OVERLAY.height // 2)
          
          paused = True
          
          while paused:
               cfg.PAUSE_OVERLAY.draw(cfg.WINDOW)
               cfg.PAUSE_OVERLAY.element.fill(cfg.BLACK)
               pygame.draw.rect(cfg.PAUSE_OVERLAY.element, cfg.LIGHT_GREY, cfg.PAUSE_OVERLAY.element.get_rect(), 5)
               cfg.PAUSE_OVERLAY.element.blit(pause_text, pause_text_rect)
               
               resume_button.draw(cfg.PAUSE_OVERLAY.element)
               options_button.draw(cfg.PAUSE_OVERLAY.element)
               quit_button.draw(cfg.PAUSE_OVERLAY.element)
               
               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         pygame.quit()
                         sys.exit()
                    elif event.type == pygame.KEYDOWN:
                         if event.key == pygame.K_ESCAPE:
                              paused = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                         if resume_button.is_clicked(event):
                              paused = False
                         if options_button.is_clicked(event):
                              paused = False
                              self.display_options_screen("pause screen")
                         if quit_button.is_clicked(event):
                              paused = False
                              self.main_menu()
                              self.reset_game(starting_level)
               
               pygame.display.update()
     
     def display_options_screen(self, screen):
          options_text = cfg.font.render("OPTIONS", True, cfg.WHITE)
          options_text_rect = options_text.get_rect()
          options_text_rect.top = cfg.CELL_EDGE
          options_text_rect.centerx = cfg.OPTIONS_OVERLAY.width // 2
          
          key_mapping_button = Button("KEY MAPPING", (5 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.font, (cfg.GREY, cfg.DARK_GREY), cfg.OPTIONS_OVERLAY.rect)
          resolutions_button = Button("RESOLUTIONS", (5 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.font, (cfg.GREY, cfg.DARK_GREY), cfg.OPTIONS_OVERLAY.rect)
          key_mapping_button.center(cfg.OPTIONS_OVERLAY.width, 2 * cfg.OPTIONS_OVERLAY.height // 3)
          resolutions_button.center(cfg.OPTIONS_OVERLAY.width, 4 * cfg.OPTIONS_OVERLAY.height // 3)
          
          options_screen_bool = True
          
          while options_screen_bool:
               self.draw_window()
               if screen == "pause screen":
                    self.draw_gameloop()
                    self.draw_tetromino()
                    self.ghost_piece(display_update=False)

               cfg.OPTIONS_OVERLAY.draw(cfg.WINDOW)
               cfg.OPTIONS_OVERLAY.element.fill(cfg.BLACK)
               pygame.draw.rect(cfg.OPTIONS_OVERLAY.element, cfg.LIGHT_GREY, cfg.OPTIONS_OVERLAY.element.get_rect(), 5)
               cfg.OPTIONS_OVERLAY.element.blit(options_text, options_text_rect)
               key_mapping_button.draw(cfg.OPTIONS_OVERLAY.element)
               resolutions_button.draw(cfg.OPTIONS_OVERLAY.element)
               
               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         pygame.quit()
                         sys.exit()
                    elif event.type == pygame.KEYDOWN:
                         if event.key == pygame.K_ESCAPE:
                              options_screen_bool = False
                              if screen == "main menu":
                                   print("wtff")
                                   self.main_menu()
                              elif screen == "pause screen":
                                   self.display_pause_screen()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                         if key_mapping_button.is_clicked(event): 
                              self.display_key_mapping_screen(screen)
                              options_screen_bool = False
                         elif resolutions_button.is_clicked(event):
                              self.display_resolutions_screen(screen)
                              options_screen_bool = False
               pygame.display.update()
     
     def change_keybind(self, action, screen):
          changing_key = True
          
          while changing_key:
               self.draw_window()
               if screen == "pause screen":
                    self.draw_gameloop()
                    self.draw_tetromino()
                    self.ghost_piece(display_update=False)
                    
               pygame.draw.rect(cfg.WINDOW, cfg.LIGHT_GREY, cfg.PLAYFIELD_FRAME.element, width=1)
               cfg.KEYBIND_OVERLAY.draw(cfg.WINDOW)
               cfg.KEYBIND_OVERLAY.element.fill(cfg.BLACK)
               pygame.draw.rect(cfg.KEYBIND_OVERLAY.element, cfg.LIGHT_GREY, cfg.KEYBIND_OVERLAY.element.get_rect(), 5)
               
               new_key_text = cfg.font.render("PRESS A NEW KEY FOR:", True, cfg.WHITE)
               new_key_text_rect = new_key_text.get_rect()
               new_key_text_rect.top = cfg.KEYBIND_OVERLAY.height // 2 - cfg.CELL_EDGE
               new_key_text_rect.centerx = cfg.KEYBIND_OVERLAY.width // 2
               
               keybind_text = cfg.font.render(str(action).upper(), True, cfg.WHITE)
               keybind_text_rect = keybind_text.get_rect()
               keybind_text_rect.top = cfg.KEYBIND_OVERLAY.height // 2
               keybind_text_rect.centerx = cfg.KEYBIND_OVERLAY.width // 2
               
               cfg.KEYBIND_OVERLAY.element.blit(new_key_text, new_key_text_rect)
               cfg.KEYBIND_OVERLAY.element.blit(keybind_text, keybind_text_rect)
               
               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         pygame.quit()
                         sys.exit()
                    elif event.type == pygame.KEYDOWN:
                         if event.key == pygame.K_ESCAPE:
                              changing_key = False
                              self.display_key_mapping_screen(screen)
                         else:
                              current_keys[action] = event.key
                              changing_key = False
                         
                              # If keybind is the same as another action, that action will be left blank
                              for key, value in current_keys.items():
                                   if key != action and value == current_keys[action]:
                                        current_keys[key] = 0
                              
                              # Updating the options file with the new change
                              json_data = json.dumps(current_keys, indent=4)
                              with open(databases.options_file, "w") as file:
                                   file.write(json_data)
                              self.display_key_mapping_screen(screen)
               pygame.display.update()
     
     def display_reset_key_mapping_screen(self, screen):
          reset_key_mapping_bool = True
          
          while reset_key_mapping_bool:
               self.draw_window()
               if screen == "pause screen":
                    self.draw_gameloop()
                    self.draw_tetromino()
                    self.ghost_piece(display_update=False)
               
               pygame.draw.rect(cfg.WINDOW, cfg.LIGHT_GREY, cfg.PLAYFIELD_FRAME.element, width=1)
               
               reset_key_mapping_text = cfg.font.render("RESET KEY MAPPING?", True, cfg.WHITE)
               reset_key_mapping_text_rect = reset_key_mapping_text.get_rect()
               reset_key_mapping_text_rect.centerx = cfg.RESET_KEY_MAPPING_OVERLAY.width // 2
               reset_key_mapping_text_rect.top = cfg.CELL_EDGE
               cfg.RESET_KEY_MAPPING_OVERLAY.draw(cfg.WINDOW)
               cfg.RESET_KEY_MAPPING_OVERLAY.element.fill(cfg.BLACK)
               pygame.draw.rect(cfg.RESET_KEY_MAPPING_OVERLAY.element, cfg.LIGHT_GREY, cfg.RESET_KEY_MAPPING_OVERLAY.element.get_rect(), 5)
               cfg.RESET_KEY_MAPPING_OVERLAY.element.blit(reset_key_mapping_text, reset_key_mapping_text_rect)
               
               ok_button = Button("OK", (4 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.font, (cfg.LIGHT_GREY, cfg.DARK_GREY), cfg.RESET_KEY_MAPPING_OVERLAY.rect)
               cancel_button = Button("CANCEL", (4 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.font, (cfg.LIGHT_GREY, cfg.DARK_GREY), cfg.RESET_KEY_MAPPING_OVERLAY.rect)
               
               ok_button.center(cfg.RESET_KEY_MAPPING_OVERLAY.width, cfg.RESET_KEY_MAPPING_OVERLAY.height - cfg.CELL_EDGE * 2)
               cancel_button.center(cfg.RESET_KEY_MAPPING_OVERLAY.width, cfg.RESET_KEY_MAPPING_OVERLAY.height + cfg.CELL_EDGE * 2)
               
               ok_button.draw(cfg.RESET_KEY_MAPPING_OVERLAY.element)
               cancel_button.draw(cfg.RESET_KEY_MAPPING_OVERLAY.element)
               
               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         pygame.quit()
                         sys.exit()
                    elif event.type == pygame.KEYDOWN:
                         if event.key == pygame.K_ESCAPE:
                              reset_key_mapping_bool = False
                              self.display_key_mapping_screen(screen)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                         if ok_button.is_clicked(event):
                              global current_keys
                              current_keys = databases.default_keys.copy()
                              if os.path.exists(databases.options_file):
                                   os.remove(databases.options_file)
                              with open(databases.options_file, "w") as file:
                                   json.dump(current_keys, file, indent=4)
                              reset_key_mapping_bool = False
                              self.display_key_mapping_screen(screen)
                              
                         elif cancel_button.is_clicked(event):
                              reset_key_mapping_bool = False
                              self.display_key_mapping_screen(screen)
               pygame.display.update()
     
     def display_key_mapping_screen(self, screen):
          key_mapping_text = cfg.font.render("KEY MAPPING", True, cfg.WHITE)  
          key_mapping_text_rect = key_mapping_text.get_rect()
          key_mapping_text_rect.top = cfg.CELL_EDGE // 2
          key_mapping_text_rect.centerx = cfg.KEY_MAPPING_OVERLAY.width // 2
          
          key_names = [key for key in databases.keys.keys()]
          key_texts = []
          key_buttons = []
          
          for i, key in enumerate(key_names):
               key_text = cfg.font.render(key, True, cfg.WHITE)
               key_text_rect = key_text.get_rect()
               key_text_rect.top = (cfg.KEY_MAPPING_OVERLAY.height // (len(key_names) + 1) * (i + 1)) - (cfg.CELL_EDGE // 2)
               key_text_rect.left = cfg.CELL_EDGE
               key_texts.append((key_text, key_text_rect))
               
               key_button = Button(pygame.key.name(current_keys[key]).upper(), (5 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.font, (cfg.LIGHT_GREY, cfg.DARK_GREY), cfg.KEY_MAPPING_OVERLAY.rect)
               key_button.center(3 * cfg.KEY_MAPPING_OVERLAY.width // 2, 2 * ((cfg.KEY_MAPPING_OVERLAY.height // (len(key_names) + 1) * (i + 1)) - (cfg.CELL_EDGE // 2) + cfg.CELL_EDGE // 3))
               key_buttons.append(key_button)
          
          reset_to_defaults_button = Button("RESET TO DEFAULTS", (8 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.font, (cfg.GREY, cfg.DARK_GREY), cfg.KEY_MAPPING_OVERLAY.rect)
          reset_to_defaults_button.center(cfg.KEY_MAPPING_OVERLAY.width, (cfg.KEY_MAPPING_OVERLAY.height - cfg.CELL_EDGE) * 2)

          waiting_for_input = True
          
          while waiting_for_input:
               cfg.KEY_MAPPING_OVERLAY.draw(cfg.WINDOW)
               cfg.KEY_MAPPING_OVERLAY.element.fill(cfg.BLACK)
               pygame.draw.rect(cfg.KEY_MAPPING_OVERLAY.element, cfg.LIGHT_GREY, cfg.KEY_MAPPING_OVERLAY.element.get_rect(), 5)
               cfg.KEY_MAPPING_OVERLAY.element.blit(key_mapping_text, key_mapping_text_rect)
               
               for key_text, key_text_rect in key_texts:
                    cfg.KEY_MAPPING_OVERLAY.element.blit(key_text, key_text_rect)
               for key_button in key_buttons:
                    key_button.draw(cfg.KEY_MAPPING_OVERLAY.element)
               reset_to_defaults_button.draw(cfg.KEY_MAPPING_OVERLAY.element)
               
               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         pygame.quit()
                         sys.exit()
                    elif event.type == pygame.KEYDOWN:
                         if event.key == pygame.K_ESCAPE:
                              waiting_for_input = False
                              self.display_options_screen(screen)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                         for i, key_button in enumerate(key_buttons):
                              if key_button.is_clicked(event):
                                   waiting_for_input = False
                                   self.change_keybind(key_names[i], screen)
                         if reset_to_defaults_button.is_clicked(event):
                              waiting_for_input = False
                              self.display_reset_key_mapping_screen(screen)
      
               pygame.display.update()
     
     def display_resolutions_screen(self, screen):
          resolutions_text = cfg.font.render("RESOLUTIONS", True, cfg.WHITE)
          resolutions_text_rect = resolutions_text.get_rect()
          resolutions_text_rect.top = cfg.CELL_EDGE // 2
          resolutions_text_rect.centerx = cfg.RESOLUTIONS_OVERLAY.width // 2
          
          resolutions_list = [(cfg.BASE_WIDTH * i, cfg.BASE_HEIGHT * i) for i in cfg.RESOLUTION_SCALING_MULTIPLIERS]
          resolution_buttons_list = []
          
          for i, (width, height) in enumerate(resolutions_list):
               resolution_button = Button(f"{width}x{height}", (5 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.font, (cfg.LIGHT_GREY, cfg.DARK_GREY), cfg.RESOLUTIONS_OVERLAY.rect)
               resolution_button.center(cfg.RESOLUTIONS_OVERLAY.width, 2 * ((cfg.RESOLUTIONS_OVERLAY.height // (len(resolutions_list) + 1) * (i + 1) + (cfg.CELL_EDGE // 2))))
               resolution_buttons_list.append(resolution_button)
          
          resolutions_screen_bool = True
          while resolutions_screen_bool:
               self.draw_window()
               if screen == "pause screen":
                    self.draw_gameloop()
                    self.draw_tetromino()
                    self.ghost_piece(display_update=False)
               cfg.RESOLUTIONS_OVERLAY.draw(cfg.WINDOW)
               cfg.RESOLUTIONS_OVERLAY.element.fill(cfg.BLACK)
               pygame.draw.rect(cfg.RESOLUTIONS_OVERLAY.element, cfg.LIGHT_GREY, cfg.RESOLUTIONS_OVERLAY.element.get_rect(), 5)
               cfg.RESOLUTIONS_OVERLAY.element.blit(resolutions_text, resolutions_text_rect)
               for resolution in resolution_buttons_list:
                    resolution.draw(cfg.RESOLUTIONS_OVERLAY.element)
               
               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         pygame.quit()
                         sys.exit()
                    elif event.type == pygame.KEYDOWN:
                         if event.key == pygame.K_ESCAPE:
                              resolutions_screen_bool = False
                              self.display_options_screen(screen)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                         for i, resolution in enumerate(resolution_buttons_list):
                              if resolution.is_clicked(event):
                                   resolutions_screen_bool = False
                                   self.display_keep_changes_screen(i, screen)
               
               pygame.display.update()
     
     def display_keep_changes_screen(self, index, screen):
          # TODO: ADD SUPPORT FOR CHANGING RESOLUTION MID-GAME
          #current_left, current_top
          cfg.update_resolution(index)
          if check_if_background_image_exists:
               global BACKGROUND
               BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (cfg.RESOLUTION_DISPLAY["width"], cfg.RESOLUTION_DISPLAY["height"]))
               cfg.WINDOW.blit(BACKGROUND, (0, 0))

          for overlay in cfg.OVERLAYS:
               overlay.update(cfg.CELL_EDGE)
          
          for frame in cfg.FRAMES:
               frame.update(cfg.CELL_EDGE)

          keep_changes_bool = True
          while keep_changes_bool:
               self.draw_window()
               if screen == "pause screen":
                    self.draw_gameloop()
                    self.draw_tetromino()
                    self.ghost_piece(display_update=False)
               
               cfg.KEEP_CHANGES_OVERLAY.draw(cfg.WINDOW)
               cfg.KEEP_CHANGES_OVERLAY.element.fill(cfg.BLACK)
               pygame.draw.rect(cfg.KEEP_CHANGES_OVERLAY.element, cfg.LIGHT_GREY, cfg.KEEP_CHANGES_OVERLAY.element.get_rect(), 5)
               
               
               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         pygame.quit()
                         sys.exit()
                    elif event.type == pygame.KEYDOWN:
                         if event.key == pygame.K_ESCAPE:
                              keep_changes_bool = False
                              self.display_resolutions_screen(screen)
               pygame.display.update()
     
     def draw_text(self, text, font, color, surface):
          textobj = font.render(text, True, color)
          textrect = textobj.get_rect()
          textrect.center = (cfg.GAME_OVER_OVERLAY.width // 2, 90)
          surface.element.blit(textobj, textrect)
     
     def game_over_screen(self):
          global current_scores
          game_over_bool = True
          score_values = [databases.scores[i][1] for i in range(len(current_scores))]
          lowest_score = min(score_values)
          
          # Variables used when there is no new score
          game_over_text = cfg.font.render("GAME OVER", True, cfg.WHITE)
          high_scores_text = cfg.font.render("HIGH SCORES", True, cfg.WHITE)
          
          main_menu_button = Button("MAIN MENU", (4 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.font, (cfg.LIGHT_GREY, cfg.DARK_GREY))
          play_again_button = Button("PLAY AGAIN", (4 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.font, (cfg.GREEN, cfg.DARK_GREEN))
          
          main_menu_button.center(cfg.RESOLUTION_DISPLAY["width"], cfg.RESOLUTION_DISPLAY["height"] + 5 * cfg.CELL_EDGE)
          play_again_button.center(cfg.RESOLUTION_DISPLAY["width"], cfg.RESOLUTION_DISPLAY["height"] + 9 * cfg.CELL_EDGE)
               
          game_over_text_rect = game_over_text.get_rect(center=(cfg.GAME_OVER_OVERLAY.width // 2, 15))
          high_scores_text_rect = high_scores_text.get_rect(center=(cfg.GAME_OVER_OVERLAY.width // 2, 40))
          
          # Variables used when there is new score
          user_input = ""
          max_initials_length = 3
          
          new_high_score_text = cfg.font.render("NEW HIGH SCORE!", True, cfg.WHITE)
          enter_initials_text = cfg.font.render("ENTER YOUR INITIALS:", True, cfg.WHITE)
          
          ok_button = Button("OK", (2 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.font, (cfg.LIGHT_GREY, cfg.DARK_GREY))
          ok_button.center(cfg.RESOLUTION_DISPLAY["width"], cfg.RESOLUTION_DISPLAY["height"] + 5 * cfg.CELL_EDGE)
          
          new_high_score_text_rect = new_high_score_text.get_rect(center=(cfg.GAME_OVER_OVERLAY.width // 2, 15))
          enter_initials_text_rect = enter_initials_text.get_rect(center=(cfg.GAME_OVER_OVERLAY.width // 2, 65))
          
               
          if self.score >= lowest_score:
               new_score = self.score
               score_number_text = cfg.font.render(str(new_score), True, cfg.WHITE)
               score_number_text_rect = score_number_text.get_rect(center=(cfg.GAME_OVER_OVERLAY.width // 2, 40))
          else:
               new_score = False
          
          while game_over_bool:
               cfg.GAME_OVER_OVERLAY.draw(cfg.WINDOW)
               cfg.GAME_OVER_OVERLAY.element.fill(cfg.BLACK)
               pygame.draw.rect(cfg.GAME_OVER_OVERLAY.element, cfg.LIGHT_GREY, cfg.GAME_OVER_OVERLAY.element.get_rect(), 5)
               if not new_score:
                    high_scores_rect = pygame.Rect(60, 30, 120, 120)
                    pygame.draw.rect(cfg.GAME_OVER_OVERLAY.element, cfg.LIGHT_GREY, high_scores_rect, width=1)
                    
                    
                    cfg.GAME_OVER_OVERLAY.element.blit(game_over_text, game_over_text_rect)
                    cfg.GAME_OVER_OVERLAY.element.blit(high_scores_text, high_scores_text_rect)
                    for i, score in enumerate(current_scores):
                         # Drawing the initials
                         initial_to_draw = cfg.font.render(score[0], True, cfg.WHITE)
                         initial_to_draw_rect = pygame.Rect(high_scores_rect.left + 5, 50 + i * cfg.CELL_EDGE, 4 * cfg.CELL_EDGE, cfg.CELL_EDGE)
                         cfg.GAME_OVER_OVERLAY.element.blit(initial_to_draw, initial_to_draw_rect)
                         
                         # Drawing the scores
                         score_to_draw = cfg.font.render(str(score[1]), True, cfg.WHITE)
                         score_to_draw_rect = pygame.Rect(high_scores_rect.right - score_to_draw.get_width() - 5, 50 + i * cfg.CELL_EDGE, 4 * cfg.CELL_EDGE, cfg.CELL_EDGE)
                         cfg.GAME_OVER_OVERLAY.element.blit(score_to_draw, score_to_draw_rect)
                         
                         # Drawing the buttons
                         main_menu_button.draw(cfg.WINDOW)
                         play_again_button.draw(cfg.WINDOW)
               else:
                    cfg.GAME_OVER_OVERLAY.element.blit(new_high_score_text, new_high_score_text_rect)
                    cfg.GAME_OVER_OVERLAY.element.blit(score_number_text, score_number_text_rect)
                    cfg.GAME_OVER_OVERLAY.element.blit(enter_initials_text, enter_initials_text_rect)
                    self.draw_text(f"{user_input}", cfg.font, cfg.WHITE, cfg.GAME_OVER_OVERLAY)
                    ok_button.draw(cfg.WINDOW)
                    
               
               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         pygame.quit()
                         sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                         if new_score:
                              if ok_button.is_clicked(event):
                                   # Save initial and score
                                   databases.scores.append([user_input, new_score])
                                   databases.scores.sort(key=lambda x: x[1], reverse=True)
                                   current_scores = databases.scores[:5]
                                   with open(databases.score_file, 'w') as file:
                                        json.dump(current_scores, file, indent=4)
                                   new_score = False
                         else:
                              if main_menu_button.is_clicked(event):
                                   game_over_bool = False
                                   self.main_menu()
                              elif play_again_button.is_clicked(event):
                                   game_over_bool = False
                              self.reset_game(starting_level)
                    elif event.type == pygame.KEYDOWN:
                         if new_score:
                              if event.key == pygame.K_RETURN:
                                   # Save initial and score
                                   databases.scores.append([user_input, new_score])
                                   databases.scores.sort(key=lambda x: x[1], reverse=True)
                                   current_scores = databases.scores[:5]
                                   with open(databases.score_file, 'w') as file:
                                        json.dump(current_scores, file, indent=4)
                                   new_score = False
                              elif event.key == pygame.K_SPACE:
                                   pass
                              elif event.key == pygame.K_BACKSPACE:
                                   user_input = user_input[:-1]
                              elif len(user_input) < max_initials_length:
                                   user_input += event.unicode.upper()
                                   
                                   
               pygame.display.update()
                                   
     def main(self):
          clock = pygame.time.Clock()
          running = True
          movement_left = False
          movement_right = False
          movement_bottom = False
          initial_move_delay = 100  # Initial delay before repeating movement
          move_fast_delay = 50  # Faster delay for continuous movement
          last_move_time = pygame.time.get_ticks()
          last_fall_time = pygame.time.get_ticks()
          holdable = True
          self.main_menu()
          
          while running:
               clock.tick(60)
               current_time = pygame.time.get_ticks()
               fall_delay = self.get_fall_delay(self.level)
               
               # Game end
               if self.board[0][4] != 0 or self.board[0][5] != 0:
                    self.game_over_screen()
               
               # Tetromino fall
               if current_time - last_fall_time > fall_delay:
                    self.y += cfg.CELL_EDGE
                    last_fall_time = current_time
               
               # Continuous movement
               if movement_left and not self.check_collision_x("left"):
                    if current_time - last_move_time > move_fast_delay:
                         self.x -= 2 * cfg.CELL_EDGE
                         last_move_time = current_time
               if movement_right and not self.check_collision_x("right"):
                    if current_time - last_move_time > move_fast_delay:
                         self.x += 2 * cfg.CELL_EDGE
                         last_move_time = current_time
               if movement_bottom and not self.check_collision_y():
                    if current_time - last_move_time > move_fast_delay:
                         self.y += cfg.CELL_EDGE
                         self.score += 1
                         last_move_time = current_time

               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         running = False
                    
                    elif event.type == pygame.KEYDOWN:
                         # Pause
                         if event.key == pygame.K_ESCAPE:
                              self.display_pause_screen()
                         
                         # Rotate right
                         elif event.key == current_keys["ROTATE RIGHT"] and not self.check_collision_rotation(1):
                              self.rotation += 1
                              if self.rotation == len(self.tetromino):
                                   self.rotation = 0
                         
                         # Rotate left
                         elif event.key == current_keys["ROTATE LEFT"] and not self.check_collision_rotation(-1):
                              if self.rotation == 0:
                                   self.rotation = len(self.tetromino)
                              self.rotation -= 1
                         
                         # Hard drop
                         elif event.key == current_keys["HARD DROP"]:
                              self.hard_drop()
                              holdable = True
                         
                         # Hold 
                         elif event.key == current_keys["HOLD"]:
                              if holdable:
                                   if len(self.hold_tetromino) == 1 and self.hold_tetromino != cfg.O:
                                        self.hold_tetromino = self.tetromino
                                        self.x = cfg.PLAYFIELD_FRAME.element.left
                                        self.y = cfg.PLAYFIELD_FRAME.element.top
                                        self.rotation = 0
                                        self.tetromino = self.next_tetromino
                                        self.next_tetromino = self.get_tetromino()
                                        holdable = False
                                   else:
                                        placeholder = self.hold_tetromino
                                        self.hold_tetromino = self.tetromino
                                        self.tetromino = placeholder
                                        self.x = cfg.PLAYFIELD_FRAME.element.left
                                        self.y = cfg.PLAYFIELD_FRAME.element.top
                                        self.rotation = 0
                                        holdable = False
                         
                         # Soft drop
                         elif event.key == current_keys["SOFT DROP"] and not self.check_collision_y():
                              self.y += cfg.CELL_EDGE
                              movement_bottom = True
                              self.score += 1
                              last_move_time = current_time + initial_move_delay  # Adding initial delay for the first move
                         
                         # Left
                         elif event.key == current_keys["MOVE LEFT"]:
                              movement_left = True
                              if not self.check_collision_x("left"):
                                   self.x -= 2 * cfg.CELL_EDGE
                              last_move_time = current_time + initial_move_delay  # Adding initial delay for the first move
                         
                         # Right
                         elif event.key == current_keys["MOVE RIGHT"]:
                              movement_right = True
                              if not self.check_collision_x("right"):
                                   self.x += 2 * cfg.CELL_EDGE
                              last_move_time = current_time + initial_move_delay  # Adding initial delay for the first move
                    
                    # Stop continuous movement if buttons aren't being pressed
                    elif event.type == pygame.KEYUP:
                         if event.key == current_keys["MOVE LEFT"]:
                              movement_left = False
                         elif event.key == current_keys["MOVE RIGHT"]:
                              movement_right = False
                         elif event.key == current_keys["SOFT DROP"]:
                              movement_bottom = False           
               
               # Update and draw
               self.clear_rows()
               self.draw_window()
               self.draw_gameloop()
               self.draw_tetromino()
               self.ghost_piece()
               
               # Place tetromino if tetromino reached the bottom or if there's a collision with another tetromino in the y axis
               if self.check_collision_y():
                    self.place_tetromino()
                    holdable = True

                    # Reset tetromino position and get a new one
                    self.x = cfg.PLAYFIELD_FRAME.element.left
                    self.y = cfg.PLAYFIELD_FRAME.element.top
                    self.rotation = 0
                    self.tetromino = self.next_tetromino
                    self.next_tetromino = self.get_tetromino()
                    last_fall_time = pygame.time.get_ticks()  # Reset fall time to avoid instant fall of new tetromino

          pygame.quit()



tetris = Tetris()

if __name__ == "__main__":
     tetris.main()
