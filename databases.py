import os
import json
import pygame
import copy

script_dir = os.path.dirname(os.path.abspath(__file__))
score_file = f"{script_dir}/scores.json"
options_file = f"{script_dir}/options.json"

# Default keys and resolution scaling index
default_options = {
    "keys": {
        "MOVE RIGHT": pygame.K_RIGHT,
        "MOVE LEFT": pygame.K_LEFT,
        "ROTATE RIGHT": pygame.K_UP,
        "ROTATE LEFT": pygame.K_z,
        "SOFT DROP": pygame.K_DOWN,
        "HARD DROP": pygame.K_SPACE,
        "HOLD": pygame.K_c
    },
    "resolution_scale_index": 1  # Default scale index (960x540)
}

# Getting the keys and the resolution
if os.path.exists(options_file):
    with open(options_file, "r") as file:
        options = json.load(file)
else:
    options = copy.deepcopy(default_options)
    with open(options_file, "w") as file:
        json.dump(options, file, indent=4)

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