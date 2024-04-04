from dataclasses import dataclass, field


@dataclass
class Screen:
    width: int = field(default=3024)
    height: int = field(default=1964)
    dpi: int = field(default=196)
    background_colour: str = field(default='white')


@dataclass
class Font:
    name: str = field(default='app/LiberationMono-Regular.ttf')
    colour: str = field(default='black')
    highlight: str = field(default='yellow')
    size: int = field(default=12)


@dataclass
class Highlight:
    positive: str = field(default='#90EE90')
    negative: str = field(default='#FFDAB9')
    generic: str = field(default='#FFFF00')


@dataclass
class Textbox:
    width: int
    height: int
    background_colour: str


@dataclass
class ProjectBaseClass:
    projects_folder: str = field(default='projects')
    import_extension: str = field(default='.txt')
    overwrite_with: str = field(default=None)
    export_folder: str = field(default='plots')
    export_extension: str = field(default='.png')


if __name__ == '__main__':
    pass
