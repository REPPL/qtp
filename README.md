
# Quick text plot (qtp)

The aim of this script is to quickly plot text highlights. It was initially written to compare text snippets extracted by different LLMs, and to compare them with those highlighted by manual coders.

The script reads an arbitrary number of `.txt` files and visualises them on a single screen:

![Example output from five text files.](/example.png)

See below for [setup](#Installation) instructions and how to use the script: 

1. **[Using the script](#Use)**
2. **[Configuration options](#Configuration)**

This script remains work-in-progress. Please [get in touch](https://github.com/REPPL) if you have ideas and/or suggestions on how to make it useful.


## Installation


### Dependencies

So far, the only dependency is [matplotlib](https://matplotlib.org/). Install required dependency with:

```sh
pip install -r requirements.txt
```


### Monospace font

You will need to install your favourite (monospace) font, which must be available in `.ttf` format. I recommend the  '[liberation-mono.ttf](https://www.fontsquirrel.com/fonts/liberation-mono)' font.

Download as a zip file, unzip, and place a single `.ttf` file (e.g.,  `LiberationMono-Regular.ttf`) into the `app/` directory. If you prefer a different font and/or type, make sure to amend the entry in the `app/config.py` file. In that case, search for and amend the following line:

```python
@dataclass
class Font:
    name: str = field(default='app/LiberationMono-Regular.ttf')
    ...
    ...
```


### Projects folder

Text files must be stored in a project sub-folder within the main `projects/` folder. Consequently, you must create a `projects/` folder manually where all project sub-folders will be located:

```sh
mkdir projects/
```

Then create a **sub-folder for each project**, e.g.,

```sh
cd projects/
mkdir test_project/
```

This is where the script will look for `.txt` files to visualise. Depending on the number of files -- and their length! -- **the output can be messy** as there is currently no way to control the amount of text shown in a single plot. *(As a general rule of thumb, I recommend combining no more than 5 files in a single plot.)*


## Use

Execute the script using the following command (assuming an active virtual environment):

```sh
python start.py PROJECT_NAME
```

Stating a `PROJECT_NAME` is mandatory and must match one of the sub_folders in the main `projects/` directory.


### Optional arguments

Use `python start.py -h` to list optional arguments.

Currently, the following arguments are supported:

1. [`-a`] **Anonymise text:** You have the option to overwrite each character with a character of your choice. By default, this option is deactivated and text is **not anonymised**.
2. [`-s`] **Show plot:** Show output in separate window, in addition to storing it as a `.png` file
2. [`-m`] **Mix colours:** Mix colours of multiple highlights *(experimental!)*
3. [`-v`] **Verbose mode**


### Highlighting text

I am still experimenting with the best way to highlight text snippets and how to plot them. *(Look at `app/config.py` for the most recent configuration.)*

**Current syntax:** At the moment, I am using the following syntax to highlight text (indicated here by `...`):

1. **Positive:** `<<p>>` ... `<</p>>`
2. **Negative:** `<<n>>` ... `<</n>>`
3. **Generic:** `<<g>>` ... `<</g>>`

**Colours:** Anything thus marked is highlighted using the following colours:

2. **Generic:** `(243, 235, 8, 155)` *(yellow)*
3. **Positive:** `(8, 243, 15, 155)` *(green)*
4. **Negative:** `(243, 8, 64, 155)` *(red)*


