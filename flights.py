from db import get_some_airports
import random
from colorama import Fore


def flights():
    airports = get_some_airports()
    return


def times_of_the_flights():  # Arpoo satunnaisia aikoja lennoille ja lisää ne listaan.
    flight_times = []
    for i in range(16):
        random_hours = random.randint(00, 24)
        random_minutes = random.randint(00, 59)
        flight_times.append((random_hours, random_minutes))
        flight_times.sort()
    return flight_times


print(f"{Fore.YELLOW}DEPARTURES")
print(f"Options     Time     Destination         Cost       Direction       Range")

flight_times = times_of_the_flights()
for i, (hours, minutes) in enumerate(flight_times, start=1):
    # Etsii listalta lähtevien lentojen tietoja ja tulostaa ne allekkain.

    print(f"{i:02d}         {hours:02d}:{minutes:02d}     Destination{i:02d}       Cost{i:02d}     "
          f"Direction{i:02d}     Range{i:02d}")
