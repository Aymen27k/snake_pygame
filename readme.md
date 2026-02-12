# 🐍 Snake Pygame

**A dynamic snake game built from scratch using Pygame — featuring fluid controls, adaptive music, and evolving boss encounters.**  
Crafted solo by [Aymen27k](https://github.com/Aymen27k), this project marks the journey of a game designer.

---

## 🎮 Features

- **Fluid controls**: Input buffering with a command queue for precise U‑turns and high‑speed play.
- **Boss stability**: Milestones fixed to trigger reliably, even during death animations.
- **Modular architecture**: Classes for snake, food, scoreboard, walls, music, and sound.
- **Dynamic menu**: A roaming snake with randomized growth and fade‑in music.
- **Adaptive difficulty**: Speed scales with score, capped at 20.
- **Tense music trigger**: At score 30, soundtrack shifts to an intense track.
- **Sound effects**: Eating, speeding up, and game over events are sonically marked.
- **Highscore tracking**: Stored locally in `game_data.json`.
- **Sprite integration**: Custom visuals for snake, food, and environment.
- **Automated CI/CD**: Cross-platform binaries (Windows/Linux) automatically built via GitHub Actions.

---

## 📦 Releases

Download binaries directly from the [Releases page](https://github.com/Aymen27k/snake_pygame/releases/tag/v1.1).  
Latest: **v1.1 — Fluid Controls & Boss Stability Update**

## 🚀 Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/Aymen27k/snake_pygame.git
   cd snake_pygame

   ```

2. Create and activate a virtual environment:
   python -m venv .venv
   source .venv/bin/activate # Linux/Mac
   .venv\Scripts\activate # Windows

3. Install dependencies:
   pip install -r requirements.txt
4. Run the game:
   python main.py

## 🎵 Assets

- **Music and sound effects** sourced from Pixabay
- **All assets are royalty-free** and safe to include under the Pixabay license

## 📁 Project Structure

```text
snake_pygame/
├── assets/                  # Image sprites, Music and sound files
├── .github/                 # GitHub workflows and actions
├── .vscode/                 # Editor settings
├── .gitignore               # Git ignore rules
├── LICENSE                  # Project license (CC BY-NC 4.0)
├── requirements.txt         # Python dependencies
├── game_data.json           # Saved game data
├── main.py                  # Game loop and state manager
├── constants.py             # Global constants
├── data_manager.py          # Handles save/load operations
├── hud.py                   # Heads-up display elements
├── background.py            # Background rendering
├── food.py                  # Food logic
├── snake.py                 # Snake logic
├── walls.py                 # Wall logic
├── sprite.py                # Sprite integration
├── musicmanager.py          # Music control
├── soundmanager.py          # Sound effects control
├── alien.py                 # Alien enemy logic
├── projectile.py            # Projectile attacks
├── shuriken.py              # Shuriken projectile logic
├── path_util.py             # Path utilities
└── readme.md                # Project documentation
```

## 🏆 Credits

- **Developed by** Aymen Kalai Ezar
- **Music & SFX**: [Pixabay](https://pixabay.com/)
- **Engine**: [Pygame](https://www.pygame.org/)

## 📜 License

This project is shared under CC BY‑NC 4.0.

- Free to play, learn, and remix.
- Attribution required — credit must always flow back to the original author.
- ❌ Commercial use is not permitted.
