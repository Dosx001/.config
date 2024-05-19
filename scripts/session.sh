#!/bin/bash
# shellcheck disable=2086

dir=$(fd . ~/repos -t d -E dist -E node_modules -E src -E src-tauri | sk)
if [[ -n $dir ]]; then
  target=$(basename $dir)
  tmux new-session -d -A -s $target -c $dir
  tmux switch-client -t $target
  tmux send-keys -t $target "cd src; nvim -c 'Telescope find_files'" C-m
  tmux new-window -d -t $target -c $dir
fi
