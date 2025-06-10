# Tetris Game

A fully functional Tetris game built in Python with customizable features and modern gameplay elements.

## Features

### Core Gameplay
- Classic Tetris mechanics with falling tetrominoes
- Line clearing and scoring system
- Increasing difficulty as you progress
- Score saving and high score tracking

### Menus & Interface
- **Main Menu** - Start game and access settings
- **Pause Menu** - Pause/resume gameplay
- **Keybind Menu** - Customize your controls
- **Resolution Menu** - Adjust screen resolution
- **Settings Menu** - Configure game preferences

### Customization
- **Custom Controls** - Remap keys to your preference
- **Resolution Options** - Multiple screen resolutions supported
- **Custom Background** - Use your own background image
- **Save System** - Your scores and settings are automatically saved

## Installation

### Using uv (Recommended)
1. Make sure you have Python installed on your system
2. Install uv if you haven't already:
   - Visit [uv's official website](https://docs.astral.sh/uv/getting-started/installation/)
   - Follow the installation instructions for your operating system
   - Or use the quick install script: `curl -LsSf https://astral.sh/uv/install.sh | sh`
3. Download all game files to a folder
4. Install dependencies:
   ```bash
   uv sync
   ```
5. Run the game:
   ```bash
   python main.py
   ```

### Alternative Installation
1. Make sure you have Python installed on your system
2. Install pygame manually:
   ```bash
   pip install pygame
   ```
3. Run the game:
   ```bash
   python main.py
   ```

## Customizing Your Background

To use your own background image:

1. Prepare your image file (PNG format recommended)
2. Open `main.py` in a text editor
3. Find line 14:
   ```python
   background_image_file = r"C:\Users\PC\Desktop\YOUR_BACKGROUND_IMAGE_FILE.png"
   ```
4. Replace the path with your image file path:
   ```python
   background_image_file = r"C:\path\to\your\image.png"
   ```
5. Save the file and restart the game

## Controls

Default controls (customizable in-game):
- **Left Arrow** - Move piece left
- **Right Arrow** - Move piece right
- **Up Arrow** - Rotate piece clockwise
- **Z** - Rotate piece counter-clockwise
- **Down Arrow** - Soft drop
- **Space** - Hard drop
- **C** - Hold piece

*Note: All controls can be changed through the Keybind Menu*

## Game Modes & Difficulty

### Difficulty Levels
- **Starting Level**: Customizable in main menu (click level button)
- **Available starting levels**: 1, 3, 5, 7, 9, 11 (cycles through when clicked)
- **Level Progression**: Increases by 1 every 10 lines cleared during gameplay
- **Speed Increase**: Each level reduces fall delay, making pieces drop faster
- **Death Mode**: Reach level 15 for the ultimate challenge with maximum speed!

### Gameplay Features
- **Hold System**: Store a piece for later use
- **T-Spin Recognition**: Advanced T-spin mechanics with bonus scoring
- **Line Clear Detection**: Standard Tetris line clearing
- **Progressive Speed**: Game gets faster as you improve

## Scoring

### Standard Line Clears
- **Single**: 100 × (level + 1) points
- **Double**: 300 × (level + 1) points  
- **Triple**: 500 × (level + 1) points
- **Tetris (4 lines)**: 800 × (level + 1) points

### T-Spin Bonuses
- **T-Spin Single**: 800 × (level + 1) points
- **T-Spin Double**: 1200 × (level + 1) points
- **T-Spin Triple**: 1600 × (level + 1) points

*Higher levels multiply your score significantly!*

## System Requirements

- Python 3.6 or higher
- Pygame library
- Windows/Mac/Linux compatible
- Minimum 640x360 screen resolution

## File Structure

```
tetris-game/
├── main.py              # Main game file
├── databases.py         # Game settings and data
├── button.py             # Customizable button class
├── config.py             # Configuration file for game colors, menus, other interfaces and tetrominos
├── pyproject.toml       # Project configuration
├── uv.lock             # Dependency lock file
└── README.md           # This file
```

## Troubleshooting

### Common Issues

**Game won't start:**
- Ensure Python and Pygame are properly installed
- Check that all game files are in the same directory

**Background image not showing:**
- Verify the image path in line 14 of main.py
- Ensure the image file exists and is accessible
- Use PNG or JPG format for best compatibility

**Controls not working:**
- Reset controls to default in the Keybind Menu
- Check for conflicting key assignments

## Features Overview

✅ Complete Tetris gameplay  
✅ Multiple menu systems  
✅ Customizable controls  
✅ Resolution options  
✅ Score saving  
✅ Custom backgrounds  
✅ Pause functionality  
✅ Progressive difficulty  

## Contributing

This is a complete, standalone Tetris implementation. Feel free to modify and enhance the code for your own projects!

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) - see the [LICENSE](LICENSE) file for details.

You are free to use, modify, and distribute this code for personal and commercial purposes.

---

**Enjoy playing Tetris!** 🎮

*For any issues or questions, please check the troubleshooting section above.*