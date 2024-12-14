#!/bin/bash
# shellcheck disable=2086

dir=$(fd . ~/repos -t d -d 2 | sk)
if [[ -n $dir ]]; then
  if [[ $(dirname $dir) == $HOME/repos ]]; then
    echo -n "Name: "
    read -r target
    if [[ -n $target ]]; then
      mkdir -p $dir$target
      tmux new-session -d -A -s $target -c $dir/$target
      tmux switch-client -t $target
      tmux new-window -d -t $target -c $dir/$target
    fi
  else
    target=$(basename $dir)
    tmux new-session -d -A -s $target -c $dir
    tmux switch-client -t $target
    tmux send-keys -t $target 'cd src; nvim -c "Telescope find_files"' C-m
    tmux new-window -d -t $target -c $dir
  fi
  if [[ -n $target && -z $TMUX ]]; then
    tmux attach -t $target
  fi
fi
