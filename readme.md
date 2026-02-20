# 🛸 Snake vs Alien (v1.2)

**A high-octane evolution of the classic Snake, featuring tactical boss combat, haptic feedback, and cross-platform polish.** Crafted solo by [Aymen27k](https://github.com/Aymen27k).

---

## 🎮 New in v1.2: "The Patterns & Polish Update"

- **🎮 Full Controller Support**: Plug-and-play compatibility with Xbox and Analog controllers, featuring hot-swap stability.
- **📳 Haptic Immersion**: Integrated controller rumble during boss spawns and major events to heighten tension.
- **🐍 Dynamic menu**: A roaming snake with randomized growth and fade‑in music.
- **🧠 Intelligent Boss AI**: Alien encounters now feature predictable, telegraphable attack patterns (Vertical, Horizontal, and 4-way Bursts).
- **🟡 Visual Telegraphing**: Bosses glow golden before dangerous attacks, allowing for skill-based dodging.
- **🍎 Sprite integration**: Custom visuals for snake, food, and environment.
- **🔊 Enhanced Soundscape**: New menu SFX, selection audio, and independent Mute toggles for music/SFX.

---

## 🚀 Quick Start (Play Now!)

Don't want to run the code? Download the standalone binaries for your OS:
- **[Download for Windows (.exe)](https://github.com/Aymen27k/Snake_pygame/releases/latest)**
- **[Download for Linux](https://github.com/Aymen27k/Snake_pygame/releases/latest)**

---

## 🛠️ Technical Engineering

- **Fluid Controls**: Input buffering with a command queue for precise U-turns.
- **Modular Architecture**: Decoupled classes for Snake logic, Boss AI, Scoreboard, and Audio Management.
- **Automated CI/CD**: Parallel Windows/Linux builds triggered via GitHub Actions (.yml).
- **Persistent Data**: Local high-score and settings tracking via `game_data.json`.
- **Dynamic Difficulty**: Real-time speed scaling and adaptive music triggers based on player performance.

---

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
├── input_manager.py         # Handles translation of inputs into actions
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
