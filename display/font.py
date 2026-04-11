from .image import Image
from constants import BLACK


class Letter:
    def __init__(self, letter: list[str]) -> None:
        self.letter: list[str] = letter

    def __getitem__(self, index: int) -> str:
        return self.letter[index]

    def __str__(self) -> str:
        s: str = ''
        for line in self.letter:
            s += line + '\n'
        return s

    def __repr__(self) -> str:
        s: str = ''
        for line in self.letter:
            s += repr(line) + '\n'
        return s


class Font:
    def __init__(self, fontname: str) -> None:
        self.width = 8
        self.height = 14
        self.letters: dict[str, Letter] = {}
        with open(fontname, 'r') as f:
            raw_font = f.read()
        for i, letter in enumerate(range(ord('!'), ord('~') + 1)):
            char_image: list[str] = []
            for line in raw_font.splitlines():
                tmp_line: str = ''
                for char in line[(i * self.width):((i + 1) * self.width)]:
                    tmp_line += char
                char_image.append(tmp_line)
            self.letters.update({chr(letter): Letter(char_image)})

    def __getitem__(self, index: str) -> Letter:
        return self.letters[index]

    def print_char(self, image: Image, x: int, y: int,
                   char: str, **kwargs) -> None:
        color = image.endian_color(kwargs.get('color', BLACK))
        bg_color = image.endian_color(kwargs.get('bg_color', None))
        size = kwargs.get('size', 1)
        if size <= 0:
            size = 1
        letter = self.letters.get(char)
        if letter is None:
            return
        for i in range(self.width):
            for j in range(self.height):
                x_coord = x + i * image.bytes_pp
                y_coord = y + j
                if (y_coord >= 0 and y_coord <= image.height and
                        x_coord >= 0 and x_coord <= image.width):
                    if letter[j][i] == '#':
                        if color is not None:
                            image.data[
                                y_coord,
                                x_coord: x_coord + image.bytes_pp
                            ] = color
                    else:
                        if bg_color is not None:
                            image.data[
                                y_coord,
                                x_coord: x_coord + image.bytes_pp
                            ] = bg_color

    def print(self, image: Image, x: int, y: int, text: str, **kwargs) -> None:
        if not text.isascii():
            raise ValueError(f"Invalid text: '{text}' "
                             "contains non ASCII characters")
        color = kwargs.get('color', BLACK)
        bg_color = kwargs.get('bg_color', None)
        size = kwargs.get('size', 1)
        if size <= 0:
            size = 1
        if x == -1:
            x = (image.width // 2) - (len(text) * size // 2)
        if y == -1:
            y = image.height // 2 - (self.height * size // 2)
        for i, char in enumerate(text):
            offset = i * image.bytes_pp * self.width * size
            if char == ' ' and bg_color is not None:
                image.draw_rect(
                    (x + offset, y),
                    (x + offset + self.width * size, y + self.height * size),
                    bg_color
                )
            else:
                self.print_char(image, x + offset, y, char,
                                color=color, bg_color=bg_color, size=size)
