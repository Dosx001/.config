#!/bin/bash
# shellcheck disable=SC2164

install=""

if [[ ! -x git ]]; then
  install="git"
fi

if [[ ! -x jq ]]; then
  install="$install jq"
fi

if [[ -n "$install" ]]; then
  sudo pacman -S "$install"
fi

cd ~/.config
git init
git remote add origin git@github.com:Dosx001/.config.git
git fetch
git checkout -ft origin/main
git submodule update --init
cd nvim
git switch main
cd
find .config/dotfiles -name '.*' -exec ln -s {} ~ \;

jq '.SKIP_HOST_UPDATE=true' .config/discord/settings.json >tmp && mv tmp .config/discord/settings.json

mkdir .zsh
cd .zsh
git clone https://github.com/BuonOmo/yarn-extra-completion
git clone https://github.com/jeffreytse/zsh-vi-mode
git clone https://github.com/zdharma-continuum/fast-syntax-highlighting
git clone https://github.com/zsh-users/zsh-autosuggestions
