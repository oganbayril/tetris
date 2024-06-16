import pygame
import random
import os
import sys
import json

from button import Button
from databases import options_file, default_keys, keys, score_file, scores
from config import *

# Upload an image file named tetris_background.jpg in the same directory and uncomment lines 13, 14 and 51 to have a background of your choosing

# BACKGROUND_IMAGE = pygame.image.load(os.path.join("tetris", "tetris_background.jpg"))
# BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))

tetrominos = [I, J, L, O, S, T, Z]
tetromino_colors = [LIGHT_BLUE, DARK_BLUE, ORANGE, YELLOW, GREEN, PURPLE, RED]
current_keys = keys
current_scores = scores
starting_level = 1

class Tetris:
     def __init__(self):
          self.reset_game()
     
     def reset_game(self, level=1):
          self.x = PLAY_SCREEN_X_START
          self.y = PLAY_SCREEN_Y_START
          self.rows = 10
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
          WINDOW.fill(BLACK)
          # WINDOW.blit(BACKGROUND, (0, 0))
          pygame.draw.rect(WINDOW, BLACK, PLAY_SCREEN)
          pygame.draw.rect(WINDOW, BLACK, NEXT_SCREEN)
          pygame.draw.rect(WINDOW, BLACK, HOLD_SCREEN)
          pygame.draw.rect(WINDOW, BLACK, SCORE_SCREEN)
          
          # Draw next tetromino screen
          pygame.draw.rect(WINDOW, LIGHT_GREY, NEXT_SCREEN, width=1)
          next_text = font.render("NEXT", True, WHITE)
          next_rect = next_text.get_rect(center=((NEXT_SCREEN_X_START + NEXT_SCREEN_X_END) / 2, NEXT_SCREEN_Y_START + SQUARE))
          WINDOW.blit(next_text, next_rect)
          
          # Draw hold screen
          pygame.draw.rect(WINDOW, LIGHT_GREY, HOLD_SCREEN, width=1)
          hold_text = font.render("HOLD", True, WHITE)
          hold_rect = hold_text.get_rect(center=((HOLD_SCREEN_X_START + HOLD_SCREEN_X_END) / 2, HOLD_SCREEN_Y_START + SQUARE))
          WINDOW.blit(hold_text, hold_rect)
          
          # Draw score screen
          pygame.draw.rect(WINDOW, LIGHT_GREY, SCORE_SCREEN, width=1)
          score_text = font.render("SCORE", True, WHITE)
          level_text = font.render("LEVEL", True, WHITE)
          lines_text = font.render("LINES", True, WHITE)
          
          score_text_rect = score_text.get_rect(center=((SCORE_SCREEN_X_START + SCORE_SCREEN_X_END) / 2, SCORE_SCREEN_Y_START + SQUARE))
          level_text_rect = level_text.get_rect(center=((SCORE_SCREEN_X_START + SCORE_SCREEN_X_END) / 2, SCORE_SCREEN_Y_START + 5 * SQUARE))
          lines_text_rect = lines_text.get_rect(center=((SCORE_SCREEN_X_START + SCORE_SCREEN_X_END) / 2, SCORE_SCREEN_Y_START + 9 * SQUARE))
          
          WINDOW.blit(score_text, score_text_rect)
          WINDOW.blit(level_text, level_text_rect)
          WINDOW.blit(lines_text, lines_text_rect)
     
     def draw_gameloop(self):
          # Draw lines in the play screen
          line_x = PLAY_SCREEN_X_START
          line_y = PLAY_SCREEN_Y_START
          
          for _ in range(self.rows+1):
               pygame.draw.line(WINDOW, GREY, (line_x, line_y), (line_x, PLAY_SCREEN_Y_END))
               for _ in range(self.columns + 1):
                    pygame.draw.line(WINDOW, GREY, (line_x, line_y), (PLAY_SCREEN_X_END, line_y))
                    line_y += SQUARE
               line_x += SQUARE
               
               line_y = PLAY_SCREEN_Y_START
          line_x = PLAY_SCREEN_X_START
          
          # Draw hold tetromino
          hold_x_positions = []
          hold_y_positions = []
          
          if len(self.hold_tetromino) == 4 or (len(self.hold_tetromino) == 2 and self.hold_tetromino != I):
               for i, string in enumerate(self.hold_tetromino[0], start=-2):
                    for j, tetromino_piece in enumerate(string, start=-2):
                         if tetromino_piece == "0":
                              x_position = (HOLD_SCREEN_X_START + HOLD_SCREEN_X_END) / 2 + j * SQUARE - SQUARE / 2
                              y_position = (HOLD_SCREEN_Y_START + HOLD_SCREEN_Y_END) / 2 + i * SQUARE
                              hold_x_positions.append(x_position)
                              hold_y_positions.append(y_position)
          elif self.hold_tetromino == I:
               for i, string in enumerate(self.hold_tetromino[0], start=-2):
                    for j, tetromino_piece in enumerate(string, start=-2):
                         if tetromino_piece == "0":
                              x_position = (HOLD_SCREEN_X_START + HOLD_SCREEN_X_END) / 2 + (j - 1) * SQUARE
                              y_position = (HOLD_SCREEN_Y_START + HOLD_SCREEN_Y_END) / 2 + (i + 1) * SQUARE - SQUARE / 2
                              hold_x_positions.append(x_position)
                              hold_y_positions.append(y_position)
          else:
               for i, string in enumerate(self.hold_tetromino[0], start=-2):
                    for j, tetromino_piece in enumerate(string, start=-2):
                         if tetromino_piece == "0":
                              x_position = (HOLD_SCREEN_X_START + HOLD_SCREEN_X_END) / 2 + (j - 1) * SQUARE
                              y_position = (HOLD_SCREEN_Y_START + HOLD_SCREEN_Y_END) / 2 + i * SQUARE
                              hold_x_positions.append(x_position)
                              hold_y_positions.append(y_position)

          for x, y in list(zip(hold_x_positions, hold_y_positions)):
               pygame.draw.rect(WINDOW, tetromino_colors[tetrominos.index(self.hold_tetromino)], (x, y, SQUARE - 1, SQUARE - 1))
          
          # Draw next tetromino
          next_x_positions = []
          next_y_positions = []
          
          if len(self.next_tetromino) == 4 or (len(self.next_tetromino) == 2 and self.next_tetromino != I):
               for i, string in enumerate(self.next_tetromino[0], start=-2):
                    for j, tetromino_piece in enumerate(string, start=-2):
                         if tetromino_piece == "0":
                              x_position = (NEXT_SCREEN_X_START + NEXT_SCREEN_X_END) / 2 + j * SQUARE - SQUARE / 2
                              y_position = (NEXT_SCREEN_Y_START + NEXT_SCREEN_Y_END) / 2 + i * SQUARE
                              next_x_positions.append(x_position)
                              next_y_positions.append(y_position)
          elif self.next_tetromino == I:
               for i, string in enumerate(self.next_tetromino[0], start=-2):
                    for j, tetromino_piece in enumerate(string, start=-2):
                         if tetromino_piece == "0":
                              x_position = (NEXT_SCREEN_X_START + NEXT_SCREEN_X_END) / 2 + (j - 1) * SQUARE
                              y_position = (NEXT_SCREEN_Y_START + NEXT_SCREEN_Y_END) / 2 + (i + 1) * SQUARE - SQUARE / 2
                              next_x_positions.append(x_position)
                              next_y_positions.append(y_position)
          else:
               for i, string in enumerate(self.next_tetromino[0], start=-2):
                    for j, tetromino_piece in enumerate(string, start=-2):
                         if tetromino_piece == "0":
                              x_position = (NEXT_SCREEN_X_START + NEXT_SCREEN_X_END) / 2 + (j - 1) * SQUARE
                              y_position = (NEXT_SCREEN_Y_START + NEXT_SCREEN_Y_END) / 2 + i * SQUARE
                              next_x_positions.append(x_position)
                              next_y_positions.append(y_position)

          for x, y in list(zip(next_x_positions, next_y_positions)):
               pygame.draw.rect(WINDOW, tetromino_colors[tetrominos.index(self.next_tetromino)], (x, y, SQUARE - 1, SQUARE - 1))
          
          # Draw placed tetrominos
          for y, row in enumerate(self.board):
               for x, val in enumerate(row):
                    if val != 0:
                         pygame.draw.rect(WINDOW, tetromino_colors[val - 1], (PLAY_SCREEN_X_START + (x * SQUARE), PLAY_SCREEN_Y_START + (y * SQUARE), SQUARE - 1, SQUARE - 1))
          
          # Draw corresponding numbers in score screen
          score_number = font.render(str(self.score), True, WHITE)
          level_number = font.render(str(self.level), True, WHITE)
          lines_number = font.render(str(self.lines), True, WHITE)
          
          score_number_rect = score_number.get_rect(center=((SCORE_SCREEN_X_START + SCORE_SCREEN_X_END) / 2, SCORE_SCREEN_Y_START + 2 * SQUARE))
          level_number_rect = level_number.get_rect(center=((SCORE_SCREEN_X_START + SCORE_SCREEN_X_END) / 2, SCORE_SCREEN_Y_START + 6 * SQUARE))
          lines_number_rect = lines_number.get_rect(center=((SCORE_SCREEN_X_START + SCORE_SCREEN_X_END) / 2, SCORE_SCREEN_Y_START + 10 * SQUARE))
          
          WINDOW.blit(score_number, score_number_rect)
          WINDOW.blit(level_number, level_number_rect)
          WINDOW.blit(lines_number, lines_number_rect)
          
          

     
     def draw_tetromino(self):
          global min_x, max_x, x_positions, y_positions
          min_x, max_x = PLAY_SCREEN_X_END, PLAY_SCREEN_X_START
          min_y, max_y = PLAY_SCREEN_Y_END, PLAY_SCREEN_Y_START
          x_positions, y_positions = [], []

          for i, string in enumerate(self.tetromino[self.rotation], start=-2):
               for j, tetromino_piece in enumerate(string, start=-2):
                    if tetromino_piece == "0":
                         x_position = (self.x + PLAY_SCREEN_X_END) / 2 + (j - 1) * SQUARE
                         y_position = self.y + (i + 1) * SQUARE
                         min_x = min(min_x, x_position)
                         max_x = max(max_x, x_position + SQUARE)
                         min_y = min(min_y, y_position)
                         max_y = max(max_y, y_position)
                         x_positions.append(x_position)
                         y_positions.append(y_position)
          
          # Implementing wall kick
          while min(x_positions) < PLAY_SCREEN_X_START:
               x_positions = [x + SQUARE for x in x_positions]
               self.x += 2 * SQUARE
          while max(x_positions) >= PLAY_SCREEN_X_END:
               x_positions = [x - SQUARE for x in x_positions]
               self.x -= 2 * SQUARE
          
          # Draw tetromino
          for x, y in zip(x_positions, y_positions):
               pygame.draw.rect(WINDOW, tetromino_colors[tetrominos.index(self.tetromino)], (x, y, SQUARE - 1, SQUARE - 1))

          pygame.display.update()

     
     def place_tetromino(self):
          # Update game board with tetromino and assign colors
          for i, string in enumerate(self.tetromino[self.rotation], start=-2):
               for j, tetromino_piece in enumerate(string, start=-2):
                    if tetromino_piece == "0":
                         x_position = int((self.x + PLAY_SCREEN_X_END) / 2 + (j - 1) * SQUARE)
                         y_position = self.y + (i + 1) * SQUARE
                         grid_x = int((x_position - PLAY_SCREEN_X_START) / SQUARE)
                         grid_y = int((y_position - PLAY_SCREEN_Y_START) / SQUARE)
                         self.board[grid_y][grid_x] = tetrominos.index(self.tetromino) + 1
          
          
     def check_collision_y(self):
          # Check bottom collision
          if max(y_positions) == PLAY_SCREEN_Y_END-SQUARE:
               return True
          
          # Check tetromino collision with other blocks
          for i, string in enumerate(self.tetromino[self.rotation], start=-2):
               for j, tetromino_piece in enumerate(string, start=-2):
                    if tetromino_piece == "0":
                         x_position = int((self.x + PLAY_SCREEN_X_END) / 2 + (j - 1) * SQUARE)
                         y_position = self.y + (i + 1) * SQUARE
                         grid_x = int((x_position - PLAY_SCREEN_X_START) / SQUARE)
                         grid_y = int((y_position - PLAY_SCREEN_Y_START) / SQUARE)
                         
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
                         x_position = (self.x + PLAY_SCREEN_X_END) / 2 + (j - 1) * SQUARE
                         y_position = self.y + (i + 1) * SQUARE
                         grid_x = int((x_position - PLAY_SCREEN_X_START) / SQUARE)
                         grid_y = int((y_position - PLAY_SCREEN_Y_START) / SQUARE)

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
                         x_position = (self.x + PLAY_SCREEN_X_END) / 2 + (j - 1) * SQUARE
                         y_position = self.y + (i + 1) * SQUARE
                         grid_x = int((x_position - PLAY_SCREEN_X_START) / SQUARE)
                         grid_y = int((y_position - PLAY_SCREEN_Y_START) / SQUARE)
                         
                         # Return false if the x position goes out of bounds, otherwise can't implement wall kick
                         if grid_x >= 10:
                              return False
                         # Return true if there's collision
                         if self.board[grid_y][grid_x] != 0:
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
               self.y += SQUARE
               self.score += 2
          self.place_tetromino()
          
          # Reset tetromino position and get a new one
          self.x = PLAY_SCREEN_X_START
          self.y = PLAY_SCREEN_Y_START
          self.rotation = 0
          self.tetromino = self.next_tetromino
          self.next_tetromino = self.get_tetromino()
     
     def get_fall_delay(self, level):
          # Fall speed
          return max(50, 1100 - level * 100)
     
     
     def main_menu(self):
          global starting_level
          play_button = Button("PLAY", (4 * SQUARE, SQUARE), font, (GREEN, DARK_GREEN))
          options_button = Button("OPTIONS", (4 * SQUARE, SQUARE), font, (GREY, DARK_GREY))
          
          play_button.center(WIDTH, PLAY_SCREEN_Y_START + 200)
          options_button.center(WIDTH, PLAY_SCREEN_X_START + 500)
          
          main_menu_bool = True
          
          while main_menu_bool:
               level_button = Button(f"LEVEL: {starting_level}", (4 * SQUARE, SQUARE), font, (GREY, DARK_GREY))
               level_button.center(WIDTH, PLAY_SCREEN_Y_START + 280)
               self.draw_window()
               pygame.draw.rect(WINDOW, LIGHT_GREY, PLAY_SCREEN, width=1)
               high_scores_text = font.render("HIGH SCORES", True, WHITE)
               high_scores_text_rect = high_scores_text.get_rect(center=(WIDTH // 2, 250))
               high_scores_rect = pygame.Rect(WIDTH // 2 - 60, 240, 120, 120)
               pygame.draw.rect(WINDOW, LIGHT_GREY, high_scores_rect, width=1)
               WINDOW.blit(high_scores_text, high_scores_text_rect)
               
               for i, score in enumerate(current_scores):
                    # Drawing the initials
                    initial_to_draw = font.render(score[0], True, WHITE)
                    initial_to_draw_rect = pygame.Rect(high_scores_rect.left + 5, 260 + i * SQUARE, 4 * SQUARE, SQUARE)
                    WINDOW.blit(initial_to_draw, initial_to_draw_rect)
                    
                    # Drawing the scores
                    score_to_draw = font.render(str(score[1]), True, WHITE)
                    score_to_draw_rect = pygame.Rect(high_scores_rect.right - score_to_draw.get_width() - 5, 260 + i * SQUARE, 4 * SQUARE, SQUARE)
                    WINDOW.blit(score_to_draw, score_to_draw_rect)
               
               # Drawing buttons in the main screen, otherwise buttons don't work
               play_button.draw(WINDOW)
               options_button.draw(WINDOW)
               level_button.draw(WINDOW)
               
               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         pygame.quit()
                         sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                         if play_button.is_clicked(event):
                              main_menu_bool = False
                         elif options_button.is_clicked(event):
                              main_menu_bool = False
                              self.options_screen("main menu")
                         elif level_button.is_clicked(event):
                              if self.level == 1:
                                   starting_level = 3 
                                   self.reset_game(starting_level)
                              elif self.level == 3:
                                   starting_level = 5
                                   self.reset_game(starting_level)
                              elif self.level == 5:
                                   starting_level = 7 
                                   self.reset_game(starting_level)
                              elif self.level == 7:
                                   starting_level = 9 
                                   self.reset_game(starting_level)
                              elif self.level == 9:
                                   starting_level = 11 
                                   self.reset_game(starting_level)
                              else:
                                   starting_level = 1 
                                   self.reset_game(starting_level)
               pygame.display.update()
     
     def pause_screen(self):
          pause_text = font.render("PAUSED", True, WHITE)
          pause_text_rect = pause_text.get_rect(center=(PAUSE_SCREEN_WIDTH // 2, 15))
          resume_button = Button("RESUME", (4 * SQUARE, SQUARE), font, (GREEN, DARK_GREEN))
          resume_button.center(WIDTH, HEIGHT - 6 * SQUARE)
          options_button = Button("OPTIONS", (4 * SQUARE, SQUARE), font, (LIGHT_GREY, DARK_GREY))
          options_button.center(WIDTH, HEIGHT + SQUARE)
          quit_button = Button("QUIT", (4 * SQUARE, SQUARE), font, (LIGHT_GREY, DARK_GREY))
          quit_button.center(WIDTH, HEIGHT + 8 * SQUARE)
          
          paused = True
          
          while paused:
               WINDOW.blit(PAUSE_SCREEN, PAUSE_SCREEN_RECT)
               PAUSE_SCREEN.fill(BLACK)
               pygame.draw.rect(PAUSE_SCREEN, LIGHT_GREY, PAUSE_SCREEN.get_rect(), 5)
               PAUSE_SCREEN.blit(pause_text, pause_text_rect)
               
               resume_button.draw(WINDOW)
               options_button.draw(WINDOW)
               quit_button.draw(WINDOW)
               
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
                              self.options_screen("pause screen")
                         if quit_button.is_clicked(event):
                              paused = False
                              self.main_menu()
                              self.reset_game(starting_level)
               
               pygame.display.update()
     
     def change_keybind(self, action, screen):
          changing_key = True
          
          while changing_key:
               if screen == "main menu":
                    self.draw_window()
               elif screen == "pause screen":
                    self.draw_window()
                    self.draw_gameloop()
                    
               pygame.draw.rect(WINDOW, LIGHT_GREY, PLAY_SCREEN, width=1)
               WINDOW.blit(KEYBIND_SCREEN, KEYBIND_SCREEN_RECT)
               KEYBIND_SCREEN.fill(BLACK)
               pygame.draw.rect(KEYBIND_SCREEN, LIGHT_GREY, KEYBIND_SCREEN.get_rect(), 5)
               
               new_keybind_text = font.render("ENTER NEW KEYBIND FOR", True, WHITE)
               new_keybind_text_rect = new_keybind_text.get_rect(center=(KEYBIND_SCREEN_WIDTH // 2, KEYBIND_SCREEN_HEIGHT // 2 - 10))
               KEYBIND_SCREEN.blit(new_keybind_text, new_keybind_text_rect)
               
               keybind_text = font.render(str(action).upper(), True, WHITE)
               keybind_text_rect = keybind_text.get_rect(center=(KEYBIND_SCREEN_WIDTH // 2, KEYBIND_SCREEN_HEIGHT // 2 + 10))
               KEYBIND_SCREEN.blit(keybind_text, keybind_text_rect)
               
               
               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         pygame.quit()
                         sys.exit()
                    elif event.type == pygame.KEYDOWN:
                         if event.key == pygame.K_ESCAPE:
                              pass
                         else:
                              current_keys[action] = event.key
                              changing_key = False
                         
                              # If keybind is the same as another action, that action will be left blank
                              for key, value in current_keys.items():
                                   if key != action and value == current_keys[action]:
                                        current_keys[key] = 0
                              
                              # Updating the options file with the new change
                              json_data = json.dumps(current_keys, indent=4)
                              with open(options_file, "w") as file:
                                   file.write(json_data)
                              self.options_screen(screen)
               pygame.display.update()
     
     def options_screen(self, screen):
          options_text = font.render("OPTIONS", True, WHITE)
          move_right_text = font.render("MOVE RIGHT", True, WHITE)
          move_left_text = font.render("MOVE LEFT", True, WHITE)
          rotate_right_text = font.render("ROTATE RIGHT", True, WHITE)
          rotate_left_text = font.render("ROTATE LEFT", True, WHITE)
          soft_drop_text = font.render("SOFT DROP", True, WHITE)
          hard_drop_text = font.render("HARD DROP", True, WHITE)
          hold_text = font.render("HOLD", True, WHITE)
          
          options_text_rect = options_text.get_rect(center=(OPTIONS_SCREEN_WIDTH // 2, 15))
          
          move_right_button = Button(pygame.key.name(current_keys["move right"]).upper(), (5 * SQUARE, SQUARE), font, (LIGHT_GREY, DARK_GREY))
          move_left_button = Button(pygame.key.name(current_keys["move left"]).upper(), (5 * SQUARE, SQUARE), font, (LIGHT_GREY, DARK_GREY))
          rotate_right_button = Button(pygame.key.name(current_keys["rotate right"]).upper(), (5 * SQUARE, SQUARE), font, (LIGHT_GREY, DARK_GREY))
          rotate_left_button = Button(pygame.key.name(current_keys["rotate left"]).upper(), (5 * SQUARE, SQUARE), font, (LIGHT_GREY, DARK_GREY))
          soft_drop_button = Button(pygame.key.name(current_keys["soft drop"]).upper(), (5 * SQUARE, SQUARE), font, (LIGHT_GREY, DARK_GREY))
          hard_drop_button = Button(pygame.key.name(current_keys["hard drop"]).upper(), (5 * SQUARE, SQUARE), font, (LIGHT_GREY, DARK_GREY))
          hold_button = Button(pygame.key.name(current_keys["hold"]).upper(), (5 * SQUARE, SQUARE), font, (LIGHT_GREY, DARK_GREY))
          reset_options_button = Button("RESET OPTIONS", (7 * SQUARE, SQUARE), font, (GREY, DARK_GREY))
          
          move_right_button.center(WIDTH + 6 * SQUARE, 312 + SQUARE)
          move_left_button.center(WIDTH + 6 * SQUARE, 312 + 5 * SQUARE)
          rotate_right_button.center(WIDTH + 6 * SQUARE, 312 + 9 * SQUARE)
          rotate_left_button.center(WIDTH + 6 * SQUARE, 312 + 13 * SQUARE)
          soft_drop_button.center(WIDTH + 6 * SQUARE, 312 + 17 * SQUARE)
          hard_drop_button.center(WIDTH + 6 * SQUARE, 312 + 21 * SQUARE)
          hold_button.center(WIDTH + 6 * SQUARE, 312 + 25 * SQUARE)
          reset_options_button.center(WIDTH, 312 + 30 * SQUARE)
          
          waiting_for_input = True
          
          while waiting_for_input:
               WINDOW.blit(OPTIONS_SCREEN, OPTIONS_SCREEN_RECT)
               OPTIONS_SCREEN.fill(BLACK)
               pygame.draw.rect(OPTIONS_SCREEN, LIGHT_GREY, OPTIONS_SCREEN.get_rect(), 5)
               OPTIONS_SCREEN.blit(options_text, options_text_rect)
               OPTIONS_SCREEN.blit(move_right_text, (2 * SQUARE, 3 * SQUARE, 4 * SQUARE, SQUARE))
               OPTIONS_SCREEN.blit(move_left_text, (2 * SQUARE, 5 * SQUARE, 5 * SQUARE, SQUARE))
               OPTIONS_SCREEN.blit(rotate_right_text, (2 * SQUARE, 7 * SQUARE, 5 * SQUARE, SQUARE))
               OPTIONS_SCREEN.blit(rotate_left_text, (2 * SQUARE, 9 * SQUARE, 5 * SQUARE, SQUARE))
               OPTIONS_SCREEN.blit(soft_drop_text, (2 * SQUARE, 11 * SQUARE, 5 * SQUARE, SQUARE))
               OPTIONS_SCREEN.blit(hard_drop_text, (2 * SQUARE, 13 * SQUARE, 5 * SQUARE, SQUARE))
               OPTIONS_SCREEN.blit(hold_text, (2 * SQUARE, 15 * SQUARE, 5 * SQUARE, SQUARE))
               
               move_right_button.draw(WINDOW)
               move_left_button.draw(WINDOW)
               rotate_right_button.draw(WINDOW)
               rotate_left_button.draw(WINDOW)
               soft_drop_button.draw(WINDOW)
               hard_drop_button.draw(WINDOW)
               hold_button.draw(WINDOW)
               reset_options_button.draw(WINDOW)
               
               
               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         pygame.quit()
                         sys.exit()
                    elif event.type == pygame.KEYDOWN:
                         if event.key == pygame.K_ESCAPE:
                              waiting_for_input = False
                              if screen == "main menu":
                                   waiting_for_input = False
                                   self.main_menu()
                              elif screen == "pause screen":
                                   waiting_for_input = False
                                   self.draw_window()
                                   self.draw_gameloop()
                                   self.draw_tetromino()
                                   self.pause_screen()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                         waiting_for_input = False
                         if move_right_button.is_clicked(event):
                              self.change_keybind("move right", screen)
                         elif move_left_button.is_clicked(event):
                              self.change_keybind("move left", screen)
                         elif rotate_right_button.is_clicked(event):
                              self.change_keybind("rotate right", screen)
                         elif rotate_left_button.is_clicked(event):
                              self.change_keybind("rotate left", screen)
                         elif soft_drop_button.is_clicked(event):
                              self.change_keybind("soft drop", screen)
                         elif hard_drop_button.is_clicked(event):
                              self.change_keybind("hard drop", screen)
                         elif hold_button.is_clicked(event):
                              self.change_keybind("hold", screen)
                         elif reset_options_button.is_clicked(event):
                              self.reset_options_screen(screen)
                         else:
                              waiting_for_input = True
                         
                         
               pygame.display.update()
     
     def reset_options_screen(self, screen):
          reset_options_bool = True
          
          while reset_options_bool:
               if screen == "main menu":
                    self.draw_window()
               elif screen == "pause screen":
                    self.draw_window()
                    self.draw_gameloop()
               
               pygame.draw.rect(WINDOW, LIGHT_GREY, PLAY_SCREEN, width=1)
               
               reset_options_text = font.render("RESET OPTIONS?", True, WHITE)
               reset_options_text_rect = reset_options_text.get_rect(center=(RESET_OPTIONS_SCREEN_WIDTH // 2, 15))
               WINDOW.blit(RESET_OPTIONS_SCREEN, RESET_OPTIONS_SCREEN_RECT)
               RESET_OPTIONS_SCREEN.fill(BLACK)
               pygame.draw.rect(RESET_OPTIONS_SCREEN, LIGHT_GREY, RESET_OPTIONS_SCREEN.get_rect(), 5)
               RESET_OPTIONS_SCREEN.blit(reset_options_text, reset_options_text_rect)
               
               button_ok = Button("OK", (4 * SQUARE, SQUARE), font, (LIGHT_GREY, DARK_GREY))
               button_cancel = Button("CANCEL", (4 * SQUARE, SQUARE), font, (LIGHT_GREY, DARK_GREY))
               
               button_ok.center(WIDTH, HEIGHT - SQUARE)
               button_cancel.center(WIDTH, HEIGHT + 3 * SQUARE)
               
               button_ok.draw(WINDOW)
               button_cancel.draw(WINDOW)
               
               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         pygame.quit()
                         sys.exit()
                    elif event.type == pygame.KEYDOWN:
                         if event.key == pygame.K_ESCAPE:
                              reset_options_bool = False
                              self.options_screen(screen)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                         if button_ok.is_clicked(event):
                              global current_keys
                              current_keys = default_keys.copy()
                              if os.path.exists(options_file):
                                   os.remove(options_file)
                              with open(options_file, "w") as file:
                                   json.dump(current_keys, file, indent=4)
                              reset_options_bool = False
                              self.options_screen(screen)
                              
                         elif button_cancel.is_clicked(event):
                              reset_options_bool = False
                              self.options_screen(screen)
               pygame.display.update()
     
     
     def draw_text(self, text, font, color, surface):
          textobj = font.render(text, True, color)
          textrect = textobj.get_rect()
          textrect.center = (GAME_OVER_SCREEN_WIDTH // 2, 90)
          surface.blit(textobj, textrect)
     
     def game_over_screen(self):
          global current_scores
          game_over_bool = True
          score_values = [scores[i][1] for i in range(len(current_scores))]
          lowest_score = min(score_values)
          
          # Variables used when there is no new score
          game_over_text = font.render("GAME OVER", True, WHITE)
          high_scores_text = font.render("HIGH SCORES", True, WHITE)
          
          main_menu_button = Button("MAIN MENU", (4 * SQUARE, SQUARE), font, (LIGHT_GREY, DARK_GREY))
          play_again_button = Button("PLAY AGAIN", (4 * SQUARE, SQUARE), font, (GREEN, DARK_GREEN))
          
          main_menu_button.center(WIDTH, HEIGHT + 5 * SQUARE)
          play_again_button.center(WIDTH, HEIGHT + 9 * SQUARE)
               
          game_over_text_rect = game_over_text.get_rect(center=(GAME_OVER_SCREEN_WIDTH // 2, 15))
          high_scores_text_rect = high_scores_text.get_rect(center=(GAME_OVER_SCREEN_WIDTH // 2, 40))
          
          # Variables used when there is new score
          user_input = ""
          max_initials_length = 3
          
          new_high_score_text = font.render("NEW HIGH SCORE!", True, WHITE)
          enter_initials_text = font.render("ENTER YOUR INITIALS:", True, WHITE)
          
          ok_button = Button("OK", (2 * SQUARE, SQUARE), font, (LIGHT_GREY, DARK_GREY))
          ok_button.center(WIDTH, HEIGHT + 5 * SQUARE)
          
          new_high_score_text_rect = new_high_score_text.get_rect(center=(GAME_OVER_SCREEN_WIDTH // 2, 15))
          enter_initials_text_rect = enter_initials_text.get_rect(center=(GAME_OVER_SCREEN_WIDTH // 2, 65))
          
               
          if self.score >= lowest_score:
               new_score = self.score
               score_number_text = font.render(str(new_score), True, WHITE)
               score_number_text_rect = score_number_text.get_rect(center=(GAME_OVER_SCREEN_WIDTH // 2, 40))
          else:
               new_score = False
          
          while game_over_bool:
               WINDOW.blit(GAME_OVER_SCREEN, GAME_OVER_SCREEN_RECT)
               GAME_OVER_SCREEN.fill(BLACK)
               pygame.draw.rect(GAME_OVER_SCREEN, LIGHT_GREY, GAME_OVER_SCREEN.get_rect(), 5)
               if not new_score:
                    high_scores_rect = pygame.Rect(60, 30, 120, 120)
                    pygame.draw.rect(GAME_OVER_SCREEN, LIGHT_GREY, high_scores_rect, width=1)
                    
                    
                    GAME_OVER_SCREEN.blit(game_over_text, game_over_text_rect)
                    GAME_OVER_SCREEN.blit(high_scores_text, high_scores_text_rect)
                    for i, score in enumerate(current_scores):
                         # Drawing the initials
                         initial_to_draw = font.render(score[0], True, WHITE)
                         initial_to_draw_rect = pygame.Rect(high_scores_rect.left + 5, 50 + i * SQUARE, 4 * SQUARE, SQUARE)
                         GAME_OVER_SCREEN.blit(initial_to_draw, initial_to_draw_rect)
                         
                         # Drawing the scores
                         score_to_draw = font.render(str(score[1]), True, WHITE)
                         score_to_draw_rect = pygame.Rect(high_scores_rect.right - score_to_draw.get_width() - 5, 50 + i * SQUARE, 4 * SQUARE, SQUARE)
                         GAME_OVER_SCREEN.blit(score_to_draw, score_to_draw_rect)
                         
                         # Drawing the buttons
                         main_menu_button.draw(WINDOW)
                         play_again_button.draw(WINDOW)
               else:
                    GAME_OVER_SCREEN.blit(new_high_score_text, new_high_score_text_rect)
                    GAME_OVER_SCREEN.blit(score_number_text, score_number_text_rect)
                    GAME_OVER_SCREEN.blit(enter_initials_text, enter_initials_text_rect)
                    self.draw_text(f"{user_input}", font, WHITE, GAME_OVER_SCREEN)
                    ok_button.draw(WINDOW)
                    
               
               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         pygame.quit()
                         sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                         if new_score:
                              if ok_button.is_clicked(event):
                                   # Save initial and score
                                   scores.append([user_input, new_score])
                                   scores.sort(key=lambda x: x[1], reverse=True)
                                   current_scores = scores[:5]
                                   with open(score_file, 'w') as file:
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
                                   scores.append([user_input, new_score])
                                   scores.sort(key=lambda x: x[1], reverse=True)
                                   current_scores = scores[:5]
                                   with open(score_file, 'w') as file:
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
               if self.board[0][4] or self.board[0][5] != 0:
                    self.game_over_screen()
               
               # Tetromino fall
               if current_time - last_fall_time > fall_delay:
                    self.y += SQUARE
                    last_fall_time = current_time
               
               # Continuous movement
               if movement_left and not self.check_collision_x("left"):
                    if current_time - last_move_time > move_fast_delay:
                         self.x -= 2 * SQUARE
                         last_move_time = current_time
               if movement_right and not self.check_collision_x("right"):
                    if current_time - last_move_time > move_fast_delay:
                         self.x += 2 * SQUARE
                         last_move_time = current_time
               if movement_bottom and not self.check_collision_y():
                    if current_time - last_move_time > move_fast_delay:
                         self.y += SQUARE
                         self.score += 1
                         last_move_time = current_time

               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         running = False
                    
                    elif event.type == pygame.KEYDOWN:
                         # Pause
                         if event.key == pygame.K_ESCAPE:
                              self.pause_screen()
                         
                         # Rotate right
                         elif event.key == current_keys["rotate right"] and not self.check_collision_rotation(1):
                              self.rotation += 1
                              if self.rotation == len(self.tetromino):
                                   self.rotation = 0
                         
                         # Rotate left
                         elif event.key == current_keys["rotate left"] and not self.check_collision_rotation(-1):
                              if self.rotation == 0:
                                   self.rotation = len(self.tetromino)
                              self.rotation -= 1
                         
                         # Hard drop
                         elif event.key == current_keys["hard drop"]:
                              self.hard_drop()
                              holdable = True
                         
                         # Hold 
                         elif event.key == current_keys["hold"]:
                              if holdable:
                                   if len(self.hold_tetromino) == 1 and self.hold_tetromino != O:
                                        self.hold_tetromino = self.tetromino
                                        self.x = PLAY_SCREEN_X_START
                                        self.y = PLAY_SCREEN_Y_START
                                        self.rotation = 0
                                        self.tetromino = self.next_tetromino
                                        self.next_tetromino = self.get_tetromino()
                                        holdable = False
                                   else:
                                        placeholder = self.hold_tetromino
                                        self.hold_tetromino = self.tetromino
                                        self.tetromino = placeholder
                                        self.x = PLAY_SCREEN_X_START
                                        self.y = PLAY_SCREEN_Y_START
                                        self.rotation = 0
                                        holdable = False
                         
                         # Soft drop
                         elif event.key == current_keys["soft drop"] and not self.check_collision_y():
                              self.y += SQUARE
                              movement_bottom = True
                              self.score += 1
                              last_move_time = current_time + initial_move_delay  # Adding initial delay for the first move
                         
                         # Left
                         elif event.key == current_keys["move left"]:
                              movement_left = True
                              if not self.check_collision_x("left"):
                                   self.x -= 2 * SQUARE
                              last_move_time = current_time + initial_move_delay  # Adding initial delay for the first move
                         
                         # Right
                         elif event.key == current_keys["move right"]:
                              movement_right = True
                              if not self.check_collision_x("right"):
                                   self.x += 2 * SQUARE
                              last_move_time = current_time + initial_move_delay  # Adding initial delay for the first move
                    
                    # Stop continuous movement if buttons aren't being pressed
                    elif event.type == pygame.KEYUP:
                         if event.key == current_keys["move left"]:
                              movement_left = False
                         elif event.key == current_keys["move right"]:
                              movement_right = False
                         elif event.key == current_keys["soft drop"]:
                              movement_bottom = False           
               
               # Update and draw
               self.clear_rows()
               self.draw_window()
               self.draw_gameloop()
               self.draw_tetromino()
               
               # Place tetromino if tetromino reached the bottom or if there's a collision with another tetromino in the y axis
               if self.check_collision_y():
                    self.place_tetromino()
                    holdable = True

                    # Reset tetromino position and get a new one
                    self.x = PLAY_SCREEN_X_START
                    self.y = PLAY_SCREEN_Y_START
                    self.rotation = 0
                    self.tetromino = self.next_tetromino
                    self.next_tetromino = self.get_tetromino()
                    last_fall_time = pygame.time.get_ticks()  # Reset fall time to avoid instant fall of new tetromino

          pygame.quit()



tetris = Tetris()

if __name__ == "__main__":
     tetris.main()