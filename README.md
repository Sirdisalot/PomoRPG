PomoRPG - The Gamified Pomodoro Timer

PomoRPG is a command-line productivity tool that turns the Pomodoro Technique into a Role-Playing Game. Earn experience points (XP) for every successful work session, level up your character, and track your productivity stats over time.

Features

Timer Logic: Standard 25-minute work sessions and 5-minute breaks.

Gamification: * Gain XP for finishing tasks.

Level up and earn new titles (e.g., Novice -> Apprentice -> Master).

XP requirements scale as you reach higher levels.

Persistence: Your progress (Level, XP, stats) is automatically saved to a JSON file, so you pick up right where you left off.

Modern UI: Uses the rich library for beautiful terminal progress bars, tables, and colors.

Prerequisites

Python 3.6 or higher.

The rich python library.

Installation

Clone the repository:

git clone [https://github.com/Sirdisalot/pomo-rpg.git](https://github.com/Sirdisalot/pomo-rpg.git)
cd pomo-rpg


Install dependencies:
This project relies on rich for terminal formatting.

pip install rich


Usage

Run the application directly from your terminal:

python pomo_rpg.py


Controls

Start Work Session: Begins a 25-minute countdown. If you interrupt it (Ctrl+C), you gain no XP.

Start Break: Begins a 5-minute countdown to rest your eyes.

View Stats: Displays your current Level, Title, and XP progress bar.

Quit: Saves your data and exits.

Project Structure

pomo_rpg.py: The main entry point containing the Game Loop, Player class, and Timer logic.

pomo_rpg_data.json: (Generated automatically) Stores your save data.

Future Roadmap (Ideas for Contribution)

Add a "Long Break" (15 min) option after 4 sessions.

Implement an Inventory system to store "Loot" found during sessions.

Add sound effects for timer completion.

Create a "Quest" system (e.g., "Complete 4 sessions today").

License

MIT
