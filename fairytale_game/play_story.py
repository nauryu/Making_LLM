"""Interactive fairy tale using the `ollama` language model."""
from enum import Enum, auto
import ollama


def load_story(path: str) -> str:
    """Return the base fairy tale text."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


class Scene(Enum):
    INTRO = auto()
    FOREST = auto()
    DRAGON = auto()
    END = auto()


def generate_reply(context: str, user_input: str) -> str:
    """Send the user input to the model and return the generated reply."""
    messages = [
        {"role": "system", "content": context},
        {"role": "user", "content": user_input},
    ]
    response = ollama.chat(model="llama2", messages=messages)
    return response["message"]["content"].strip()


def main() -> None:
    story_text = load_story("data/fairy_tale.txt")
    print(story_text)
    name = input("Enter your name, brave hero: ")
    context = (
        f"You are {name}, the main character in the following fairy tale. "
        "Respond with in-story dialogue that continues the adventure."
    )

    scene = Scene.INTRO
    while scene is not Scene.END:
        if scene is Scene.INTRO:
            user_in = input("How do you respond to the call to adventure? ")
            print(generate_reply(context, user_in))
            scene = Scene.FOREST
        elif scene is Scene.FOREST:
            user_in = input("You enter a dark forest. What do you do? ")
            print(generate_reply(context, user_in))
            scene = Scene.DRAGON
        elif scene is Scene.DRAGON:
            user_in = input("A dragon appears! What's your move? ")
            print(generate_reply(context, user_in))
            scene = Scene.END

    print("The story ends. Thank you for playing!")


if __name__ == "__main__":
    main()
