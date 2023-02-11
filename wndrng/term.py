import sys

import wndrng.i18n as i18n
import textwrap

from termcolor import cprint

colors = [
    "light_grey", "light_red", "light_green", "light_yellow",
    "light_blue", "light_magenta", "light_cyan", "light_grey"
]


def tidy_print(text, color):
    text = text.replace("\n", "")
    text = textwrap.fill(text, 100)
    print()
    cprint(text, color)
    sys.stdout.flush()


def print_hint(a_key):
    print()
    cprint(i18n.hint(a_key), "white")
    sys.stdout.flush()
