import sys
import os
import os.path as path

import wndrng.term as term

key = None


def setup_key():
    global key
    home = os.environ["HOME"]
    k_file = path.join(home, ".openai")
    if path.exists(k_file):
        with open(k_file) as k:
            key = k.readline().strip()

    if key is None or key == "":
        term.print_hint("Welcome to setup the game!")
        term.print_hint("Please give the key for your OpenAI API access")
        key = sys.stdin.readline().strip()
        with open(k_file, mode="w") as k:
            k.write(key)
