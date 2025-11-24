#!/bin/python

import pathlib
import random
import shutil

TEMPLATE = """\
<!DOCTYPE html>
<html lang="pt-br">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Amigo Secreto</title>
    <style>
body {{
	display: flex;
	align-items: center;
	justify-content: center;
	height: 100vh;
	font-size: 4em;
	font-family: sans-serif;
}}
    </style>
  </head>
  <body style="display: flex; align-items: center; justify-content: center;">
    <p>
      Olá, {name}!
      <br/>
      Seu amigo secreto é {friend}!
    </p>
  </body>
</html>
"""

NAMES = [
    "Jonas",
    "Rafaela",
    "Márcio",
    "Lene",
    "Camila",
    "Mauro",
    "Vera",
    "Anna",
    "João",
    "Gustavo",
    "Natália",
    "Letícia",
    "Rafael",
    "Sofia",
    "Mila",
    "Julia",
]

FORBIDDEN_PAIRS = (
    ("Natália", "Sofia"),
    ("Gustavo", "Sofia"),
    ("Natália", "Julia"),
    ("Gustavo", "Julia"),
    ("Letícia", "Mila"),
    ("Rafael", "Mila"),
)

FORBIDDEN_PAIRS = set(tuple(sorted(p)) for p in FORBIDDEN_PAIRS)


class Shuffler:
    def __init__(self, names, forbidden_pairs):
        self.__names = list(names)
        self.__forbidden_pairs = set(tuple(sorted(p)) for p in forbidden_pairs)

        self.__validate_input()
        self.__shuffle_names()

    def __validate_input(self):
        all_names = set()
        for name in self.__names:
            if name in all_names:
                raise Exception(f"duplicate name: {name}")
            all_names.add(name)

        names_from_forbidden = {
            name
            for pair in self.__forbidden_pairs
            for name in pair
        }
        missing_names = names_from_forbidden - all_names
        if missing_names:
            raise Exception(f"names in forbidden pairs are missing in list of names: {missing_names}")

    def __shuffle_names(self):
        indices = list(range(len(self.__names)))
        while True:
            random.shuffle(indices)
            for i, j in enumerate(indices):
                if i == j:
                    break

                a, b = tuple(sorted((self.__names[i], self.__names[j])))
                if (a, b) in self.__forbidden_pairs:
                    break
            else:
                break

        self.__indices = indices

    def dump(self, build_dir):
        try:
            shutil.rmtree(build_dir)
        except FileNotFoundError:
            pass

        build_dir.mkdir()

        for i, j in enumerate(self.__indices):
            a, b = self.__names[i], self.__names[j]
            key = "".join(chr(random.randrange(ord('a'), ord('z') + 1)) for _ in range(6))
            (build_dir / f"{key}.html").write_text(TEMPLATE.format(name=a, friend=b))
            print(a, f"https://guludo.github.io/amigo-secreto/build/{key}.html")


if __name__ == "__main__":
    build_dir = pathlib.Path(__file__).parent / "build"
    Shuffler(NAMES, FORBIDDEN_PAIRS).dump(build_dir)
