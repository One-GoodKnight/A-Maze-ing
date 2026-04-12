
class Font:
    def __init__(self, fontname: str) -> None:
        self.width = 8
        self.height = 14
        self.letters: dict[str, list[str]] = {}
        with open(fontname, 'r') as f:
            raw_font = f.read()
        for i, letter in enumerate(range(ord('!'), ord('~') + 1)):
            char_image: list[str] = []
            for line in raw_font.splitlines():
                tmp_line: str = ''
                for char in line[(i * self.width):((i + 1) * self.width)]:
                    tmp_line += char
                char_image.append(tmp_line)
            self.letters.update({chr(letter): char_image})

    def __getitem__(self, index: str) -> list[str]:
        return self.letters[index]

    def __str__(self, char: str) -> str:
        s: str = ''
        for letter in self.letters:
            for line in letter:
                s += line + '\n'
        return s

    def __repr__(self) -> str:
        s: str = '{\n'
        for letter in self.letters:
            for line in letter:
                s += repr(line) + '\n'
        s += '}'
        return s
