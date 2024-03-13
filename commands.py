from colorama import Fore
from rich.console import Console
from rich.table import Table
import db
import game
import flights


# Function that checks whether the given command is found in the list of commands, and then returns the
# corresponding function
def command(text):
    game.clear_and_exit_check(text)
    if text in command_functions:
        return command_functions[text]
    else:
        return invalid_command


# Checks if the first word is "help" and if the second word is in the list of commands, and prints out the
# description for that specific command
def command_description(text):
    game.clear_and_exit_check(text)
    if text[0] == "help" and text[1] in help_list:
        print(help_list[text[1]])
    else:
        return invalid_command()


# Prints the description for every command
def print_helplist():
    print(f"\n{Fore.GREEN}Available commands:{Fore.RESET}"
          f"\n------------------------------")
    for line in help_list.values():
        print(line)


# Prints the instructions for the game
def print_instructions():
    instructions = [f"{Fore.CYAN}Around The World{Fore.RESET} is a text-based game where you have to fly "
                    "around the world in 20 days while trying to keep your expenses and CO2 emissions "
                    "as low as possible.",
                    "- The amount of days you have and your starting money is determined by the game difficulty.",
                    "- The game can be played alone or with friends (turn based).",
                    "- You will start on a random airport, and you will have to catch flights around the world until "
                    "you have circled around the globe.",
                    f"- Airports can be {Fore.CYAN}small{Fore.RESET}, {Fore.BLUE}medium{Fore.RESET} or "
                    f"{Fore.MAGENTA}large{Fore.RESET}. How far you can fly will depend on the size of the airport.",
                    f"- Typing {Fore.GREEN}'help'{Fore.RESET} (without apostrophes) will display a list of "
                    f"available commands and a short description for each one.",
                    f"- Typing {Fore.RED}'exit'{Fore.RESET} at any point will quit the game.",
                    "Good luck!"]
    for line in instructions:
        print(line)


# Prints the players' status in a table
def print_status():
    current_player = game.game_controller.get_current_player()
    current_airport = db.get_airport(current_player.location)
    airport_name = current_airport["name"]
    airport_size = flights.airport_type([current_airport])[0]
    print(current_player.origin_latitude, current_player.origin_longitude)
    start_airport = db.get_airport_by_cords(current_player.origin_latitude, current_player.origin_longitude)
    print(start_airport)
    # Creates a table, defines the column names, and displays player data on the second first row
    console = Console()
    table = Table(show_header=True, header_style="cyan")
    table.add_column("Name", style="white")
    table.add_column("Location", style="white")
    table.add_column("Airport size", style="white")
    table.add_column("Money", style="white")
    table.add_column("CO2 emissions", style="white")
    table.add_column("Distance traveled", style="white")
    table.add_column("Date", style="white")
    table.add_column("Halfway", style="white")
    table.add_column("Start airport", style="white")
    (table.add_row(f"{current_player.screen_name}", f"{airport_name}", f"{airport_size}",
                   f"{current_player.money:.2f}€", f"{current_player.co2_consumed:.2f}kg",
                   f"{current_player.distance_traveled}km",
                   f"{current_player.get_time()}",
                   f"{current_player.halfway_latitude, current_player.halfway_longitude}", f"{start_airport['name']}"))
    console.print(table)


# Uses function imported from flights.py that prints the flights' timetable
# Lets the player choose a flight, changing their current location to a new one and ending their turn
def fly():
    current_player = game.game_controller.get_current_player()
    current_airport = db.get_airport(current_player.location)
    airport_name = current_airport["name"]
    while True:
        print(f"Current location: {Fore.CYAN}{airport_name}{Fore.RESET}\n")
        flights.flight_timetable()
        try:
            selection = input(Fore.RESET + "\nSelect where you want to fly (1-16) (0 to cancel): ")
            game.clear_and_exit_check(selection)
            selection = int(selection)
            if 0 < selection < 17:
                chosen_flight = (flights.timed_flights[selection - 1])
                port = chosen_flight["airport"]
                current_player.fly(chosen_flight)
                print(f"\nWelcome to {Fore.CYAN}{port["name"]}{Fore.RESET}!")
                break
            elif selection == 0:
                return
            else:
                print(f"{Fore.RED}Invalid selection!{Fore.RESET}")
        except ValueError:
            print(f"{Fore.RED}Selection must be a number!\n{Fore.RESET}")
    return "break"


def invalid_command():
    print(f"{Fore.RED}Invalid command!{Fore.RESET}")


# Keeps asking the player for a command until they end the turn or quit the game
# Calls the 'command_description' function if the input has 2 words (for command-specific 'help' descriptions)
def run_commands():
    while True:
        command_input = input("\nEnter a command: ").lower()
        inputsplit = command_input.split()
        if len(inputsplit) == 2:
            command_description(inputsplit)
        else:
            answer = command(command_input)()
            # Ends the current player's turn after using the 'fly' command
            if answer == "break":
                break
    return True


# A dictionary of all commands and a short explanation for each one
help_list = {"help": f"{Fore.GREEN}Help{Fore.RESET} - Shows this list. Typing a command after "
                     f"'help' will give you the description for that specific command.",
             "instructions": f"{Fore.GREEN}Instructions{Fore.RESET} - Shows the instructions for playing the game.",
             "status": f"{Fore.GREEN}Status{Fore.RESET} - "
                       f"Shows your name, location, money, consumed CO2, days and time.",
             "fly": f"{Fore.GREEN}Fly{Fore.RESET} - Displays all available flights, and lets you pick one of them.",
             "exit": f"{Fore.GREEN}Exit{Fore.RESET} - Quits the game."}

# Contains all the commands that use functions (except "exit")
command_functions = {"help": print_helplist, "instructions": print_instructions, "status": print_status, "fly": fly}
