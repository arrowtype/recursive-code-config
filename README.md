# Customize Recursive for Code

You can get premade Recursive fonts for Desktop, Web, & Code at https://github.com/arrowtype/recursive/releases/latest.

But, if you want to customize your own build of Recursive for Code, you can run the script in this repo!

Note: this is an experimental repo & mostly for entertainment. It’s not really an official part of the Recursive project; I just hope it’s fun & helpful to some people. If it’s not, sorry! Feel free to make a PR to improve it, or to just use the [pre-configured Code fonts](https://github.com/arrowtype/recursive/releases/latest).

If you find issues in this customization workflow, please report them in this repo’s [Issues](https://github.com/arrowtype/recursive-code-config/issues).

If you find issues in the fonts themselves, please report them in the [Recursive project Issues](https://github.com/arrowtype/recursive/issues).


## Usage

The basic way to use this tool is to:

1. Clone the repo and install dependencies (you may wish to fork first, so you can save your preferences to GitHub)
2. Configure your font options in `config.yaml`
3. Run the build script

This instantiates custom fonts for Regular, Italic, Bold, and Bold Italic styles, which you can then use in your preferred editor. One VS Code theme that supports Italics is the [Recursive Theme](https://github.com/arrowtype/recursive-theme).


### Prerequisites for this Python project

- To work directly with these examples, you should have [Git set up on your computer](https://help.github.com/en/github/getting-started-with-github/set-up-git).
- To run the font-building script, you must also [Download Python](http://python.org/download/) and install it if you haven’t already.
- This uses a virtual environment to keep installed Python modules contained. If you are used to using node_modules in a JavaScript-based project, it’s somewhat similar to that.

In a terminal, use `cd` to get to a folder you want this project in. Then, clone the repo and move into it:

```
git clone https://github.com/arrowtype/recursive-code-config.git
cd recursive-code-config
```

Then, set up the venv and install requirements:

```bash
python3 -m venv venv             # make a virtual environment called "venv"
source venv/bin/activate         # activate the virtual environment
pip install -r requirements.txt  # install dependencies
```


### 1. Customize your font settings in `config.yaml`

This file uses YAML. Hopefully, it is fairly self-explanatory. If not, file an issue and someone will hopefully help out!

First, specify the family name you want (e.g. `Rec Mono Custom`). 

Then, specify axis values you want for Regular, Italic, Bold, & Bold Italic fonts.

Then, specify whether you want code ligatures on by default. Mark `True` for yes or `False` for no.

Finally, you can copy in the font feature options you want:

```yaml
# These options only have an affect at CRSV<=0.5 (roman/normal styles)
- ss01 # single-story a
- ss02 # single-story g
- ss03 # simplified f
- ss04 # simplified i
- ss05 # simplified l
- ss06 # simplified r

# These options affect both Roman & Cursive styles
- ss07 # serifless L and Z
- ss08 # simplified @
- ss09 # simplified 6 and 9
- ss10 # dotted 0
- ss11 # simplified 1
```

![OpenType features](font-data/img/recursive-ot_features.png)


### 2. Build the fonts!

Build the fonts by running the main Python script in the project:

```bash
python3 scripts/instantiate-code-fonts.py
```

It will build & output fonts to a folder like `RecMono-Custom` (this is affected by whatever custom name you give fonts in config.yaml).

**Building with other config files**

If you wish to build fonts with premade configurations (or reference these), just add their path as an argument:

```bash
py scripts/instantiate-code-fonts.py premade-configs/duotone.yaml
```

This argument may also be helpful if you wish to create multiple custom versions. To experiment, just duplicate the `config.yaml` with a new filename, change the `Family Name` option, and run the script pointing to that new config file.

## Project to-dos

- [ ] improve output file names with custom names
- [ ] fix or surpress console warnings from feature freezer (example below)

```console
WARNING: [applySubstitutions] Cannot remap 'idot' -> 'idot.mono' because neither has a Unicode value assigned in any of the cmap tables.
```
