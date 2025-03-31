import pygame
import random
import os
import sys
import json

from button import Button
import databases as db
import config as cfg

# Full path of your background image file (optional)
# Supported formats: png, jpeg, bmp, tga, gif (non-animated), ppm, xpm
background_image_file = r"YOUR_BACKGROUND_IMAGE_FILE.png"  # Change this to your image file name, png is recommended

check_if_background_image_exists = os.path.exists(background_image_file)

if check_if_background_image_exists:
     BACKGROUND_IMAGE = pygame.image.load(os.path.join(db.script_dir, background_image_file))
     BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (cfg.RESOLUTION_DISPLAY["width"], cfg.RESOLUTION_DISPLAY["height"]))

tetrominos = [cfg.I, cfg.J, cfg.L, cfg.O, cfg.S, cfg.T, cfg.Z]
tetromino_colors = [cfg.LIGHT_BLUE, cfg.DARK_BLUE,cfg.ORANGE, cfg.YELLOW, cfg.GREEN, cfg.PURPLE, cfg.RED]
starting_level = 1

class Tetris:
     def __init__(self):
          self.options = db.options
          self.current_keys = self.options["keys"]
          self.current_scores = db.scores
          self.reset_game()

     def reset_game(self, level=1):
          self.grid_x = 2
          self.grid_y = -1
          self.rows = cfg.PLAYFIELD_FRAME.num_cells_width
          self.columns = cfg.PLAYFIELD_FRAME.num_cells_height
          self.rotation = 0
          self.bag = tetrominos.copy()
          self.tetromino = self.get_tetromino()
          self.next_tetromino = self.get_tetromino()
          self.hold_tetromino = None
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
     
     def draw_frames(self):
          cfg.WINDOW.fill(cfg.BLACK)
          if check_if_background_image_exists:
               cfg.WINDOW.blit(BACKGROUND, (0, 0))
          pygame.draw.rect(cfg.WINDOW, cfg.BLACK, cfg.PLAYFIELD_FRAME.element)
          pygame.draw.rect(cfg.WINDOW, cfg.BLACK, cfg.NEXT_FRAME.element)
          pygame.draw.rect(cfg.WINDOW, cfg.BLACK, cfg.HOLD_FRAME.element)
          pygame.draw.rect(cfg.WINDOW, cfg.BLACK, cfg.SCORE_FRAME.element)
          
          # Draw next tetromino frame
          pygame.draw.rect(cfg.WINDOW, cfg.LIGHT_GREY, cfg.NEXT_FRAME.element, width=1)
          next_text = cfg.FONT.render("NEXT", True, cfg.WHITE)
          next_rect = next_text.get_rect()
          next_rect.centerx = cfg.NEXT_FRAME.element.centerx
          next_rect.y = cfg.NEXT_FRAME.element.y + cfg.CELL_EDGE # Small increment so the text isn't directly on the border of the rectangle
          cfg.WINDOW.blit(next_text, next_rect)
          
          # Draw hold frame
          pygame.draw.rect(cfg.WINDOW, cfg.LIGHT_GREY, cfg.HOLD_FRAME.element, width=1)
          hold_text = cfg.FONT.render("HOLD", True, cfg.WHITE)
          hold_rect = hold_text.get_rect()
          hold_rect.centerx = cfg.HOLD_FRAME.element.centerx
          hold_rect.y = cfg.HOLD_FRAME.element.y + cfg.CELL_EDGE
          cfg.WINDOW.blit(hold_text, hold_rect)
          
          # Draw score frame
          pygame.draw.rect(cfg.WINDOW, cfg.LIGHT_GREY, cfg.SCORE_FRAME.element, width=1)
          score_text = cfg.FONT.render("SCORE", True, cfg.WHITE)
          level_text = cfg.FONT.render("LEVEL", True, cfg.WHITE)
          lines_text = cfg.FONT.render("LINES", True, cfg.WHITE)
          
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
     
     def draw_next_hold_screens(self, frame):
          frame_center_x = frame.element.centerx
          frame_center_y = frame.element.centery
          
          if frame == cfg.NEXT_FRAME:
               tetromino = self.next_tetromino
          elif frame == cfg.HOLD_FRAME:
               tetromino = self.hold_tetromino
          if not tetromino:
               return

          # Find height (count of rows with at least one '0')
          tetromino_height = sum(1 for row in tetromino[0] if "0" in row) * cfg.CELL_EDGE

          # Find width (difference between leftmost and rightmost '0')
          leftmost = min((row.find("0") for row in tetromino[0] if "0" in row), default=0)
          rightmost = max((row.rfind("0") for row in tetromino[0] if "0" in row), default=0)
          tetromino_width = (rightmost - leftmost + 1) * cfg.CELL_EDGE
          
          # Adjust position so the tetromino is centered inside the frame
          start_x = frame_center_x - tetromino_width // 2
          start_y = frame_center_y - tetromino_height // 2
          
          if len(tetromino) == 1:
               correction_x = 2
          else:
               correction_x = 1
          correction_y = 1

          # Draw the tetromino
          for i, row in enumerate(tetromino[0]):
               for j, block in enumerate(row):
                    if block == "0":
                         x = start_x + (j - correction_x) * cfg.CELL_EDGE
                         y = start_y + (i - correction_y) * cfg.CELL_EDGE
                         pygame.draw.rect(cfg.WINDOW, tetromino_colors[tetrominos.index(tetromino)],
                                        (x, y, cfg.CELL_EDGE - 1, cfg.CELL_EDGE - 1))
     
     def draw_playframe_lines(self):
          # Draw lines in the play screen
          line_x = cfg.PLAYFIELD_FRAME.element.left
          line_y = cfg.PLAYFIELD_FRAME.element.top
          
          for _ in range(self.rows + 1):
               pygame.draw.line(cfg.WINDOW, cfg.GREY, (line_x, line_y), (line_x, cfg.PLAYFIELD_FRAME.element.bottom))
               for _ in range(self.columns + 1):
                    pygame.draw.line(cfg.WINDOW, cfg.GREY, (line_x, line_y), (cfg.PLAYFIELD_FRAME.element.right, line_y))
                    line_y += cfg.CELL_EDGE
               line_x += cfg.CELL_EDGE
               
               line_y = cfg.PLAYFIELD_FRAME.element.top
          line_x = cfg.PLAYFIELD_FRAME.element.left
     
     def draw_placed_tetrominos(self):
          # Draw placed tetrominos
          for y, row in enumerate(self.board):
               for x, val in enumerate(row):
                    if val != 0:
                         pygame.draw.rect(cfg.WINDOW, tetromino_colors[val - 1], (cfg.PLAYFIELD_FRAME.element.left + (x * cfg.CELL_EDGE), cfg.PLAYFIELD_FRAME.element.top + (y * cfg.CELL_EDGE), cfg.CELL_EDGE - 1, cfg.CELL_EDGE - 1))
     
     def draw_score_screen(self):
          # Draw corresponding numbers in score screen
          score_number = cfg.FONT.render(str(self.score), True, cfg.WHITE)
          level_number = cfg.FONT.render(str(self.level), True, cfg.WHITE)
          lines_number = cfg.FONT.render(str(self.lines), True, cfg.WHITE)
          
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

          for i, string in enumerate(self.tetromino[self.rotation]):
               for j, tetromino_piece in enumerate(string):
                    if tetromino_piece == "0":
                         # Convert grid coordinates to pixel coordinates
                         x_position = cfg.PLAYFIELD_FRAME.element.left + (self.grid_x + j) * cfg.CELL_EDGE
                         y_position = cfg.PLAYFIELD_FRAME.element.top + (self.grid_y + i) * cfg.CELL_EDGE

                         min_x = min(min_x, x_position)
                         max_x = max(max_x, x_position + cfg.CELL_EDGE)
                         min_y = min(min_y, y_position)
                         max_y = max(max_y, y_position)

                         x_positions.append(x_position)
                         y_positions.append(y_position)
          
          # Implementing wall kick
          while min(x_positions) < cfg.PLAYFIELD_FRAME.element.left:
               self.grid_x += 1
               x_positions = [x + cfg.CELL_EDGE for x in x_positions]
          while max(x_positions) >= cfg.PLAYFIELD_FRAME.element.right:
               self.grid_x -= 1
               x_positions = [x - cfg.CELL_EDGE for x in x_positions]

          # Draw tetromino
          for x, y in zip(x_positions, y_positions):
               pygame.draw.rect(cfg.WINDOW, tetromino_colors[tetrominos.index(self.tetromino)], 
                                   (x, y, cfg.CELL_EDGE - 1, cfg.CELL_EDGE - 1))
     
     def draw_ghost_piece(self, display_update=True):
          ghost_y = self.get_ghost_position()
          
          for i, row in enumerate(self.tetromino[self.rotation]):
               for j, block in enumerate(row):
                    if block == "0":
                         x = cfg.PLAYFIELD_FRAME.element.left + (self.grid_x + j) * cfg.CELL_EDGE
                         y = cfg.PLAYFIELD_FRAME.element.top + (ghost_y + i) * cfg.CELL_EDGE
                         pygame.draw.rect(cfg.WINDOW, tetromino_colors[tetrominos.index(self.tetromino)], (x, y, cfg.CELL_EDGE - 1, cfg.CELL_EDGE - 1), 1)

          if display_update:
               pygame.display.update()
     
     def draw_gameloop(self):
          self.draw_next_hold_screens(cfg.NEXT_FRAME)
          self.draw_next_hold_screens(cfg.HOLD_FRAME)
          self.draw_playframe_lines()
          self.draw_placed_tetrominos()
          self.draw_score_screen()
          self.draw_tetromino()
          self.draw_ghost_piece(display_update=False)

     def place_tetromino(self):
          for i, row in enumerate(self.tetromino[self.rotation]):
               for j, block in enumerate(row):
                    if block == "0":
                         grid_x = self.grid_x + j
                         grid_y = self.grid_y + i
                         
                         # Place tetromino on the board
                         self.board[grid_y][grid_x] = tetrominos.index(self.tetromino) + 1
          
     def check_collision(self, dx=0, dy=0, grid_y=None, rotation=None):
          if self.tetromino == cfg.O:
               rotation = 0
          else:
               rotation = rotation if rotation is not None else self.rotation

          for i, row in enumerate(self.tetromino[rotation]):
               for j, block in enumerate(row):
                    if block == "0":
                         new_x = self.grid_x + j + dx
                         if grid_y:
                              new_y = grid_y + i + dy
                         else:
                              new_y = self.grid_y + i + dy
                         
                         # Check boundaries
                         if new_x < 0 or new_x >= cfg.PLAYFIELD_FRAME.num_cells_width:
                              return True  # Collision with left/right walls
                         if new_y >= cfg.PLAYFIELD_FRAME.num_cells_height:
                              return True  # Collision with the floor
                         
                         # Check if cell is occupied
                         if self.board[new_y][new_x]:  
                              return True  # Collision with another block
                         
          return False  # No collision

     def get_ghost_position(self):
          ghost_y = self.grid_y
          
          while not self.check_collision(dy=1, grid_y=ghost_y):
               ghost_y += 1
          
          return ghost_y

     
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
          while not self.check_collision(dy=1):
               self.grid_y += 1
               self.score += 2
          self.place_tetromino()
          
          # TODO: CONFIRM IF THIS WORKS
          pygame.time.delay(10) # Added a small delay to remove any accidental inputs like 2 tetrominos hard dropping at the same time (i don't know if this actually works, might need to change later)
          
          # Reset tetromino position and get a new one
          self.grid_x = 2
          self.grid_y = -1
          self.rotation = 0
          self.tetromino = self.next_tetromino
          self.next_tetromino = self.get_tetromino()
          
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
          
          high_scores_rect = pygame.Rect(0, 0, cfg.CELL_EDGE * 6, cfg.CELL_EDGE * 6)
          high_scores_rect.center = cfg.RESOLUTION_DISPLAY["width"] // 2, cfg.RESOLUTION_DISPLAY["height"] // 2
          high_scores_text = cfg.FONT.render("HIGH SCORES", True, cfg.WHITE)
          high_scores_text_rect = high_scores_text.get_rect()
          high_scores_text_rect.centerx = high_scores_rect.centerx
          high_scores_text_rect.top = high_scores_rect.top + cfg.USER_CHOICE_SCALE # Small increment so the text doesn't touch the top of the rectangle

          while main_menu_bool:
               self.draw_frames()
               pygame.draw.rect(cfg.WINDOW, cfg.LIGHT_GREY, cfg.PLAYFIELD_FRAME.element, width=1)
               pygame.draw.rect(cfg.WINDOW, cfg.LIGHT_GREY, high_scores_rect, width=1)
               cfg.WINDOW.blit(high_scores_text, high_scores_text_rect)
               
               for i, score in enumerate(self.current_scores):
                    # Drawing the initials
                    initial_to_draw = cfg.FONT.render(score[0], True, cfg.WHITE)
                    initial_to_draw_rect = pygame.Rect(0, 0, cfg.CELL_EDGE * 2, cfg.CELL_EDGE)
                    initial_to_draw_rect.left = high_scores_rect.left + cfg.USER_CHOICE_SCALE
                    initial_to_draw_rect.top = high_scores_rect.top + cfg.CELL_EDGE * (i + 1)
                    cfg.WINDOW.blit(initial_to_draw, initial_to_draw_rect)
                    
                    # Drawing the scores
                    score_to_draw = cfg.FONT.render(str(score[1]), True, cfg.WHITE)
                    score_to_draw_rect = score_to_draw.get_rect()
                    score_to_draw_rect.right = high_scores_rect.right - cfg.USER_CHOICE_SCALE
                    score_to_draw_rect.top = high_scores_rect.top + cfg.CELL_EDGE * (i + 1)
                    cfg.WINDOW.blit(score_to_draw, score_to_draw_rect)
               
               play_button = Button("PLAY", (4 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.FONT, (cfg.GREEN, cfg.DARK_GREEN))
               level_button = Button(f"LEVEL: {starting_level}", (4 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.FONT, (cfg.GREY, cfg.DARK_GREY))
               options_button = Button("OPTIONS", (4 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.FONT, (cfg.GREY, cfg.DARK_GREY))
               quit_button = Button("QUIT", (4 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.FONT, (cfg.GREY, cfg.DARK_GREY))
               
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
                         elif quit_button.is_clicked(event):
                              pygame.quit()
                              sys.exit()
                    elif event.type == pygame.KEYDOWN:
                         if event.key == pygame.K_ESCAPE:
                              pygame.quit()
                              sys.exit()
               pygame.display.update()
     
     def display_pause_screen(self):
          pause_text = cfg.FONT.render("PAUSED", True, cfg.WHITE)
          pause_text_rect = pause_text.get_rect()
          pause_text_rect.top = cfg.CELL_EDGE
          pause_text_rect.centerx = cfg.PAUSE_OVERLAY.width // 2
          
          resume_button = Button("RESUME", (4 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.FONT, (cfg.GREEN, cfg.DARK_GREEN), cfg.PAUSE_OVERLAY.rect)
          options_button = Button("OPTIONS", (4 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.FONT, (cfg.LIGHT_GREY, cfg.DARK_GREY), cfg.PAUSE_OVERLAY.rect)
          quit_button = Button("QUIT", (4 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.FONT, (cfg.LIGHT_GREY, cfg.DARK_GREY), cfg.PAUSE_OVERLAY.rect)
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
          options_text = cfg.FONT.render("OPTIONS", True, cfg.WHITE)
          options_text_rect = options_text.get_rect()
          options_text_rect.top = cfg.CELL_EDGE
          options_text_rect.centerx = cfg.OPTIONS_OVERLAY.width // 2
          
          key_mapping_button = Button("KEY MAPPING", (5 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.FONT, (cfg.GREY, cfg.DARK_GREY), cfg.OPTIONS_OVERLAY.rect)
          resolutions_button = Button("RESOLUTIONS", (5 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.FONT, (cfg.GREY, cfg.DARK_GREY), cfg.OPTIONS_OVERLAY.rect)
          key_mapping_button.center(cfg.OPTIONS_OVERLAY.width, 2 * cfg.OPTIONS_OVERLAY.height // 3)
          resolutions_button.center(cfg.OPTIONS_OVERLAY.width, 4 * cfg.OPTIONS_OVERLAY.height // 3)
          
          options_screen_bool = True
          
          while options_screen_bool:
               self.draw_frames()
               if screen == "pause screen":
                    self.draw_gameloop()

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
               self.draw_frames()
               if screen == "pause screen":
                    self.draw_gameloop()
                    
               pygame.draw.rect(cfg.WINDOW, cfg.LIGHT_GREY, cfg.PLAYFIELD_FRAME.element, width=1)
               cfg.KEYBIND_OVERLAY.draw(cfg.WINDOW)
               cfg.KEYBIND_OVERLAY.element.fill(cfg.BLACK)
               pygame.draw.rect(cfg.KEYBIND_OVERLAY.element, cfg.LIGHT_GREY, cfg.KEYBIND_OVERLAY.element.get_rect(), 5)
               
               new_key_text = cfg.FONT.render("PRESS A NEW KEY FOR:", True, cfg.WHITE)
               new_key_text_rect = new_key_text.get_rect()
               new_key_text_rect.top = cfg.KEYBIND_OVERLAY.height // 2 - cfg.CELL_EDGE
               new_key_text_rect.centerx = cfg.KEYBIND_OVERLAY.width // 2
               
               keybind_text = cfg.FONT.render(str(action).upper(), True, cfg.WHITE)
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
                              self.options["keys"][action] = event.key
                              changing_key = False
                         
                              # If keybind is the same as another action, that action will be left blank
                              for key, value in self.options["keys"].items():
                                   if key != action and value == self.options["keys"][action]:
                                        self.options["keys"][key] = 0
                              self.current_keys = self.options["keys"]
                              
                              # Updating the options file with the new change
                              with open(db.options_file, "w") as file:
                                   json.dump(self.options, file, indent=4)
                              self.display_key_mapping_screen(screen)
               pygame.display.update()
     
     def display_reset_key_mapping_screen(self, screen):
          reset_key_mapping_bool = True
          
          while reset_key_mapping_bool:
               self.draw_frames()
               if screen == "pause screen":
                    self.draw_gameloop()
               
               pygame.draw.rect(cfg.WINDOW, cfg.LIGHT_GREY, cfg.PLAYFIELD_FRAME.element, width=1)
               
               reset_key_mapping_text = cfg.FONT.render("RESET KEY MAPPING?", True, cfg.WHITE)
               reset_key_mapping_text_rect = reset_key_mapping_text.get_rect()
               reset_key_mapping_text_rect.centerx = cfg.RESET_KEY_MAPPING_OVERLAY.width // 2
               reset_key_mapping_text_rect.top = cfg.CELL_EDGE
               cfg.RESET_KEY_MAPPING_OVERLAY.draw(cfg.WINDOW)
               cfg.RESET_KEY_MAPPING_OVERLAY.element.fill(cfg.BLACK)
               pygame.draw.rect(cfg.RESET_KEY_MAPPING_OVERLAY.element, cfg.LIGHT_GREY, cfg.RESET_KEY_MAPPING_OVERLAY.element.get_rect(), 5)
               cfg.RESET_KEY_MAPPING_OVERLAY.element.blit(reset_key_mapping_text, reset_key_mapping_text_rect)
               
               ok_button = Button("OK", (4 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.FONT, (cfg.LIGHT_GREY, cfg.DARK_GREY), cfg.RESET_KEY_MAPPING_OVERLAY.rect)
               cancel_button = Button("CANCEL", (4 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.FONT, (cfg.LIGHT_GREY, cfg.DARK_GREY), cfg.RESET_KEY_MAPPING_OVERLAY.rect)
               
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
                              self.options["keys"] = db.default_options["keys"]
                              self.current_keys = self.options["keys"]
                              with open(db.options_file, "w") as file:
                                   json.dump(self.options, file, indent=4)
                              reset_key_mapping_bool = False
                              self.display_key_mapping_screen(screen)
                              
                         elif cancel_button.is_clicked(event):
                              reset_key_mapping_bool = False
                              self.display_key_mapping_screen(screen)
               pygame.display.update()
     
     def display_key_mapping_screen(self, screen):
          key_mapping_text = cfg.FONT.render("KEY MAPPING", True, cfg.WHITE)  
          key_mapping_text_rect = key_mapping_text.get_rect()
          key_mapping_text_rect.top = cfg.CELL_EDGE // 2
          key_mapping_text_rect.centerx = cfg.KEY_MAPPING_OVERLAY.width // 2
          
          key_names = [key for key in self.options["keys"].keys()]
          key_texts = []
          key_buttons = []
          
          for i, key in enumerate(key_names):
               key_text = cfg.FONT.render(key, True, cfg.WHITE)
               key_text_rect = key_text.get_rect()
               key_text_rect.top = (cfg.KEY_MAPPING_OVERLAY.height // (len(key_names) + 1) * (i + 1)) - (cfg.CELL_EDGE // 2)
               key_text_rect.left = cfg.CELL_EDGE
               key_texts.append((key_text, key_text_rect))
               
               key_button = Button(pygame.key.name(self.options["keys"][key]).upper(), (5 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.FONT, (cfg.LIGHT_GREY, cfg.DARK_GREY), cfg.KEY_MAPPING_OVERLAY.rect)
               key_button.center(3 * cfg.KEY_MAPPING_OVERLAY.width // 2, 2 * ((cfg.KEY_MAPPING_OVERLAY.height // (len(key_names) + 1) * (i + 1)) - (cfg.CELL_EDGE // 2) + cfg.CELL_EDGE // 3))
               key_buttons.append(key_button)
          
          reset_to_defaults_button = Button("RESET TO DEFAULTS", (8 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.FONT, (cfg.GREY, cfg.DARK_GREY), cfg.KEY_MAPPING_OVERLAY.rect)
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
          resolutions_text = cfg.FONT.render("RESOLUTIONS", True, cfg.WHITE)
          resolutions_text_rect = resolutions_text.get_rect()
          resolutions_text_rect.top = cfg.CELL_EDGE // 2
          resolutions_text_rect.centerx = cfg.RESOLUTIONS_OVERLAY.width // 2
          
          resolutions_list = [(cfg.BASE_WIDTH * i, cfg.BASE_HEIGHT * i) for i in cfg.RESOLUTION_SCALING_MULTIPLIERS]
          resolution_buttons_list = []
          
          for i, (width, height) in enumerate(resolutions_list):
               resolution_button = Button(f"{width}x{height}", (5 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.FONT, (cfg.LIGHT_GREY, cfg.DARK_GREY), cfg.RESOLUTIONS_OVERLAY.rect)
               resolution_button.center(cfg.RESOLUTIONS_OVERLAY.width, 2 * ((cfg.RESOLUTIONS_OVERLAY.height // (len(resolutions_list) + 1) * (i + 1) + (cfg.CELL_EDGE // 2))))
               resolution_buttons_list.append(resolution_button)
          
          resolutions_screen_bool = True
          while resolutions_screen_bool:
               self.draw_frames()
               if screen == "pause screen":
                    self.draw_gameloop()
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
          previous_resolution_scale_index = cfg.USER_CHOICE_SCALE
          
          def update_resolution(scale_index):
               global BACKGROUND
               cfg.update_resolution(scale_index)
               if check_if_background_image_exists:
                    BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (cfg.RESOLUTION_DISPLAY["width"], cfg.RESOLUTION_DISPLAY["height"]))
                    cfg.WINDOW.blit(BACKGROUND, (0, 0))
               for overlay in cfg.OVERLAYS:
                    overlay.update(cfg.CELL_EDGE)
               for frame in cfg.FRAMES:
                    frame.update(cfg.CELL_EDGE)
                    
          update_resolution(index)
               
          ok_button = Button("OK", (4 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.FONT, (cfg.GREEN, cfg.DARK_GREEN), cfg.KEEP_CHANGES_OVERLAY.rect)
          cancel_button = Button("CANCEL", (4 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.FONT, (cfg.LIGHT_GREY, cfg.DARK_GREY), cfg.KEEP_CHANGES_OVERLAY.rect)
          ok_button.center(cfg.KEEP_CHANGES_OVERLAY.width, 2 * (cfg.KEEP_CHANGES_OVERLAY.height - cfg.CELL_EDGE * 2) - cfg.CELL_EDGE)
          cancel_button.center(cfg.KEEP_CHANGES_OVERLAY.width, 2 * (cfg.KEEP_CHANGES_OVERLAY.height - cfg.CELL_EDGE))
          
          keep_changes_text = cfg.FONT.render("KEEP CHANGES?", True, cfg.WHITE)
          keep_changes_text_rect = keep_changes_text.get_rect()
          keep_changes_text_rect.top = cfg.CELL_EDGE
          keep_changes_text_rect.centerx = cfg.KEEP_CHANGES_OVERLAY.width // 2
     
          keep_changes_bool = True
          countdown_time = 11000
          countdown_start = pygame.time.get_ticks()
          while keep_changes_bool:
               self.draw_frames()
               if screen == "pause screen":
                    self.draw_gameloop()
               
               cfg.KEEP_CHANGES_OVERLAY.draw(cfg.WINDOW)
               cfg.KEEP_CHANGES_OVERLAY.element.fill(cfg.BLACK)
               pygame.draw.rect(cfg.KEEP_CHANGES_OVERLAY.element, cfg.LIGHT_GREY, cfg.KEEP_CHANGES_OVERLAY.element.get_rect(), 5)
               cfg.KEEP_CHANGES_OVERLAY.element.blit(keep_changes_text, keep_changes_text_rect)
               elapsed_time = pygame.time.get_ticks() - countdown_start
               remaining_time = max(0, (countdown_time - elapsed_time) // 1000)
               countdown_text = cfg.FONT.render(f"{remaining_time}", True, cfg.WHITE)
               countdown_text_rect = countdown_text.get_rect()
               countdown_text_rect.centerx = cfg.KEEP_CHANGES_OVERLAY.width // 2
               countdown_text_rect.centery = cfg.KEEP_CHANGES_OVERLAY.height // 2 - cfg.CELL_EDGE
               cfg.KEEP_CHANGES_OVERLAY.element.blit(countdown_text, countdown_text_rect)
               
               ok_button.draw(cfg.KEEP_CHANGES_OVERLAY.element)
               cancel_button.draw(cfg.KEEP_CHANGES_OVERLAY.element)
               
               if elapsed_time >= countdown_time:
                    keep_changes_bool = False
                    update_resolution(previous_resolution_scale_index)
                    self.display_resolutions_screen(screen)
               
               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         pygame.quit()
                         sys.exit()
                    elif event.type == pygame.KEYDOWN:
                         if event.key == pygame.K_ESCAPE:
                              keep_changes_bool = False
                              update_resolution(previous_resolution_scale_index)
                              self.display_resolutions_screen(screen)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                         if ok_button.is_clicked(event):
                              keep_changes_bool = False
                              self.options["resolution_scale_index"] = index
                              with open(db.options_file, "w") as file:
                                   json.dump(self.options, file, indent=4)
                              self.display_resolutions_screen(screen)
                         elif cancel_button.is_clicked(event):
                              keep_changes_bool = False
                              update_resolution(previous_resolution_scale_index)
                              self.display_resolutions_screen(screen)
               pygame.display.update()
     
     def draw_text(self, text, font, color, surface):
          textobj = font.render(text, True, color)
          textrect = textobj.get_rect()
          textrect.center = (cfg.GAME_OVER_OVERLAY.width // 2, cfg.GAME_OVER_OVERLAY.height // 2)
          surface.element.blit(textobj, textrect)
     
     def game_over_screen(self):
          game_over_bool = True
          score_values = [db.scores[i][1] for i in range(len(self.current_scores))]
          lowest_score = min(score_values)
          
          # Variables used when there is no new score
          high_scores_rect = pygame.Rect(0, 0, cfg.CELL_EDGE * 6, cfg.CELL_EDGE * 6)
          high_scores_rect.center = cfg.GAME_OVER_OVERLAY.width // 2, cfg.GAME_OVER_OVERLAY.height // 2
          
          game_over_text = cfg.FONT.render("GAME OVER", True, cfg.WHITE)
          game_over_text_rect = game_over_text.get_rect()
          game_over_text_rect.centerx = cfg.GAME_OVER_OVERLAY.width // 2
          game_over_text_rect.centery = high_scores_rect.top // 2
          
          high_scores_text = cfg.FONT.render("HIGH SCORES", True, cfg.WHITE)
          high_scores_text_rect = high_scores_text.get_rect()
          high_scores_text_rect.centerx = high_scores_rect.centerx
          high_scores_text_rect.top = high_scores_rect.top + cfg.USER_CHOICE_SCALE
          
          play_again_button = Button("PLAY AGAIN", (5 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.FONT, (cfg.GREEN, cfg.DARK_GREEN), cfg.GAME_OVER_OVERLAY.rect)
          play_again_button.center(cfg.GAME_OVER_OVERLAY.width, 2 * (high_scores_rect.bottom + cfg.CELL_EDGE) - cfg.CELL_EDGE // 2)
          main_menu_button = Button("MAIN MENU", (5 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.FONT, (cfg.LIGHT_GREY, cfg.DARK_GREY), cfg.GAME_OVER_OVERLAY.rect)
          main_menu_button.center(cfg.GAME_OVER_OVERLAY.width, 2 * (high_scores_rect.bottom + cfg.CELL_EDGE * 2))
          
          # Variables used when there is new score
          user_input = ""
          max_initials_length = 3
          
          new_high_score_text = cfg.FONT.render("NEW HIGH SCORE!", True, cfg.WHITE)
          new_high_score_text_rect = new_high_score_text.get_rect()
          new_high_score_text_rect.centerx = cfg.GAME_OVER_OVERLAY.width // 2
          new_high_score_text_rect.top = cfg.CELL_EDGE
          
          enter_initials_text = cfg.FONT.render("ENTER YOUR INITIALS:", True, cfg.WHITE)
          enter_initials_text_rect = enter_initials_text.get_rect()
          enter_initials_text_rect.centerx = cfg.GAME_OVER_OVERLAY.width // 2
          enter_initials_text_rect.top = cfg.GAME_OVER_OVERLAY.height // 2 - cfg.CELL_EDGE * 2
          
          ok_button = Button("OK", (2 * cfg.CELL_EDGE, cfg.CELL_EDGE), cfg.FONT, (cfg.LIGHT_GREY, cfg.DARK_GREY), cfg.GAME_OVER_OVERLAY.rect)
          ok_button.center(cfg.GAME_OVER_OVERLAY.width, cfg.GAME_OVER_OVERLAY.height + cfg.CELL_EDGE * 6)
               
          if self.score >= lowest_score:
               new_score = self.score
               score_number_text = cfg.FONT.render(str(new_score), True, cfg.WHITE)
               score_number_text_rect = score_number_text.get_rect()
               score_number_text_rect.centerx = cfg.GAME_OVER_OVERLAY.width // 2
               score_number_text_rect.top = cfg.CELL_EDGE * 2
          else:
               new_score = False
          
          while game_over_bool:
               cfg.GAME_OVER_OVERLAY.draw(cfg.WINDOW)
               cfg.GAME_OVER_OVERLAY.element.fill(cfg.BLACK)
               pygame.draw.rect(cfg.GAME_OVER_OVERLAY.element, cfg.LIGHT_GREY, cfg.GAME_OVER_OVERLAY.element.get_rect(), 5)
               if not new_score:
                    pygame.draw.rect(cfg.GAME_OVER_OVERLAY.element, cfg.LIGHT_GREY, high_scores_rect, width=1)
                    
                    cfg.GAME_OVER_OVERLAY.element.blit(game_over_text, game_over_text_rect)
                    cfg.GAME_OVER_OVERLAY.element.blit(high_scores_text, high_scores_text_rect)
                    for i, score in enumerate(self.current_scores):
                         # Drawing the initials
                         initial_to_draw = cfg.FONT.render(score[0], True, cfg.WHITE)
                         initial_to_draw_rect = pygame.Rect(0, 0, cfg.CELL_EDGE * 2, cfg.CELL_EDGE)
                         initial_to_draw_rect.left = high_scores_rect.left + cfg.USER_CHOICE_SCALE
                         initial_to_draw_rect.top = high_scores_rect.top + cfg.CELL_EDGE * (i + 1)
                         cfg.GAME_OVER_OVERLAY.element.blit(initial_to_draw, initial_to_draw_rect)
                         
                         # Drawing the scores
                         score_to_draw = cfg.FONT.render(str(score[1]), True, cfg.WHITE)
                         score_to_draw_rect = score_to_draw.get_rect()
                         score_to_draw_rect.right = high_scores_rect.right - cfg.USER_CHOICE_SCALE
                         score_to_draw_rect.top = high_scores_rect.top + cfg.CELL_EDGE * (i + 1)
                         cfg.GAME_OVER_OVERLAY.element.blit(score_to_draw, score_to_draw_rect)
                         
                         # Drawing the buttons
                         main_menu_button.draw(cfg.GAME_OVER_OVERLAY.element)
                         play_again_button.draw(cfg.GAME_OVER_OVERLAY.element)
               else:
                    cfg.GAME_OVER_OVERLAY.element.blit(new_high_score_text, new_high_score_text_rect)
                    cfg.GAME_OVER_OVERLAY.element.blit(score_number_text, score_number_text_rect)
                    cfg.GAME_OVER_OVERLAY.element.blit(enter_initials_text, enter_initials_text_rect)
                    self.draw_text(f"{user_input}", cfg.FONT, cfg.WHITE, cfg.GAME_OVER_OVERLAY)
                    ok_button.draw(cfg.GAME_OVER_OVERLAY.element)
                    
               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         pygame.quit()
                         sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                         if new_score:
                              if ok_button.is_clicked(event):
                                   # Save initial and score
                                   db.scores.append([user_input, new_score])
                                   db.scores.sort(key=lambda x: x[1], reverse=True)
                                   self.current_scores = db.scores[:5]
                                   with open(db.score_file, 'w') as file:
                                        json.dump(self.current_scores, file, indent=4)
                                   game_over_bool = False
                                   new_score = False
                                   self.main_menu()
                                   self.reset_game(starting_level)
                         else:
                              if main_menu_button.is_clicked(event):
                                   game_over_bool = False
                                   self.main_menu()
                              elif play_again_button.is_clicked(event):
                                   game_over_bool = False
                              self.reset_game(starting_level)
                    elif event.type == pygame.KEYDOWN:
                         if new_score:
                              if event.key == pygame.K_ESCAPE:
                                   game_over_bool = False
                                   self.reset_game(starting_level)
                                   self.main_menu()
                              elif event.key == pygame.K_RETURN:
                                   # Save initial and score
                                   db.scores.append([user_input, new_score])
                                   db.scores.sort(key=lambda x: x[1], reverse=True)
                                   self.current_scores = db.scores[:5]
                                   with open(db.score_file, 'w') as file:
                                        json.dump(self.current_scores, file, indent=4)
                                   new_score = False
                                   game_over_bool = False
                                   self.reset_game(starting_level)
                                   self.main_menu()
                              elif event.key == pygame.K_SPACE:
                                   pass
                              elif event.key == pygame.K_BACKSPACE:
                                   user_input = user_input[:-1]
                              elif len(user_input) < max_initials_length:
                                   user_input += event.unicode.upper()
                         else:
                              if event.key == pygame.K_ESCAPE:
                                   game_over_bool = False
                                   self.reset_game(starting_level)
                                   self.main_menu()
                                   
                                   
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
                    self.grid_y += 1
                    last_fall_time = current_time
               
               # Continuous movement
               if movement_left and not self.check_collision(dx=-1):
                    if current_time - last_move_time > move_fast_delay:
                         self.grid_x -= 1
                         last_move_time = current_time
               if movement_right and not self.check_collision(dx=1):
                    if current_time - last_move_time > move_fast_delay:
                         self.grid_x += 1
                         last_move_time = current_time
               if movement_bottom and not self.check_collision(dy=1):
                    if current_time - last_move_time > move_fast_delay:
                         self.grid_y += 1
                         self.score += 1
                         last_move_time = current_time

               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         running = False
                    
                    elif event.type == pygame.KEYDOWN:
                         # Pause
                         if event.key == pygame.K_ESCAPE:
                              movement_right = False
                              movement_left = False
                              movement_bottom = False
                              self.display_pause_screen()
                         
                         # Rotate right
                         elif event.key == self.current_keys["ROTATE RIGHT"]:
                              self.rotation += 1
                              if self.rotation == len(self.tetromino):
                                   self.rotation = 0
                         
                         # Rotate left
                         elif event.key == self.current_keys["ROTATE LEFT"]:
                              if self.rotation == 0:
                                   self.rotation = len(self.tetromino)
                              self.rotation -= 1
                         
                         # Hard drop
                         elif event.key == self.current_keys["HARD DROP"]:
                              self.hard_drop()
                              holdable = True
                         
                         # Hold 
                         elif event.key == self.current_keys["HOLD"]:
                              if holdable:
                                   # If there is no tetromino in hold, put the current tetromino in hold and get a new one
                                   if not self.hold_tetromino:
                                        self.hold_tetromino = self.tetromino
                                        self.grid_x = 2
                                        self.grid_y = -1
                                        self.rotation = 0
                                        self.tetromino = self.next_tetromino
                                        self.next_tetromino = self.get_tetromino()
                                        holdable = False
                                   # If there is a tetromino in hold, swap the hold and current tetrominos
                                   else:
                                        self.tetromino, self.hold_tetromino = self.hold_tetromino, self.tetromino
                                        self.grid_x = 2
                                        self.grid_y = -1
                                        self.rotation = 0
                                        holdable = False
                         
                         # Soft drop
                         elif event.key == self.current_keys["SOFT DROP"] and not self.check_collision(dy=1):
                              self.grid_y += 1
                              movement_bottom = True
                              self.score += 1
                              last_move_time = current_time + initial_move_delay  # Adding initial delay for the first move
                         
                         # Left
                         elif event.key == self.current_keys["MOVE LEFT"]:
                              movement_left = True
                              if not self.check_collision(dx=-1):
                                   self.grid_x -= 1
                              last_move_time = current_time + initial_move_delay  # Adding initial delay for the first move
                         
                         # Right
                         elif event.key == self.current_keys["MOVE RIGHT"]:
                              movement_right = True
                              if not self.check_collision(dx=1):
                                   self.grid_x += 1 
                              last_move_time = current_time + initial_move_delay  # Adding initial delay for the first move
                    
                    # Stop continuous movement if buttons aren't being pressed
                    elif event.type == pygame.KEYUP:
                         if event.key == self.current_keys["MOVE LEFT"]:
                              movement_left = False
                         elif event.key == self.current_keys["MOVE RIGHT"]:
                              movement_right = False
                         elif event.key == self.current_keys["SOFT DROP"]:
                              movement_bottom = False           
               
               # Update and draw
               self.clear_rows()
               self.draw_frames()
               self.draw_playframe_lines()
               self.draw_tetromino()
               self.draw_gameloop()
               self.draw_ghost_piece()
               
               # Place tetromino if tetromino reached the bottom or if there's a collision with another tetromino in the y axis
               if self.check_collision(dy=1):
                    self.place_tetromino()
                    holdable = True

                    # Reset tetromino position and get a new one
                    self.grid_x = 2
                    self.grid_y = -1
                    self.rotation = 0
                    self.tetromino = self.next_tetromino
                    self.next_tetromino = self.get_tetromino()
                    last_fall_time = pygame.time.get_ticks()  # Reset fall time to avoid instant fall of new tetromino

          pygame.quit()



tetris = Tetris()

if __name__ == "__main__":
     tetris.main()