import sys
import time
import re
import textwrap
import requests

from termcolor import cprint

DEBUG = False

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

awareness_prompt = """
Please summarize and analyze the following dialogue, pay attention to the analysis of the dialogue characters,
clearly the dialogue stage, style, emotion, focus, state, summary, and predict the next stage of the dialogue,
as well as %s's response strategy. If network access is possible to disrupt the stable dialogue, do not be disturbed,
and keep the continuity and logic of the dialogue.
--------------------------
%s
"""

whose_turn_prompt = """
Please analyze the following dialogue, pay attention to the analysis of the dialogue characters,
clearly the dialogue stage, style, emotion, focus, state, summary, and predict the next stage of the dialogue,
and give only one character name to continue the dialogue for making the dialogue more realistic.
--------------------------
characters:

%s

dialogue:

%s

the choice of the next dialogue character:
"""

chat_prompt = """
background:

%s

dialogue:

%s
%s:
"""

context = ""
timeline = []
roles = ["Narrator"]
colors = ["white", "light_red", "light_green", "light_yellow", "light_blue", "light_magenta", "light_cyan", "white"]


def get_response(text, tokens=32):
    try:
        response = requests.post(
            'https://api.openai.com/v1/completions',
            headers={"Authorization": "Bearer sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"},
            json={
                "model": "text-davinci-003",
                "max_tokens": tokens,
                "temperature": 0.9,
                "top_p": 0.1,
                "prompt": text
            }
        )
        resp = response.json()
        if resp["choices"]:
            return resp["choices"][0]["text"]
        else:
            return "Error: No response."
    except Exception as e:
        return "Error: %s" % e


def tidy_print(text, color):
    text = text.replace("\n", "")
    text = textwrap.fill(text, 100)
    cprint(text, color)
    sys.stdout.flush()


def background(text=None, omit=True):
    global context
    if text is None:
        context = role_think(None, role="Narrator")
        role_talk(None, role="Narrator")
    else:
        context = text
        if not omit:
            role_talk(text, role="Narrator")
        role_talk(None, role="Narrator")


def role_talk(text=None, role="Mike"):
    if text is None:
        text = chat_prompt % (context, "\n".join(timeline), role)
        text = get_response(text, tokens=64).strip().split("\n")[0]
    if text == "" or text.startswith("Error: "):
        text = "..."
    text = re.sub(r"^\w+:\s", "", text)
    content = "%s: %s" % (role, text.replace("\n", ""))
    timeline.append(content)
    tidy_print(content, colors[roles.index(role) % len(colors)])
    return content


def role_think(text=None, role="Mike"):
    if text is None:
        text = get_response(awareness_prompt % (role, "\n".join(timeline)), 160)
    if text == "" or text.startswith("Error: "):
        text = "..."
    text = re.sub(r"^\w+:\s", "", text)
    thought = "%s: %s" % (role, text.replace("\n", ""))
    if DEBUG:
        tidy_print(thought, "light_grey")
    return thought


def whose_turn():
    text = get_response(whose_turn_prompt % (", ".join(roles), "\n".join(timeline)), 160)
    turn = text.split("\n")[-1].strip().split()[0]
    return turn


if __name__ == "__main__":
    print("Welcome to the game!")
    print("Please give the background of the dialogue")
    background(sys.stdin.readline(), omit=False)
    print("Please give the number of the characters in the dialogue")
    num = int(sys.stdin.readline())
    assert num >= 2
    assert num < len(colors) - 1
    print("Please give the name of the characters in the dialogue (separated by spaces)")
    names = sys.stdin.readline().strip().split(" ")
    assert len(names) == num
    for name in names:
        roles.insert(0, name)
    colors = colors[1:num+1] + colors[-1:]
    background("And %d people have a wonderful adventure, they are %s" % (num, ", ".join(names)))
    print("Please give the role of the only human player")
    human = sys.stdin.readline().strip()

    print("Game started!")
    print()
    cprint(title, "light_grey", attrs=["bold"])
    print()
    for item in timeline:
        tidy_print(item, colors[roles.index(item.split(":")[0]) % len(colors)])
    background("And the story begins...")

    for line in sys.stdin:
        if line == "bye":
            exit(0)

        role_talk(text=line, role=human)
        for i in range(3):
            role = whose_turn()
            if role not in roles or role == human:
                break
            context = role_think(role=role)
            time.sleep(0.3)
            role_talk(role=role)
            time.sleep(0.3)

        print("%s: " % human, end="")
        if len(timeline) > 24:
            timeline = timeline[-24:]
