from colorama import init, Fore
import random

init(autoreset=True)

DISTINCT_COLOURS = [
    Fore.RED,
    Fore.GREEN,
    Fore.YELLOW,
    Fore.BLUE,
    Fore.MAGENTA,
    Fore.CYAN,
    Fore.BLACK,
]

COLOUR_VARIANTS = {
    Fore.RED: [Fore.LIGHTRED_EX],
    Fore.GREEN: [Fore.LIGHTGREEN_EX],
    Fore.YELLOW: [Fore.LIGHTYELLOW_EX],
    Fore.BLUE: [Fore.LIGHTBLUE_EX],
    Fore.MAGENTA: [Fore.LIGHTMAGENTA_EX],
    Fore.CYAN: [Fore.LIGHTCYAN_EX],
    Fore.BLACK: [Fore.LIGHTBLACK_EX],
}

last_used_colour = None

def get_next_colour():
    global last_used_colour
    
    # If no color has been used yet, pick a random one
    if last_used_colour is None:
        last_used_colour = random.choice(DISTINCT_COLOURS)
        return last_used_colour
    
    excluded_colours = [last_used_colour] + COLOUR_VARIANTS.get(last_used_colour, [])
    available_colours = [colour for colour in DISTINCT_COLOURS if colour not in excluded_colours]
    
    # If no colors are left (unlikely), reset and pick a random one
    if not available_colours:
        last_used_colour = random.choice(DISTINCT_COLOURS)
        return last_used_colour
    
    next_colour = random.choice(available_colours)
    last_used_colour = next_colour
    return next_colour