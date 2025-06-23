# Flap.py 🐦

A modern Python implementation of the classic Flappy Bird game built with Pygame, featuring smooth animations, particle effects, and polished gameplay mechanics.

![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-v2.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

- **Smooth Gameplay**: 60 FPS gameplay with fluid bird movement and rotation
- **Visual Effects**: Particle systems for jumps, collisions, and scoring
- **Audio Integration**: Sound effects for jumps, collisions, and scoring
- **Game States**: Complete menu system with pause functionality
- **Score Tracking**: Persistent high score tracking
- **Responsive Controls**: Intuitive keyboard controls
- **Fallback Assets**: Graceful fallbacks when assets are missing

## 🎮 Controls

| Key | Action |
|-----|--------|
| `SPACE` | Jump / Start Game / Restart |
| `P` | Pause / Resume |
| `ESC` | Return to Menu |

## 🚀 Getting Started

### Prerequisites

- Python 3.6 or higher
- Pygame 2.0 or higher

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/flap-py.git
   cd flap-py
   ```

2. **Install dependencies**
   ```bash
   pip install pygame
   ```

3. **Run the game**
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
flap-py/
│
├── main.py              # Main game file
├── Fonts/               # Font assets (optional)
│   └── BaiJamjuree-Bold.ttf
├── Sounds/              # Audio assets (optional)
│   ├── slap.wav         # Collision sound
│   ├── woosh.wav        # Jump sound
│   └── score.wav        # Score sound
└── Images/              # Visual assets (optional)
    ├── player.png       # Bird sprite
    ├── pipe_up.png      # Bottom pipe
    ├── pipe_down.png    # Top pipe
    ├── ground.png       # Ground texture
    └── background.png   # Background image
```

## 🎨 Asset Requirements

The game includes automatic fallbacks, so it will run without assets. However, for the full experience, include:

### Images
- `player.png` - 34x24px bird sprite
- `pipe_up.png` / `pipe_down.png` - 52x320px pipe sprites  
- `ground.png` - 400x64px ground texture
- `background.png` - 400x600px background

### Audio
- `slap.wav` - Collision sound effect
- `woosh.wav` - Jump sound effect  
- `score.wav` - Score sound effect

### Fonts
- `BaiJamjuree-Bold.ttf` - Custom font (falls back to system font)

## 🎯 Game Mechanics

### Player Physics
- **Gravity**: Constant downward acceleration
- **Jump**: Instant upward velocity on spacebar press
- **Rotation**: Dynamic rotation based on velocity
- **Idle Animation**: Gentle bobbing when game hasn't started

### Pipe System
- **Procedural Generation**: Randomly positioned pipes
- **Collision Detection**: Pixel-perfect collision system
- **Scoring**: Points awarded when passing pipes
- **Visual Feedback**: Highlight effect when scoring

### Particle Effects
- **Jump Particles**: White particles on jump
- **Collision Explosion**: Red particles on collision
- **Score Burst**: Yellow particles when scoring

## 🔧 Customization

### Difficulty Settings
Modify these variables in `main.py`:

```python
# Pipe speed and gap
pipes.append(Pipe(400, new_height, 180, 2.4))  # gap=180, speed=2.4

# Player physics
self.velocity += 0.75  # Gravity strength
self.velocity = -10    # Jump strength
```

### Visual Settings
```python
window_w = 400    # Window width
window_h = 600    # Window height
fps = 60          # Frame rate
```

## 🐛 Troubleshooting

### Common Issues

**Game won't start**
- Ensure Python 3.6+ is installed
- Install pygame: `pip install pygame`

**No sound**
- Check that audio files are in the `Sounds/` directory
- Verify audio file formats (WAV recommended)

**Missing graphics**
- Game uses colored rectangles as fallbacks
- Place image files in `Images/` directory for full visual experience

**Performance issues**
- Reduce FPS in the code: `fps = 30`
- Close other applications to free up system resources

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

1. **Bug Reports**: Open an issue describing the problem
2. **Feature Requests**: Suggest new features or improvements
3. **Code Contributions**: Fork the repo and submit a pull request
4. **Asset Creation**: Create new sprites, sounds, or fonts

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -am 'Add new feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the original Flappy Bird by Dong Nguyen
- Built with [Pygame](https://www.pygame.org/)
- Font: Bai Jamjuree (if included)

## 📊 Stats

- **Language**: Python
- **Framework**: Pygame
- **Lines of Code**: ~400+
- **File Size**: Lightweight (~15KB without assets)

---

**Enjoy the game!** 🎮 Star this repo if you found it helpful!
