from colorama import Fore
import commands
import intro
from rich.console import Console
from rich.table import Table


def leaderboard_table():
    console = Console()
    leaderboards = Table(title="Leaderboards", title_style="gold3", show_header=True, header_style="red1")
    leaderboards.add_column("Player", justify="center")
    leaderboards.add_column("Score", justify="center")
    console.print(leaderboards)
    return leaderboards


def display_menu():
    print(f"\n{Fore.CYAN}Welcome to your journey AROUND THE WORLD!{Fore.RESET}\n")

    print(f"1. Start your journey!")
    print(f"2. Leaderboards")
    print(f"{Fore.GREEN}3. Instructions / Help{Fore.RESET}")
    print(f"{Fore.RED}4. Exit{Fore.RESET}")


def menu_choice():
    print()
    menu_options = input("Option: ")
    commands.clear_and_exit_check(menu_options)

    if len(menu_options) > 0:
        try:
            menu_options = int(menu_options)

        except ValueError:
            print(f"{menu_options} is not a valid option, please try again")

        else:
            if 1 <= menu_options <= 4:
                return menu_options

            else:
                print(f"Option doesn't exist")

    else:
        print("Empty input is not a valid option, please try again!")
    return menu_options


def display_win_screen():
    print(f"\n{Fore.LIGHTBLUE_EX}CONGRATULATIONS! YOU'VE COMPLETED YOUR JOURNEY!{Fore.RESET}\n")
    commands.print_status()
    print()
    leaderboards = leaderboard_table()


def display_loss_screen():
    print(f"\n{Fore.LIGHTRED_EX}Unfortunately you've ran out of money and your journey has ended.{Fore.RESET}\n")
    commands.print_status()


game_over = False

while not game_over:
    display_menu()
    options = menu_choice()

    if options == 1:
        intro = intro.game_intro()
        commands.run_commands()

    elif options == 2:
        show_leaderboards = leaderboard_table()
        next_screen = str(input(f"{Fore.BLUE}\nInput anything to continue back to main menu: {Fore.RESET}"))

    elif options == 3:
        commands.print_instructions()
        commands.print_helplist()

    elif options == 4:
        print(f"\n{Fore.RED}Quitting the game...{Fore.RESET}")
        game_over = True

        if game_over:
            # display_win_screen()
            display_loss_screen()

            while True:
                back_to_menu = input(f"\nWould you like to continue back to main menu? (Y/N): ")
                if back_to_menu.lower() == "y" or back_to_menu.lower() == "yes":
                    commands.clear_and_exit_check(0)
                    game_over = False
                    break
                elif back_to_menu.lower() == "n" or back_to_menu.lower() == "no":
                    commands.clear_and_exit_check(0)
                    print(f"\n{Fore.RED}Quitting the game...{Fore.RESET}")
                    game_over = True
                    break
                else:
                    commands.clear_and_exit_check(0)
                    print("Invalid input, please enter 'Y' or 'N'!")


