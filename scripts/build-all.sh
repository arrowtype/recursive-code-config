# !/bin/bash

# A basic script to build all premade onfigs in the project for release

set -e

version=1.064
release=ArrowType-RecMonoCode-v$version

rm -rf ./fonts

configs=$(ls ./premade-configs)

for config in $configs; do
    python scripts/instantiate-code-fonts.py ./premade-configs/$config
done

cp -r ./fonts ./$release

zip $release.zip -r $release -x .DS_*

rm -rf $release
