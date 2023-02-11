import sys
import os
import os.path as path
import re
import random
import textwrap

import requests

from termcolor import cprint
from wndrng.i18n.hints import hints
from wndrng.i18n.people import defaults
from wndrng.i18n.prompts import prompts
from wndrng.i18n.settings import settings


DEBUG = False

langs = ["en", "zh_S", "zh_T"]
print("Please select your language:")
print("1. English")
print("2. 简体中文")
print("3. 繁體中文")
choice = int(sys.stdin.readline().strip()) - 1
lang = langs[choice]


def hint(text):
    print()
    ltext = hints[text][lang]
    cprint(ltext, "white")
    sys.stdout.flush()


def prompt(key):
    return prompts[key][lang]


def default(key):
    return defaults[key][lang]


def setting(key):
    return settings[key][lang]


key = None
if key is None:
    home = os.environ["HOME"]
    kfile = path.join(home, ".openai")
    if path.exists(kfile):
        with open(kfile) as k:
            key = k.readline().strip()
if key is None:
    hint("Welcome to setup the game!")
    hint("Please give the key for your openai aip access")
    key = sys.stdin.readline().strip()
    with open(kfile, mode="w") as k:
        k.write(key)
    print()


title = """
░██╗░░░░░░░██╗░█████╗░███╗░░██╗██████╗░███████╗██████╗░██╗███╗░░██╗░██████╗░  ██╗███╗░░██╗
░██║░░██╗░░██║██╔══██╗████╗░██║██╔══██╗██╔════╝██╔══██╗██║████╗░██║██╔════╝░  ██║████╗░██║
░╚██╗████╗██╔╝███████║██╔██╗██║██║░░██║█████╗░░██████╔╝██║██╔██╗██║██║░░██╗░  ██║██╔██╗██║
░░████╔═████║░██╔══██║██║╚████║██║░░██║██╔══╝░░██╔══██╗██║██║╚████║██║░░╚██╗  ██║██║╚████║
░░╚██╔╝░╚██╔╝░██║░░██║██║░╚███║██████╔╝███████╗██║░░██║██║██║░╚███║╚██████╔╝  ██║██║░╚███║
░░░╚═╝░░░╚═╝░░╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░╚══════╝╚═╝░░╚═╝╚═╝╚═╝░░╚══╝░╚═════╝░  ╚═╝╚═╝░░╚══╝

░██████╗░██████╗░████████╗
██╔════╝░██╔══██╗╚══██╔══╝
██║░░██╗░██████╔╝░░░██║░░░
██║░░╚██╗██╔═══╝░░░░██║░░░
╚██████╔╝██║░░░░░░░░██║░░░
░╚═════╝░╚═╝░░░░░░░░╚═╝░░░
"""


context = ""
genre = "science fiction"
people = [default("Narrator")]
roles = [default("An auxiliary role who does not participate in the story itself")]
colors = ["light_grey", "light_red", "light_green", "light_yellow", "light_blue", "light_magenta", "light_cyan", "light_grey"]
timeline = []


def get_response(text, max_tokens=32):
    try:
        response = requests.post(
            'https://api.openai.com/v1/completions',
            headers={"Authorization": "Bearer %s" % key},
            json={
                "model": "text-davinci-003",
                "max_tokens": max_tokens,
                "temperature": 0.9,
                "top_p": 0.2,
                "n": 3,
                "prompt": text,
            }
        )
        resp = response.json()
        if resp["choices"]:
            idx = int(random.random() * 3 + 0.5)
            return resp["choices"][idx]["text"]
        else:
            return "Error: No response."
    except Exception as e:
        return "Error: %s" % e


def tidy_print(text, color):
    text = text.replace("\n", "")
    text = textwrap.fill(text, 100)
    print()
    cprint(text, color)
    sys.stdout.flush()


def background(text=None, omit=True):
    global context
    if text is None:
        context = role_think(None, role=default("Narrator"))
        role_talk(None, role=default("Narrator"))
    else:
        context = text
        if not omit:
            role_talk(text, role=default("Narrator"))
        role_talk(None, role=default("Narrator"))


def role_talk(text=None, role="Mike"):
    if text is None:
        text = prompt("chat") % (context, "\n".join(timeline), role)
        text = get_response(text, max_tokens=setting("talk_tokens_length")).strip().split("\n")[0]
    if text == "" or text.startswith("Error: "):
        text = "..."
    text = re.sub(r"^\w+:\s", "", text)
    content = "%s: %s" % (role, text.replace("\n", ""))
    timeline.append(content)
    tidy_print(content, colors[people.index(role) % len(colors)])
    return content


def role_think(text=None, role="Mike"):
    if text is None:
        text = get_response(prompt("awareness") % (role, "\n".join(timeline)), setting("awareness_tokens_length"))
    if text == "" or text.startswith("Error: "):
        text = "..."
    text = re.sub(r"^\w+:\s", "", text)
    thought = "%s: %s" % (role, text.replace("\n", ""))
    if DEBUG:
        tidy_print(thought, "light_grey")
    return thought


def whose_turn():
    text = get_response(prompt("whose_turn") % (", ".join(people), "\n".join(timeline)), setting("whose_turn_tokens_length"))
    turn = text.split("\n")[-1].strip()
    return turn
