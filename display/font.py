class Font:
    def __init__(self, fontname: str) -> None:
        self.width = 8
        self.height = 14
        self.characters_supported = ord('~') - ord('!') + 1
        self.chars: dict[str, list[str]] = {}

        with open(fontname, 'r') as f:
            raw_font = f.read()
        lines = raw_font.splitlines()
        if len(lines) == 0:
            raise ValueError("Font file should not be empty")
        if any([len(line) != len(lines[0]) for line in lines]):
            raise ValueError("Every line of the font file"
                             "must have the same size")
        if len(lines[0]) != self.characters_supported * self.width:
            raise ValueError(f"The font file should support "
                             f"{self.characters_supported} characters "
                             f"{self.width} chars long and "
                             f"{self.height} chars tall")
        if len(lines) != self.height != 0:
            raise ValueError(f"The font file must have {self.height} lines")
        for i, char in enumerate(range(ord('!'), ord('~') + 1)):
            char_image: list[str] = []
            for line in lines:
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
