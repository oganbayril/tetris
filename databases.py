import os
import json
import pygame

script_dir = os.path.dirname(os.path.abspath(__file__))
options_file = f"{script_dir}\options.json"
score_file = f"{script_dir}\scores.json"
resolutions_file = f"{script_dir}\resolutions.json"

# Default keys for tetris
default_keys = {
        "MOVE RIGHT": pygame.K_RIGHT,
        "MOVE LEFT": pygame.K_LEFT,
        "ROTATE RIGHT": pygame.K_UP,
        "ROTATE LEFT": pygame.K_z,
        "SOFT DROP": pygame.K_DOWN,
        "HARD DROP": pygame.K_SPACE,
        "HOLD": pygame.K_c
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