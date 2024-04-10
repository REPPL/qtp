import os
import matplotlib.pyplot as plt

from pathlib import Path

from app.documents import Collection, Document
from app.config import Screen, Font, ProjectBaseClass


class QuickTextPlot(ProjectBaseClass):
    """A new QuickTextPlot project. The project name is derived from
    the folder name within `projects_folder/`.
    """

    def __init__(self, config):
        self.config = vars(config)
        self.name = self.config['name']
        self.path = f'{os.getcwd()}/{self.projects_folder}/{self.name}'
        try:
            # Attempt to access project directory
            _ = [d.name for d in os.scandir(f'{self.path}/..') if d.is_dir()]
        except FileNotFoundError:
            print('\n>>> ERROR: Main projects directory does not exist.')
            return None
        self.screen = Screen()
        self.documents = self._get_documents()
        self.sub_plots = {
            title: document.get_img(self.minimum_font_size)
            for title, document in self.documents.items()}
        self.plotting()

    @property
    def title(self):
        return ' '.join(
            [w.capitalize()
             for w in self.name.replace('_', ' ').split()])

    @property
    def minimum_font_size(self):
        font_size = Font().size
        for document in self.documents.values():
            font_size = min(font_size, document.font.size)
        return font_size

    def get_files(self, collections=False, folder=None):
        """Returns a list of document files located in the
        current project folder.

        ======
        Option
        ======

        `collections=True` ... Returns a list of sub-folders within
                               the current project folder.
        """

        path = self.path
        if collections:
            return sorted(
                [f.path for f in os.scandir(path) if f.is_dir()])
        # If not collections, then return document files
        if folder:
            path = f'{self.path}/{folder}/'
        files = sorted(
            [f.path for f in os.scandir(path) if f.is_file()])
        return [f for f in files if f.endswith(self.import_extension)]

    def plotting(self):
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
            f'{export_dir}/{self.name}{self.export_extension}',
            dpi=self.screen.dpi*5)
        if self.config['show']:
            plt.show()
        return True

    def get_collections(self):
        """Returns a dictionary with collections of documents.
        Collections are derived from the name of sub_folders
        within the folder for this project.

        Key ..... : Name of the collection.
        Value ... : A dictionary with `Document()` objects
                    for this collection.

        If the project folder does not contain any sub_folders,
        no collection is generated and a dictionary with
        documents is returned.
        """

        collections = {}
        for f in self.get_files(collections=True):
            documents = self._get_documents(folder=f)
            collections[f] = documents
        if not collections:
            return self._get_documents()

    def _get_documents(self, folder=None):
        """Returns a dictionary for `documents`:

        Key ..... : The document's file name (with path).
        Value ... : A `Document()` object.
        """

        documents = {}
        for f in self.get_files(folder):
            k, v = self._new_document(f)
            documents[k] = v
        return documents

    def _new_document(self, file_name):
        """Helper method: Initialises a new document.
        """

        document = Document(file_name, self.config)
        title = document.title
        # Set textbox for this document
        width = self.screen.width // len(self.get_files())
        height = self.screen.height
        colour = self.screen.background_colour
        document.set_textbox(width, height, colour)
        # Set minimum font size for this document
        document.calculate_mimimum_font_size()
        # Return title & document
        return title, document


if __name__ == '__main__':
    pass
