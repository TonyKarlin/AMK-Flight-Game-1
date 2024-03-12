from colorama import Fore
import flights
import time
import sys
from rich.console import Console
from rich.table import Table
import os


# Function that checks whether the given command is found in the list of commands, and then returns the
# corresponding function
def command(text):
    clear_and_exit_check(text)
    if text in command_functions:
        return command_functions[text]
    else:
        return invalid_command


# Checks if the player has typed "exit" and if so, exits the program
# Also clears the console
def clear_and_exit_check(text):
    os.system('cls' if os.name == 'nt' else 'clear')
    text = str(text)
    if text.lower() == "exit":
        exit_msg = f"{Fore.RED}Quitting the game...{Fore.RESET}"
        for letter in exit_msg:
            print(letter, end="")
            time.sleep(0.03)
            sys.stdout.flush()
        exit()


# Checks if the first word is "help" and if the second word is in the list of commands, and prints out the
# description for that specific command
def command_description(text):
    clear_and_exit_check(text)
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
                    f"around the world in 20 days (or 10, depending on the chosen difficulty),",
                    f"while trying to keep your expenses and CO2 emissions as low as possible.",
                    "You will start on a random airport, and you will have to catch flights around the world until "
                    "you have circled around the globe.",
                    "Typing 'help' (without apostrophes) will display a list of available commands "
                    "and a short description for each one.", "Typing 'exit' at any point will quit the game.",
                    "Good luck!"]
    for line in instructions:
        print(line)


# Prints the players' status in a table
def print_status():
    console = Console()
    table = Table(show_header=True, header_style="cyan")
    table.add_column("Name", style="white")
    table.add_column("Location", style="white")
    table.add_column("Money", style="white")
    table.add_column("CO2 emissions", style="white")
    table.add_column("Day", style="white")
    table.add_row(f"{status[1]}", f"{status[2]}", f"{status[3]}", f"{status[4]}", f"{status[5]}")
    console.print(table)


# Uses function imported from flights.py that prints the flights' timetable
# Lets the player choose a flight, changing their current location to a new one)
def fly():
    flights.flight_timetable()
    try:
        selection = input(Fore.RESET + "\nSelect where you want to fly (1-16): ")
        clear_and_exit_check(selection)
        selection = int(selection)
        if 0 < selection < 17:
            chosen_flight = (flights.timed_flights[selection - 1])
            port = chosen_flight["airport"]
            new_coordinates = (port["latitude_deg"], port["longitude_deg"])
            status[2] = port["name"]
            flying_msg = "Flying to airport..."
            for letter in flying_msg:
                print(letter, end="")
                time.sleep(0.1)
                sys.stdout.flush()
            print(f"\nWelcome to {port["name"]}!")
        else:
            print("Invalid selection!")
    except ValueError:
        print("Selection must be a number!")


def invalid_command():
    print("Invalid command!")


# Keeps asking the player for a command until they exit
# Calls the 'command_description' function if the input has 2 words (for command-specific 'help' descriptions)
def run_commands():
    while True:
        command_input = input("\nEnter a command: ").lower()
        inputsplit = command_input.split()
        if len(inputsplit) == 2:
            command_description(inputsplit)
        else:
            command(command_input)()


# A dictionary of all commands and a short explanation for each one
help_list = {"help": f"{Fore.GREEN}Help{Fore.RESET} - Shows this list. Typing a command after "
                     f"'help' will give you the description for that specific command.",
             "instructions": f"{Fore.GREEN}Instructions{Fore.RESET} - Shows the instructions for playing the game",
             "status": f"{Fore.GREEN}Status{Fore.RESET} - "
                       f"Shows your name, location, money, consumed CO2, days and time.",
             "fly": f"{Fore.GREEN}Fly{Fore.RESET} - Displays all available flights, and lets you pick one of them.",
             "exit": f"{Fore.GREEN}Exit{Fore.RESET} - Quits the game."}

# Player stats placeholder
status = {1: "Ronald McDonald", 2: "Starting airport", 3: 20000,
          4: 0, 5: 1}

# Contains all the commands that use functions (except "exit")
command_functions = {"help": print_helplist, "instructions": print_instructions, "status": print_status, "fly": fly}

if __name__ == "__main__":
    run_commands()
