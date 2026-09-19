#!/bin/bash

readarray -t sources < <(git remote)

if [[ ${#sources[@]} -eq 1 ]]; then
  source=$(git remote get-url origin)
else
  source=$(printf "%s\n" "${sources[@]}" | sk | xargs git remote get-url)
fi

if [[ $source =~ ^git@ ]]; then
  source=${source#git@}
  source=${source%.git}
  source=${source/:/\/}
elif [[ $source =~ ^ssh:// ]]; then
  source=${source#ssh://}
  source=${source%.git}
  if [[ $source =~ ^aur ]]; then
    source=${source#aur@}
    source=${source%.git}
    source=${source/\//\/packages/}
  else
    source=${source#git@}
  fi
elif [[ ! $source =~ ^https?:// ]]; then
  echo "Invalid source: $source"
  exit
fi

firefox --private-window "$source"
