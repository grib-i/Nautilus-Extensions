#!/usr/bin/env bash

if [ ! -d $HOME/.config/nautilus-extensions++/ ]; then
    mkdir $HOME/.config/nautilus-extensions++/
    echo "Create $HOME/.config/nautilus-extensions++/"
fi

if [ ! -d $HOME/.local/share/nautilus-python/ ]; then
    mkdir $HOME/.local/share/nautilus-python/
fi

if [ ! -d $HOME/.local/share/nautilus-python/extensions/ ]; then
    mkdir $HOME/.local/share/nautilus-python/extensions/
    echo "Create $HOME/.local/share/nautilus-python/extensions/"
fi

echo "Available lang RU | EN | ES"
cp -r ./lang $HOME/.config/nautilus-extensions++/

python3 -m py_compile ./src/NautilusExtensions.py
cp ./src/NautilusExtensions.py $HOME/.local/share/nautilus-python/extensions/

python3 -m compileall ./src/nautilusextensions/
cp -r ./src/nautilusextensions $HOME/.local/share/nautilus-python/extensions/


nautilus -q
