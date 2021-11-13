# !/bin/bash

# A basic script to build all premade onfigs in the project for release

set -e

if [ -z "$1" ];then
    echo "No argument supplied – font path required"
    exit 1
fi

fontPath=$1

version=$(font-v report $fontPath | tail -1)
release=ArrowType-RecMonoCode-v$version

echo $release

rm -rf ./fonts

configs=$(ls ./premade-configs)

for config in $configs; do
    python scripts/instantiate-code-fonts.py ./premade-configs/$config $fontPath
done

cp -r ./fonts ./$release

zip $release.zip -r $release -x .DS_*

rm -rf $release
