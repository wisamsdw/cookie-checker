"""Cookie Quest: a tiny terminal game.

Run:
    python checker.py
"""

from __future__ import annotations

import argparse
import random
import textwrap


INTRO = """
Willkommen bei Cookie Quest!
Du bist im Cookie-Labor und suchst den perfekten Keks.
Sammle Zutaten, vermeide Pannen und knacke das Rezept.
"""

ROOMS = {
    "Labor": {
        "desc": "Du stehst im Labor. Es riecht nach Vanille.",
        "items": ["Zucker"],
        "next": ["Speisekammer", "Ofenraum"],
    },
    "Speisekammer": {
        "desc": "Regale voller Zutaten. Etwas knistert.",
        "items": ["Mehl", "Schoko"],
        "next": ["Labor"],
    },
    "Ofenraum": {
        "desc": "Der Ofen glüht. Vorsicht vor Überhitze!",
        "items": ["Butter"],
        "next": ["Labor"],
    },
}

RECIPE = {"Mehl", "Zucker", "Butter", "Schoko"}


def wrap(text: str) -> str:
    return "\n".join(textwrap.wrap(text, width=72))


def choose(options: list[str], input_fn: callable) -> str:
    while True:
        choice = input_fn("Deine Wahl: ").strip()
        for option in options:
            if choice.lower() == option.lower():
                return option
        print("Bitte wähle eine der Optionen:", ", ".join(options))


def show_status(room: str, inventory: set[str]) -> None:
    print("\n" + "=" * 72)
    print(f"Ort: {room}")
    print(ROOMS[room]["desc"])
    items = ROOMS[room]["items"]
    if items:
        print("Du siehst:", ", ".join(items))
    else:
        print("Hier liegt nichts mehr.")
    print("Inventar:", ", ".join(sorted(inventory)) if inventory else "(leer)")


def handle_event(inventory: set[str], rng: random.Random) -> bool:
    roll = rng.randint(1, 6)
    if roll == 1:
        print(wrap("Eine Mehlwolke! Du niest und verlierst eine Zutat."))
        if inventory:
            lost = rng.choice(list(inventory))
            inventory.remove(lost)
            print(f"Verloren: {lost}")
        return True
    if roll == 6:
        print(wrap("Du findest ein geheimes Rezept-Notizblatt. Bonus!"))
        return True
    return False


def bake(inventory: set[str]) -> bool:
    missing = sorted(RECIPE - inventory)
    if missing:
        print("Dir fehlen noch:", ", ".join(missing))
        return False
    print(wrap("Du mischst alles zusammen und schiebst das Blech in den Ofen..."))
    print("Der Duft ist perfekt. Du hast den ultimativen Keks gebacken!")
    return True


def play_game(
    *,
    player_name: str,
    input_fn: callable,
    rng: random.Random,
) -> None:
    print(wrap(INTRO))
    print(f"Viel Erfolg, {player_name}!")

    room = "Labor"
    inventory: set[str] = set()

    while True:
        show_status(room, inventory)
        handle_event(inventory, rng)
        print("\nAktionen: nehmen, gehen, backen, beenden")
        action = choose(["nehmen", "gehen", "backen", "beenden"], input_fn)

        if action == "beenden":
            print("Bis zum nächsten Keks!")
            break
        if action == "nehmen":
            items = ROOMS[room]["items"]
            if not items:
                print("Nichts zu nehmen.")
                continue
            print("Was nimmst du?", ", ".join(items))
            item = choose(items, input_fn)
            items.remove(item)
            inventory.add(item)
            print(f"{item} eingepackt.")
            continue
        if action == "gehen":
            destinations = ROOMS[room]["next"]
            print("Wohin?", ", ".join(destinations))
            room = choose(destinations, input_fn)
            continue
        if action == "backen":
            if bake(inventory):
                break


def demo_input(actions: list[str]) -> callable:
    def _input(prompt: str) -> str:
        if actions:
            choice = actions.pop(0)
            print(f"{prompt}{choice}")
            return choice
        print(f"{prompt}beenden")
        return "beenden"

    return _input


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cookie Quest terminal game.")
    parser.add_argument("--demo", action="store_true", help="Run a scripted demo.")
    parser.add_argument("--seed", type=int, default=None, help="Random seed.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rng = random.Random(args.seed)
    if args.demo:
        input_fn = demo_input(
            [
                "nehmen",
                "Zucker",
                "gehen",
                "Speisekammer",
                "nehmen",
                "Mehl",
                "nehmen",
                "Schoko",
                "gehen",
                "Labor",
                "gehen",
                "Ofenraum",
                "nehmen",
                "Butter",
                "backen",
            ]
        )
        play_game(player_name="Demo", input_fn=input_fn, rng=rng)
        return

    name = input("Wie heißt du, Chef-Bäcker:in? ").strip() or "Bäcker:in"
    play_game(player_name=name, input_fn=input, rng=rng)


if __name__ == "__main__":
    main()
