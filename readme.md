# 🐍 Snake Pygame

**A dynamic snake game built from scratch using Pygame — featuring adaptive music, sound effects, and evolving gameplay.**  
Crafted solo by [Aymen27k](https://github.com/Aymen27k), this project marks the birth of a game designer.

---

## 🎮 Features

- **Modular architecture**: Classes for snake, food, scoreboard, walls, music, and sound.
- **Dynamic menu**: A roaming snake with randomized growth and fade-in music.
- **Adaptive difficulty**: Game speed increases with score, capped at 20.
- **Tense music trigger**: At score 50, music shifts to a more intense track.
- **Sound effects**: Eating, speeding up, and game over events are sonically marked.
- **Highscore tracking**: Stored locally in `highscore.json`.
- **Sprite integration**: Custom visuals for snake, food, and environment.
- **Future plans**: Alien enemy with projectile attacks and epic boss music.

---

## 🧩 Installation

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

🎵 Assets

- \*\*Music and sound effects sourced from Pixabay.
- \*\*All assets are royalty-free and safe to include under the Pixabay license.

snake_pygame/
├── assets/ # Music and sound files
├── .vscode/ # Editor settings
├── .gitignore
├── requirements.txt
├── highscore.json
├── main.py # Game loop and state manager
├── background.py
├── food.py
├── musicmanager.py
├── soundmanager.py
├── scoreboard.py
├── snake.py
├── sprite.py
└── walls.py

🏆 Credits
Developed by Aymen Kalai Ezar
Music & SFX: Pixabay
Engine: Pygame
