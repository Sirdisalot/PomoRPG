import time
import json
import os
import random
import platform
from datetime import datetime

# We will use 'rich' for a modern, colorful CLI experience
# If you don't have it , run: pip install rich

try:
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
    from rich.panel import Panel
    from rich.layout import Layout
    from rich import print as rprint
except ImportError:
    print("This app requires the 'rich' library. Please install it using 'pip install rich'")
    exit(1)

console = Console()

#CONFIGURATION
DATA_FILE = "pomo_rpg_data.json"
WORK_DURATION = 1 * 60  # 25 minutes
BREAK_DURATION = 1 * 60   # 5 minutes
LONG_BREAK_DURATION = 1 * 60  # 20 minutes
XP_PER_SESSION = 100

#GAME LOGIC & PERSISTANCE

class Player:
    def __init__(self):
        self.level = 1
        self.current_xp = 0
        self.required_xp = 500 # Starting requirement
        self.sessions_completed = 0
        self.sessions_since_long_break = 0
        self.title = "Novice Focuser"

    def gain_xp(self, amount):
        self.current_xp += amount
        self.sessions_completed += 1
        self.sessions_since_long_break += 1
         # Flavor text for gaining XP
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
            "sessions_since_long_break": self.sessions_since_long_break,
            "title": self.title
        }
    
    def from_dict(self, data):
        self.level = data.get("level", 1)
        self.current_xp = data.get("current_xp", 0)
        self.required_xp = data.get("required_xp", 500)
        self.sessions_completed = data.get("sessions_completed", 0)
        self.sessions_since_long_break = data.get("sessions_since_long_break", 0)
        self.title = data.get("title", "Novice Focuser")

def play_sound():
    # Plays a cross-platform sound notification
    sys_os = platform.system()
    try:
        if sys_os == "Windows":
            import winsound
            winsound.Beep(1000, 1000)  # Frequency, Duration
        elif sys_os == "Darwin":  # macOS
            os.system('afplay /System/Library/Sounds/Ping.aiff')
        elif sys_os == "Linux":
            # Try 'spd-say' (speech-dispatcher) first as it's common on Ubuntu/Debian
            if os.system("spd-say 'Timer Complete' 2>/dev/null") != 0:
                print('\a')  # Fallback to bell character
        else:
            print('\a')
    except Exception as e:
        pass  # If sound fails, just ignore

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

#TIMER FUNCTIONALITY
def run_timer(duration, task_name="Focusing"):
    # Runs a visual progress bar for the specified duration.
    console.print(f"\n[bold white]Beginning task: {task_name}[/bold white]")

    # Rich progress bar context manager
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("."),
        TimeRemainingColumn(),
        console=console
    ) as progress:
        task_id = progress.add_task(f"{task_name}...", total=duration)
        while not progress.finished:
            time.sleep(1) # Udpate every second
            progress.update(task_id, advance=1)
    
    console.print(f"[bold green]{task_name} complete![/bold green] \a")  # \a is the bell character

#UI & MENUS
def show_stats(player):
    # Displays the player's RPG stats in a table format
    table = Table(title="Character Status")
    
    table.add_column("Attribute", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")

    table.add_row("Title", str(player.title))
    table.add_row("Level", str(player.level))
    table.add_row("XP", f"{player.current_xp} / {player.required_xp}")
    table.add_row("Sessions Completed", str(player.sessions_completed))
    table.add_row("Streak (to Long Break)", f"{player.sessions_since_long_break}" / 4)

    # Calculate progress bar for XP manually for the table view
    xp_percent = int((player.current_xp / player.required_xp) * 20)
    xp_bar = "█" * xp_percent + "░" * (20 - xp_percent)
    table.add_row("XP Progress", f"[{xp_bar}]")

    console.print(table)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(Panel.fit("[bold magneta]Welcome to Pomodoro RPG![/bold magneta]\nGamifiy your productivity journey!", subtitle="v1.0"))

    player = load_game()

    while True:
        print("\n")
        # Determine break type
        if player.sessions_since_long_break >= 4:
            break_desc = "Long Break"
            break_dur_text = "20 min"
            break_style = "bold cyan"
        else:
            break_desc = "Short Break"
            break_dur_text = "5 min"
            break_style = "blue"


        console.print("[bold]Choose an action:[/bold]")
        console.print("[1. [green]Start Work Session[/green] (25 min)]")
        console.print(f"[2. [{break_style}]Start {break_desc}[/{break_style}] ({break_dur_text})]")
        console.print("[3. [yellow]View Character Stats[/yellow]]")
        console.print("[4. [red]Quit (and save)[/red]]")

        choice = input("\n>> ")

        if choice == '1':
            # Optional: Let user name the task
            task = input("Enter task name (or press Enter for 'Focus Session'): ")
            if not task.strip():
                task_name = "Focus Session"
            try:
                run_timer(WORK_DURATION, task_name)
                player.gain_xp(XP_PER_SESSION)
                
                # Random flavor text/loot drop chance
                # if random.random() > 0.7:
                #     loot = random.choice(["a Focus Amulet", "a Productivity Potion", "a Time Turner"])
                #     console.print(f"[bold gold1]Lucky Find! You found a {loot}![/bold gold1]")

                save_game(player)
            except KeyboardInterrupt:
                console.print("\n[red]Work session aborted! No XP gained.[/red]")
        
        elif choice == '2':
            if player.sessions_since_long_break >= 4:
                duration = LONG_BREAK_DURATION
                task_name = "Long Break"
                # Reset the counter
                player.sessions_since_long_break = 0
                save_game(player)
            else:
                duration = BREAK_DURATION
                task_name = "Short Break"
            try:
                run_timer(duration, task_name)
                console.print("[italic]You feel refreshed![/italic]")
            except KeyboardInterrupt:
                console.print("\n[red]Break ended early.[/red]")

        elif choice == '3':
            show_stats(player)

        elif choice == '4':
            save_game(player)
            console.print("[bold blue]Game saved. Goodbye![/bold blue]")
            break
        else:
            console.print("[red]Invalid choice. Please try again.[/red]")

if __name__ == "__main__":
    main()
