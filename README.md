# Quick text plot

The aim of this simple script is to quickly plot text highlights. It was initially written to compare text snippets extracted by different LLMs, and to compare them with those highlighted by manual coders.

The script reads an arbitrary number of `.txt` files and visualises them on a single screen:

![Example output from five text files.](/example.png)

See below for [setup](#Setup) instruction and how to use the script: 

1. **[Using the script](#Use)**
2. **[Configuration options](#Configuration)**

*(If you have suggestions or ideas for making this script more useful, please experiment with it and/or [get in touch](https://github.com/REPPL).)*


## Setup


### Install dependencies

So far, the only dependency is [matplotlib](https://matplotlib.org/). Install required dependency with:

```sh
pip install -r requirements.txt
```


### Install a monospace font

You will need to install your favourite (monospace) font, which must be accessible in `.ttf` format. I recommend the  '[liberation-mono.ttf](https://www.fontsquirrel.com/fonts/liberation-mono)' font.

Download as a zip file, unzip, and place a single `.ttf` file (e.g.,  `LiberationMono-Regular.ttf`) into the `app/` directory. If you prefer a different font and/or type, make sure to amend the entry in the `app/config.py` file. In that case, search for and amend the following line:

```python
@dataclass
class Font:
    name: str = field(default='app/LiberationMono-Regular.ttf')
    ...
    ...
```


### Create a projects folder

Text files must be stored in a project sub-folder within the main `projects/` folder. Consequently, 
before using the script, you must create a `projects/` folder where all project sub-folders will be located:

```sh
mkdir projects/
```

Then create a **sub-folder for each project**, e.g.,

```sh
cd projects/
mkdir test_project/
```

This is where the script will look for `.txt` files to visualise. Depending on the number of files -- and their length! -- **the output can be messy** as there is currently no way to control the amount of text shown in a single plot. *(As a general rule of thumb, I recommend using no more than 5 files.)*


## Use

Execute the script using the following command (assuming use of a virtual environment):

```sh
python start.py PROJECT_NAME
```

Stating a `PROJECT_NAME` is mandatory and must match a sub_folder in the main `projects/` folder.


### Arguments

Use `python start.py -h` to list optional arguments. Currently, the following arguments are available:

1. `-s`: Opens the plot in a separate window (in addition to storing it as a `.png` file)
2. `-v`: Verbose mode


### Highlighting text

The main task for manual coder is to highlight text snippets. I am still experimenting with the best way to highlight text snippets manually and how they are being plotted. *(Look at `app/config.py` for the most recent configuration.)*


#### Syntax

At the moment, I am using the following syntax to highlight text (indicated here by `...`):

1. **Positive:** `[p>[` ... `]]`
2. **Negative:** `[n>[` ... `]]`
3. **Generic:** `[[` ... `]]`


#### Colours

Anything thus highlighted will be plotted using the following colours:

1. **Positive:** `#90EE90` *(light green)*
2. **Negative:** `#FFDAB9` *(light red)*
3. **Generic:** `#FFFF00` *(yellow)*


### Configuration

At the moment, the only configuration option is to specify whether to 'anonymise' text output. More options may follow in the future; this option should also be moved to be an [optional argument](#Arguments), but that's not yet the case.


#### Anonymise text

You have the option to overwrite each character with a character of your choice. By default, this option is deactivated and text is **not anonymised**. To change that, go to `app/config.py` and search for the following line:

```python
@dataclass
class ProjectBaseClass:
    ...
    ...
    overwrite_with: str = field(default=None)
    ...
    ...
```

Change the default to any character, e.g.,

```python
    overwrite_with: str = field(default='#')
```

*(This will overwrite every alphanumerical character with `#`.)*
