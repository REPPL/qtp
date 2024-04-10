import re

from PIL import Image, ImageDraw, ImageFont, ImageColor

from app.config import Highlighter, Font, Textbox


class Collection():
    """
    """

    pass


class Document():
    """A new document object generated from `file_name`.

    ========
    Required
    ========

    `file_name` ... : A unique filename.
    `config` ...... : A config dict (from argparse).
    """

    def __init__(self, file_name, config):
        self.file_name = file_name
        self.config = config
        self.textbox = None
        self.font = Font()
        self.highlighter = Highlighter()

    @property
    def title(self):
        return self.file_name.split('/')[-1].split('.')[0].upper()

    @property
    def paragraphs(self):
        try:
            with open(self.file_name, 'r') as f:
                raw_text = f.read()
            return raw_text.split('\n\n')
        except Exception as e:
            raise f'\nERROR READING FILE:\n{e}.'

    @property
    def lines(self):
        lines = []
        for paragraph in self.paragraphs:
            line = ''
            for word in paragraph.split():
                font = ImageFont.truetype(self.font.name, self.font.size)
                # Remove markup
                clean_line = ''.join(
                    re.split(self.highlighter.pattern, line + ' ' + word))
                _, _, width, _ = font.getbbox(clean_line)
                if width <= self.textbox.width * .95:
                    line += ' ' + word
                else:
                    lines.append(line.strip())
                    line = word
            lines.append(line.strip())
            lines.append(' ')
        return lines

    def get_img(self, font_size):

        def get_color(c1, c2):
            """Helper function to combine two RGBA values.

            Adapted from charlotte/Stackoverflow:
            https://stackoverflow.com/questions/52992900/
            how-to-blend-two-rgb-colors-front-and-back-based-on-their-alpha-channels
            """

            a = 255 - ((255 - c1[3]) * (255 - c2[3]) // 255)
            r = (c1[0] * (255 - c2[3]) + c2[0] * c2[3]) // 255
            g = (c1[1] * (255 - c2[3]) + c2[1] * c2[3]) // 255
            b = (c1[2] * (255 - c2[3]) + c2[2] * c2[3]) // 255
            return (r, g, b, a)
        # <-- Begin get_img() -->

        self._print_status_message(
            f'Generating image for "{self.title}" ... ')
        y = 0
        line_height = font_size * 1.1
        img = Image.new(
            'RGBA',
            (self.textbox.width, self.textbox.height),
            self.textbox.background_colour)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(self.font.name, self.font.size)
        # Assign background colour as default background for highlights
        # highlights = [self.textbox.background_colour]
        highlights = []
        for line in self.lines:
            x = 0
            # Check for highlights
            for chunk in re.split(self.highlighter.pattern, line):
                _, _, width, _ = font.getbbox(chunk)
                if chunk in self.highlighter.colours.keys():
                    highlights.append(chunk)
                    continue
                elif chunk in self.highlighter.closing_pattern.keys():
                    highlights.reverse()
                    try:
                        highlights.remove(
                            chunk.replace(self.highlighter.closing_char, ''))
                        continue
                    except ValueError:
                        pass
                    finally:
                        highlights.reverse()
                # Draw box to highlight
                highlight_box = draw.textbbox((x, y), chunk, font=font)
                if highlights:
                    fill_colour = self.highlighter.colours[highlights[-1]]
                else:
                    fill_colour = self.textbox.background_colour
                # Mixing colours? Cycling through highlights
                if self.config['mix_colours']:
                    for highlight in highlights:
                        fill_colour = get_color(
                            fill_colour, self.highlighter.colours[highlight])
                # Fill text box
                draw.rectangle(highlight_box, fill=fill_colour)
                # Anonymise text (optional)
                try:
                    text = ''.join(
                        [c if not c.isalnum() else self.config['anonymise']
                         for c in chunk])
                except TypeError:
                    text = chunk
                draw.text(
                    (x, y), text, font=font, fill=self.font.colour)
                # Adjust width
                x += width
            # Adjust height
            y += line_height
        self._print_status_message(None)  # == DONE!
        return img

    def set_textbox(self, width, height, colour):
        self.textbox = Textbox(width, height, colour)
        return True

    def calculate_mimimum_font_size(self):
        self._print_status_message(
            f'Calculating minimum font size for "{self.title}" ... ')
        while True:
            text = ' '.join(self.paragraphs)
            font = ImageFont.truetype(self.font.name, self.font.size)
            _, _, width, height = font.getbbox(text.strip())
            width += len(self.paragraphs) * height
            number_of_lines = width // self.textbox.width
            height *= number_of_lines
            # Clumsy ... but I'm limiting to 80% for now ...
            if height < self.textbox.height * .7:
                break
            else:
                self.font.size -= 1
        self._print_status_message(None)
        return True

    def _print_status_message(self, message):
        if not self.config['verbose']:
            return False
        if not message:
            print('DONE!')
        else:
            print(message, end='')
        return True


if __name__ == '__main__':
    pass
