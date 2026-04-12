
class Font:
    def __init__(self, fontname: str) -> None:
        self.width = 8
        self.height = 14
        self.chars: dict[str, list[str]] = {}
        with open(fontname, 'r') as f:
            raw_font = f.read()
        for i, char in enumerate(range(ord('!'), ord('~') + 1)):
            char_image: list[str] = []
            for line in raw_font.splitlines():
                tmp_line: str = ''
                for pixel in line[(i * self.width):((i + 1) * self.width)]:
                    tmp_line += pixel
                char_image.append(tmp_line)
            self.chars.update({chr(char): char_image})

    def __getitem__(self, index: str) -> list[str]:
        return self.chars[index]

    def __str__(self, char: str) -> str:
        s: str = ''
        for char in self.chars:
            for line in char:
                s += line + '\n'
        return s

    def __repr__(self) -> str:
        s: str = '{\n'
        for char in self.chars:
            for line in char:
                s += repr(line) + '\n'
        s += '}'
        return s
