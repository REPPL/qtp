import os
import matplotlib.pyplot as plt

from pathlib import Path

from app.document import Document
from app.config import Screen, Font, ProjectBaseClass


class TextPlot(ProjectBaseClass):
    """A new TextPlot project.
    The project name is derived from the folder name within
    `projects_folder/`.
    """

    def __init__(self, project_name):
        self.name = project_name
        self.path = f'{os.getcwd()}/{self.projects_folder}/{self.name}'
        self.screen = Screen()
        self.documents = self.get_documents()
        self.sub_plots = {
            title: document.get_img(self.minimum_font_size)
            for title, document in self.documents.items()}

    @property
    def title(self):
        return ' '.join(
            [w.capitalize() for w in self.name.replace('_', ' ').split()])

    @property
    def minimum_font_size(self):
        font_size = Font().size
        for document in self.documents.values():
            font_size = min(font_size, document.font.size)
        return font_size

    @property
    def files(self):
        all_projects = [
            d.name for d in os.scandir(f'{self.path}/..') if d.is_dir()]
        if self.name not in all_projects:
            return False
        project_files = sorted(
            [f.path for f in os.scandir(self.path) if f.is_file()])
        return [f for f in project_files if f.endswith(self.import_extension)]

    def print_plot(self, show=False):
        columns = len(self.documents)
        fig, axes = plt.subplots(
            1, columns, layout='constrained')
        if columns < 1:
            return False
        elif columns == 1:
            title = list(self.sub_plots)[0]
            img = self.sub_plots[title]
            axes.imshow(img)
            axes.set_title(title, fontweight='bold', size=10)
            axes.axis('off')
        else:
            for i, (title, img) in enumerate(self.sub_plots.items()):
                column = i % columns
                axes[column].imshow(img)
                axes[column].set_title(title, fontweight='bold', size=10)
                axes[column].axis('off')
        export_dir = f'{self.path}/../{self.export_folder}'
        if not Path(export_dir).is_dir():
            Path(export_dir).mkdir()
        print(f'\nSaving {self.export_extension} to disk ... ', end='')
        plt.savefig(
            f'{export_dir}/{self.name}{self.export_extension}',
            dpi=self.screen.dpi*5)
        print('DONE!')
        if show:
            plt.show()
        return True

    def get_documents(self):
        """Initialises the `documents` dictionary for `Project()`.
        updates a previous version if a `documents` dictionary
        already exists.

        Key ..... : File name (with path).
        Value ... : A `Document()` object.
        """

        try:
            documents = self.documents
            for f in self.files:
                if f not in documents:
                    k, v = self._new_document(f)
                    documents[k] = v
        except AttributeError:  # If self._documents does not yet exist
            documents = {}
            for f in self.files:
                k, v = self._new_document(f)
                documents[k] = v
        self.documents = documents
        return self.documents

    def _new_document(self, file_name):
        """Helper method: Initialises a new document
        for `Project()` object.
        """

        document = Document(
            file_name, self.overwrite_with)
        title = document.title
        # Set textbox for this document
        width = self.screen.width // len(self.files)
        height = self.screen.height
        colour = self.screen.background_colour
        document.set_textbox(width, height, colour)
        # Set minimum font size for this document
        document.calculate_mimimum_font_size()
        # Return title & document
        return title, document


if __name__ == '__main__':
    pass
