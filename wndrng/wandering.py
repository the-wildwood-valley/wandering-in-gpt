"""
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

import re
import random
import sys

import wndrng.api as api
import wndrng.i18n as i18n
import wndrng.term as term

DEBUG = False

context = None
genre = None
people = None
roles = None
human = None
step = None
timeline = None


def init():
    global context, genre, people, roles, human, step, timeline
    context = ""
    genre = "science fiction"
    people = [i18n.default("Narrator")]
    roles = [i18n.default("An auxiliary role who does not participate in the story itself")]
    human = None
    step = 0
    timeline = [
    ]


def timeline_append(entry):
    global step, timeline
    timeline.append(entry)
    step = step + 1
    if len(timeline) > 24:
        timeline = timeline[-24:]


def background(text=None, omit=True, quotation_check=True):
    global context
    if text is None:
        context = role_think(None, role=i18n.default("Narrator"))
        role_talk(None, role=i18n.default("Narrator"))
    else:
        context = text
        if not omit:
            role_talk(text, role=i18n.default("Narrator"), quotation_check=quotation_check)
            if random.random() > 0.2:
                if step > 5:
                    role = whose_turn()
                    if role and role != i18n.default("Narrator"):
                        role_talk(None, role=role)
                else:
                    role = i18n.default("Narrator")
                    role_talk(None, role=role)


def role_talk(text, role, quotation_check=True):
    assert(role is not None)

    if text is None or text == "":
        text = i18n.prompt("chat") % (context, "\n".join(timeline), role)
        text = api.get_response(text, max_tokens=i18n.setting("talk_tokens_length")).strip().split("\n")[0]
        if text == "" or text.startswith("Error: "):
            text = "..."

    if not quotation_check or not handle_quotation(text):
        text = "%s: %s" % (role, text)
        timeline_append(text)
        term.tidy_print(text, term.colors[people.index(role) % len(term.colors)])
        return text

    return text


def role_think(text=None, role=None):
    assert(role is not None)

    if text is None:
        text = api.get_response(i18n.prompt("awareness") % (role, "\n".join(timeline)),
                                max_tokens=i18n.setting("awareness_tokens_length"))
        if text == "" or text.startswith("Error: "):
            text = "..."

    text = re.sub(r"^\w+:\s", "", text)
    thought = "%s: %s" % (role, text.replace("\n", ""))
    if DEBUG:
        term.tidy_print(thought, "red")

    return thought


def whose_turn():
    whose_turn_prompt = i18n.prompt("whose_turn") % (", ".join(people), "\n".join(timeline))
    text = api.get_response(whose_turn_prompt, max_tokens=i18n.setting("whose_turn_tokens_length"))
    turn = text.split("\n")[-1].strip()
    if turn in people:
        return turn
    else:
        return None


def match_person(text, matcher, seperator, ender):
    if matcher in text:
        for person in people:
            if text[:len(person)] == person:
                segments = text.split(seperator)
                background(text=segments[0], omit=False, quotation_check=False)
                segments = segments[1].split(ender)
                role_talk(text=segments[0].strip(" \"“”"), role=person, quotation_check=False)
                if len(segments) > 1 and segments[1]:
                    background(text=segments[1], omit=False, quotation_check=False)
                return True
    return False


def handle_quotation(text):
    return match_person(text, "：“", "：“", "”") or match_person(text, ": “", ": “", "”") or \
        match_person(text, ": \"", ": \"", "\"") or match_person(text, ": ", ": ", "~")


def game_loop():
    global context, timeline
    print()
    term.cprint("%s:" % human, "light_grey", attrs=["bold"])
    for line in sys.stdin:
        line = line.strip()
        if line == "bye":
            exit(0)

        role_talk(text=line, role=human)
        for i in range(3):
            role = whose_turn()
            if role not in people or role == human:
                break
            context = role_think(role=role)
            role_talk(None, role=role)

        print()
        term.cprint("%s:" % human, "light_grey", attrs=["bold"])
