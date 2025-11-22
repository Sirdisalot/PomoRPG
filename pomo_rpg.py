import time
import json
import os
import random
from datetime import datetime

# We will use 'rich' for a modern, colorful CLI experience
# If you don't have it , run: pip install rich

try:
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
    from rich.panel import Panel
    from rich.layout import Layout
    from rich import print as rprint
except ImportError:
    print("This app requires the 'rich' library. Please install it using 'pip install rich'")
    exit(1)

console = Console()

#CONFIGURATION
DATA_FILE = "pomo_rpg_data.json"
WORK_DURATION = 25 * 60  # 25 minutes
BREAK_DURATION = 5 * 60   # 5 minutes
XP_PER_SESSION = 100

#GAME LOGIC & PERSISTANCE
class Player:
    def __init__(self):
        self.level = 1
        self.current_xp = 0
        self.required_xp = 500 # Starting requirement
        self.sessions_completed = 0
        self.title = "Novice Focuser"

    def gain_xp(self, amount):
        self.current_xp += amount
        self.sessions_completed += 1
        console.print(f"[bold green] + {amount} XP![/bold green]")

        # Check for level up
        if self.current_xp >= self.required_xp:
            self.level_up()
    
    def level_up(self):
        self.level += 1
        self.current_xp -= self.required_xp
        self.required_xp = int(self.required_xp * 1.5)  # Increase XP requirement
        
         # Flavor text for leveling up
        titles = {"Apprentice Focuser", "Adept Focuser", "Master Focuser", "Grandmaster Focuser", "Sage of Focuser"}

        console.print(Panel(f"[bold yellow]LEVEL UP![/bold yellow]\nYou are now Level {self.level} - {self.title}!", title="Congratulations"))

    def to_dict(self):
        return {
            "level": self.level,
            "current_xp": self.current_xp,
            "required_xp": self.required_xp,
            "sessions_completed": self.sessions_completed,
            "title": self.title
        }
    
    def from_dict(self, data):
        self.level = data.get("level", 1)
        self.current_xp = data.get("current_xp", 0)
        self.required_xp = data.get("required_xp", 500)
        self.sessions_completed = data.get("sessions_completed", 0)
        self.title = data.get("title", "Novice Focuser")

def save_game(player):
    # Save player data to a JSON file
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(player.to_dict(), f, indent=4)
        # We don't print here to avoid clutter, but the data is safe
    except Exception as e:
        console.print(f"[bold red]Error saving game: {e}[/bold red]")

def load_game():
    # Load player data from a JSON file
    player = Player()
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                player.from_dict(data)
            console.print("[green]Welcome back. Profile loaded[/green]")
        except Exception as e:
            console.print(f"[red]Error loading game: {e}[/red]")
    else:
        console.print("[blue]New adventure started. Creating profile...[/blue]")
    return player

#TIME FUNCTIONALITY
