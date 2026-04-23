# COMP9001 Wizard Game

A story-driven 2D educational RPG built with **Python + pygame**.

You play as a student progressing through a 3-week COMP9001-style course. Your background (wealthy, middle-income, or lower-income) changes your starting resources and the likelihood/impact of events, simulating inequality in education.

## Features

- Player personalization (name, course, background) inside pygame UI (desktop + browser compatible)
- Inequality-aware stat system (`xp`, `time`)
- 3 structured course weeks with learning topics and decisions
- Random weekly events (positive and negative)
- Mentor + Guide advice with class-sensitive dialogue
- Multiple endings based on performance and pressure
- Async-compatible pygame loop for `pygbag`

## Project Structure

```text
comp9001_wizard_game/
│── main.py
│── game.py
│── config.py
│── events.py
│── ui.py
│── assets/
│── requirements.txt
│── README.md
```

## Run Locally

```bash
cd comp9001_wizard_game
pip install -r requirements.txt
python main.py
```

## Build for Browser with pygbag

Install pygbag (outside project requirements):

```bash
pip install pygbag
```

Build web assets from the `comp9001_wizard_game` directory:

```bash
python -m pygbag --build .
```

After build, output is generated in a `build/web/` style folder (path may vary by pygbag version).

## Deploy to GitHub Pages (quick path)

1. Build with `pygbag`.
2. Push generated web build files to a branch served by GitHub Pages (commonly `gh-pages`).
3. In GitHub repo settings, set **Pages** source to the branch/folder containing the generated `index.html`.
4. Wait for Pages deployment, then open your published URL.

## Inequality System (Short Explanation)

The game assigns different starting `xp` and `time` by background:

- **Wealthy**: starts with more resources and easier access to advantages
- **Middle-income**: balanced start and mixed event pressure
- **Lower-income**: fewer initial resources and higher pressure, but includes support/catch-up paths

This creates different gameplay trajectories while keeping all paths fully completable.
