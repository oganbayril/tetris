import os
import json
import pygame

options_file = "options.json"
score_file = "scores.json"

# Default keys for tetris
default_keys = {
        "move right": pygame.K_RIGHT,
        "move left": pygame.K_LEFT,
        "rotate right": pygame.K_UP,
        "rotate left": pygame.K_z,
        "soft drop": pygame.K_DOWN,
        "hard drop": pygame.K_SPACE,
        "hold": pygame.K_c
}

# Getting keys
if os.path.exists(options_file):
    with open(options_file, "r") as file:
        keys = json.load(file)
else:
    keys = default_keys
    with open(options_file, "w") as file:
        json.dump(keys, file, indent=4)

# Getting high scores
if os.path.exists(score_file):
    with open(score_file, "r") as file:
        scores = json.load(file)
else:
    scores = [["", 5000],
              ["", 4000],
              ["", 3000],
              ["", 2000],
              ["", 1000]]
    with open(score_file, "w") as file:
        json.dump(scores, file, indent=4)