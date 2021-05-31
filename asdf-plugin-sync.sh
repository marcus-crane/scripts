#!/bin/bash

TOOLS_FILE="$HOME/.tool-versions"

if [ ! -f "$TOOLS_FILE" ]; then
  echo "$TOOLS_FILE could not be found. Did you remember to symlink your dotfiles?"
  exit 1
fi

PLUGIN_LIST=$(awk '{ print $1 }' "$TOOLS_FILE")

for PLUGIN in $PLUGIN_LIST
do
  asdf plugin-add "$PLUGIN"
done
