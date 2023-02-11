import sys

from wndrng.i18n.hints import hints
from wndrng.i18n.people import defaults
from wndrng.i18n.prompts import prompts
from wndrng.i18n.settings import settings

langs = [
    "en", "zh_S", "zh_T"
]
lang = "en"


def hint(text):
    return hints[text][lang]


def prompt(a_key):
    return prompts[a_key][lang]


def default(a_key):
    return defaults[a_key][lang]


def setting(a_key):
    return settings[a_key][lang]


def setup_i18n():
    global lang
    print("Please select your language:")
    print("1. English")
    print("2. 简体中文")
    print("3. 繁體中文")
    choice = int(sys.stdin.readline().strip()) - 1
    lang = langs[choice]
