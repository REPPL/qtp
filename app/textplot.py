import os
import matplotlib.pyplot as plt

from pathlib import Path

from app.document import Document
from app.config import Screen, Font, ProjectBaseClass


class QuickTextPlot(ProjectBaseClass):
    """A new QuickTextPlot project.
    The project name is derived from the folder name within
    `projects_folder/`.
    """

    def __init__(self, params):
        params = vars(params)
        self._param_name = params['name']
        self._param_show_output = params['show_output']
        self._param_verbose = params['verbose']
        self.path = f'{os.getcwd()}/{self.projects_folder}/{self._param_name}'
        try:
            # Attempt to access project directory
            _ = [d.name for d in os.scandir(f'{self.path}/..') if d.is_dir()]
        except FileNotFoundError:
            print('\n>>> ERROR: Project directory does not exist.')
            return None
        self.screen = Screen()
        self.documents = self.get_documents()
        self.sub_plots = {
            title: document.get_img(self.minimum_font_size)
            for title, document in self.documents.items()}
        self.plotting(show=self._param_show_output)

    @property
    def title(self):
        return ' '.join(
            [w.capitalize()
             for w in self._param_name.replace('_', ' ').split()])

    @property
    def minimum_font_size(self):
        font_size = Font().size
        for document in self.documents.values():
            font_size = min(font_size, document.font.size)
        return font_size

    @property
    def files(self):
        project_files = sorted(
            [f.path for f in os.scandir(self.path) if f.is_file()])
        return [f for f in project_files if f.endswith(self.import_extension)]

    def plotting(self, show=False):
        columns = len(self.documents)
        fig, axes = plt.subplots(
            1, columns, layout='constrained')
        if columns < 1:
            return False
        elif columns == 1:
            title = list(self.sub_plots)[0]
            img = self.sub_plots[title]
            axes.imshow(img)
            axes.set_title(title, fontweight='bold', size=Font().size)
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
        plt.savefig(
            f'{export_dir}/{self._param_name}{self.export_extension}',
            dpi=self.screen.dpi*5)
        if show:
            plt.show()
        return True

    def get_documents(self):
        """Initialises the `documents` dictionary for `Project()`.

        Key ..... : File name (with path).
        Value ... : A `Document()` object.
        """

        documents = {}
        for f in self.files:
            k, v = self._new_document(f)
            documents[k] = v
        return documents

    def _new_document(self, file_name):
        """Helper method: Initialises a new document
        for `Project()` object.
        """

        document = Document(
            file_name, self.overwrite_with, self._param_verbose)
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
