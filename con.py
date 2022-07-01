import re
from collections import Counter


def load_file(filename: str) -> dict:
    with open(filename, "r") as f:
        lines = f.read()
    words = re.findall(r"\w+", lines.lower())
    return dict(Counter(words))


words = []

while True:
    user_input = input("введите команду:")
    if user_input.startswith("load"):
        filename = user_input.split()[-1]
        words = load_file(filename)
    elif user_input.startswith("wordcount"):
        if len(words) == 0:
            print("сначала загрузите файл")
            continue
        word = user_input.split()[-1]
        if word not in words:
            count = 0
        else:
            count = words[word]
        print(f"число слов '{word}' равно {count}")
    elif user_input.startswith("clear-memory"):
        words = []
    else:
        print("некоректная команда")
