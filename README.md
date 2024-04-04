# Quick text plot

The aim of this simple script is to quickly plot text highlights. It was initially written to compare text snippets extracted by different LLMs, and to compare them with those highlighted by manual coders.

The script reads an arbitrary number of `.txt` files (stored in a `project_folder/`) and visualises them on a single screen:

![Example output from five text files.](/example.png)

See below for [setup](Setup) instruction and how to use the script: 

1. **[Using the script](Use)**: How to use the script
2. **[Customise the script](Options)**: How to customise the output


## Setup


### Installation

So far, the only dependency is [matplotlib](https://matplotlib.org/). Install required dependency with:

```
pip install -r requirements.txt
```

You will need to install your favourite (monospace) font, which must be accessible in `.ttf` format. I recommend the  '[liberation-mono.ttf](https://www.fontsquirrel.com/fonts/liberation-mono)' font.

Download as a zip file, unzip, and place a single `.ttf` file (e.g.,  `LiberationMono-Regular.ttf`) into the `app/` directory. If you prefer a different font and/or type, make sure to amend the entry in the `app/config.py` file. In that case, search for and amend the following line:

```
@dataclass
class Font:
    name: str = field(default='app/LiberationMono-Regular.ttf')
    ...
    ...
```


## Managing projects

Before using the script, you must create a `projects/` folder to store your projects in:

```
mkdir projects/
```

Then create a sub-folder for each project, e.g.,

```
cd projects/
mkdir test_project/
```

This is where the script expects the `.txt` files to visualise. Depending on the number of files -- and their length! -- **the output can be messy** as there is currently no way to control the amount of text shown in a single plot. *(As a general rule of thumb, I recommend using no more than 5 files.)*


## Use

I am still experimenting with the best way to highlight text snippets manually and how they are being plotted. *(Look at `app/config.py` for the most recent configuration.)*


### Syntax

At the moment, I am using the following syntax to highlight text (indicated here by `...`):

1. **Positive:** `[p>[` ... `]]`
2. **Negative:** `[n>[` ... `]]`
3. **Generic:** `[[` ... `]]`


### Colours

Anything thus highlighted will be plotted using the following colours:

1. **Positive:** `#90EE90` *(light green)*
2. **Negative:** `#FFDAB9` *(light red)*
3. **Generic:** `#FFFF00` *(yellow)*


## Options

At the moment, the only main option is to 'anonymise' text output. More options may follow in the future.


### Anonymise text

You have the option to overwrite each character with a character of your choice. By default, this option is deactivated and text is **not anonymised**. To change that, go to `app/config.py` and search for the following line:

```
@dataclass
class ProjectBaseClass:
    ...
    ...
    overwrite_with: str = field(default=None)
    ...
    ...
```

Change the default to any character, e.g.,

```
    overwrite_with: str = field(default='#')
```

*(This will overwrite every alphanumerical character with `#`.)*
