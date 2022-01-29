

# fetch latest changes to upstream

```
# git remote add upstream git://github.com/ORIGINAL-DEV-USERNAME/REPO-YOU-FORKED-FROM.git
git fetch upstream
git pull upstream main
```


# setup one time

```
python -m venv venv             # make a virtual environment called "venv"
bash
source venv/bin/activate         # activate the virtual environment
pip install -r requirements.txt  # install dependencies
```

# build the font

```
bash
source venv/bin/activate         # activate the virtual environment if you haven’t already
python scripts/instantiate-code-fonts.py premade-configs/config.code.yaml font-data/Recursive_VF_1.084.ttf
```
