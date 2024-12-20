#!/bin/bash
# shellcheck disable=2086

# action, source, dir, target
function setup() {
  case $1 in
  0)
    mkdir $3$4
    ;;
  1)
    git clone $2 $3$4
    ;;
  2)
    gh repo clone $2 $3$4
    ;;
  esac
  tmux new-session -d -A -s $4 -c $3$4
  tmux switch-client -t $4
  tmux new-window -d -t $4 -c $3$4
}

dir=$(fd . ~/repos -t d -d 2 | sk)
if [[ -n $dir ]]; then
  if [[ $(dirname $dir) == $HOME/repos ]]; then
    echo -n "Name: "
    read -r target
    if [[ -n $target ]]; then
      source=$target
      target=$(basename $target .git)
      if [[ $source =~ ^https?:// || $source =~ ^git@ ]]; then
        setup 1 $source $dir $target
      elif [[ $source =~ ^[[:alnum:]-]+/[[:alnum:]-]+ ]]; then
        setup 2 $source $dir $target
      else
        setup 0 "" $dir $target
      fi
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
