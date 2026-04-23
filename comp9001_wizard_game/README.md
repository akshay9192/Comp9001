# COMP9001 Knowledge Castle (13-Week Platformer RPG)

This project is a modular Mario-style educational platformer built with **pygame**.

## Highlights
- 13-week COMP9001 progression (Week 1 to Week 13)
- Leon mentor NPC hints during platforming
- Boss fight at end of each week
- Armin quiz gate after each boss (10 questions, pass >= 7)
- Retry quiz on fail (no full level restart)
- Async game loop for pygbag/web compatibility

## Run locally
```bash
cd comp9001_wizard_game
pip install -r requirements.txt
python main.py
```

## Build with pygbag
```bash
cd comp9001_wizard_game
pip install pygbag
python -m pygbag --build .
```

## Deploy to GitHub Pages
1. Build with pygbag.
2. Publish generated web output folder to `gh-pages` (or configured Pages source).
3. Enable GitHub Pages in repository settings.

## Architecture
- `main.py`: async entrypoint
- `game.py`: central engine/state machine
- `player.py`: movement/physics/stats
- `level.py` + `world.py`: level composition and mechanics
- `enemies.py` + `bosses.py`: combat entities
- `quiz_engine.py`: Armin quiz gate logic
- `mentor.py`: Leon/Armin dialogue systems
- `ui.py`: HUD/dialogue/quiz overlays
- `data/weeks.json`: full 13-week syllabus + quizzes
