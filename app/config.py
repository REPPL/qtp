from dataclasses import dataclass, field


def highlighter():
    return {
        '<<g>>': (243, 235, 8, 155),
        '<<p>>': (8, 243, 15, 155),
        '<<n>>': (243, 8, 64, 155)
        }


def closing_char():
    return '/'


def closing_pattern():
    return {
        k[:2] + closing_char() + k[2:]: v for k, v in highlighter().items()}


@dataclass
class Highlighter:
    pattern: str = field(default=r'(<</?[npg]?>>)')
    colours: dict = field(default_factory=highlighter)
    closing_pattern: dict = field(default_factory=closing_pattern)
    closing_char: str = field(default_factory=closing_char)


@dataclass
class ProjectBaseClass:
    projects_folder: str = field(default='projects')
    import_extension: str = field(default='.txt')
    export_folder: str = field(default='plots')
    export_extension: str = field(default='.png')


@dataclass
class Screen:
    width: int = field(default=3024)
    height: int = field(default=1964)
    dpi: int = field(default=196)
    background_colour: tuple = field(
        default=(255, 255, 255, 255))


@dataclass
class Textbox:
    width: int
    height: int
    background_colour: str


@dataclass
class Font:
    name: str = field(default='app/LiberationMono-Regular.ttf')
    colour: tuple = field(default=(0, 0, 0, 255))
    size: int = field(default=12)


if __name__ == '__main__':
    pass
