# Quick text plot

The aim of this simple script is to quickly plot text highlights. It was initially developed to compare text snippets extracted by different LLMs, and to compare them with those highlighted by manual coders.


![Example output.](/example.png)


## Installation

So far, the only dependency is [matplotlib](https://matplotlib.org/), which may change once the script is being developed. You install all required dependency using:

```
pip install -r requirements.txt
```

You will need to install a (monospace) font of your choice. The file must be a `.ttf` format and I recommend '[liberation-mono.ttf](https://www.fontsquirrel.com/fonts/liberation-mono)'.

Download the font as a zip file, unzip, and place the `LiberationMono-Regular.ttf` into the `app/` directory. *(If you wish to use a different font and/or different type, make sure to amend the entry in the `app/config.py` file. Search for the following line:

```
@dataclass
class Font:
    name: str = field(default='app/LiberationMono-Regular.ttf')
    ...
    ...
```


## Managing projects

You must create a `projects/` folder where you store your projects in:

```
mkdir projects/
```

Then create a sub-folder for each project, e.g.,

```
cd projects/
mkdir test_project/
```

This is where you store the `.txt` files you wish to visualise. Depending on the number of files -- and their length! -- the output can be messy as there is currently no way to control this. *(As a general rule of thumb, I recommend using no more than 5 files.)*


## Options

### Anonymising text

You have the option to 'anonymise' text, that is, to overwrite each character with a character of your choice. By default, text is not anonymised. If you wish to change that, go to `app/config.py` and search for the following line:

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


## Highlights

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
