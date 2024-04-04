import re

from PIL import Image, ImageDraw, ImageFont

from app.config import Font, Highlight, Textbox


class Document():
    """A new document object created from the file
    specified in `file_name`.
    """

    def __init__(self, file_name, overwrite_with, verbose):
        self.file_name = file_name
        self.overwrite_with = overwrite_with
        self.verbose = verbose
        self.textbox = None
        self.font = Font()
        self.highlight = Highlight()

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
                    re.split(r'\[[n|p]?>?\[|\]\]', line + ' ' + word))
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
        self._print_status_message(
            f'Generating image for "{self.title}" ... ')
        y = 0
        line_height = font_size * 1.1
        img = Image.new(
            'RGB',
            (self.textbox.width, self.textbox.height),
            self.textbox.background_colour)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(self.font.name, self.font.size)
        # Set default text colour
        font_colour = self.font.colour
        highlight = None
        for line in self.lines:
            x = 0
            # Check for highlights
            for chunk in re.split(r'(\[[n|p]?>?\[|\]\])', line):
                _, _, width, _ = font.getbbox(chunk)
                if chunk == '[[':
                    highlight = self.highlight.generic
                    continue
                elif chunk == '[n>[':
                    highlight = self.highlight.negative
                    continue
                elif chunk == '[p>[':
                    highlight = self.highlight.positive
                    continue
                elif chunk == ']]':
                    highlight = None
                    continue
                if highlight:
                    highlight_box = draw.textbbox(
                        (x, y), chunk, font=font)
                    draw.rectangle(highlight_box, fill=highlight)
                # Anonymise text (optional)
                if self.overwrite_with:
                    text = ''.join(
                        [c if not c.isalnum() else self.overwrite_with
                         for c in chunk])
                else:
                    text = chunk
                draw.text(
                    (x, y), text, font=font, fill=font_colour)
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
        if self.verbose:
            return False
        if not message:
            print('DONE!')
        else:
            print(message, end='')
        return True


if __name__ == '__main__':
    pass
