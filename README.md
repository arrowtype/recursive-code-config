# Customize Recursive for Code

You can get premade Recursive fonts for Desktop, Web, & Code at https://github.com/arrowtype/recursive/releases/latest.

But, if you want to customize your own build of Recursive for Code, you can run the script in this repo!

## Usage

0. Set up this Python project

- To work directly with these examples, you should have [Git set up on your computer](https://help.github.com/en/github/getting-started-with-github/set-up-git).
- To use DrawBot as a module, you must also [Download Python](http://python.org/download/) and install it if you haven’t already.
- This uses a virtual environment to keep installed Python modules contained. If you are used to using node_modules in a JavaScript-based project, it’s similar to that.

In a terminal, use `cd` to get to a folder you want this project in. Then, clone the repo:

```
git clone https://github.com/arrowtype/recursive-code-config.git
cd recursive-code-config
```

Then, set up the venv and install requirements:

```bash
python3 -m venv venv             # make a virtual environment
source venv/bin/activate         # activate the virtual environment
pip install -r requirements.txt  # install dependencies
```

1. Customize your font settings in `config.yaml`

This file uses YAML. Hopefully, it is fairly self-explanatory. If not, file an issue and someone will hopefully help out!

First, specify the family name you want (e.g. `Rec Mono Custom`). 

Then, specify axis values you want for Regular, Italic, Bold, & Bold Italic fonts.

Finally, you can copy in the font feature options you want:

```yaml
Options:
  ss01 # single-story a
  ss02 # single-story g
  ss03 # simplified f
  ss04 # simplified i
  ss05 # simplified l
  ss06 # simplified r
  ss07 # serifless L and Z
  ss08 # simplified @
  ss09 # simplified 6 and 9
  ss10 # dotted 0
  ss11 # simplified 1
```

1. Build the font!

```bash
python3 instantiate-code-fonts.py
```

## To do

- [ ] let config options control font features
- [ ] improve output file names