#!/bin/bash

resurrect() {
	file="$HOME/.local/share/tmux/resurrect/last"
	[ -e "$file" ] || return
	age=$(($(date +%s) - $(stat -c %Y "$file")))
	if [ "$age" -lt 60 ]; then
		printf "💾 %ds" "$age"
	elif [ "$age" -lt 3600 ]; then
		printf "💾 %dm" $((age / 60))
	elif [ "$age" -lt 86400 ]; then
		printf "💾 %dh" $((age / 3600))
	else
		printf "💾 %dd" $((age / 86400))
	fi
}

pacman() {
	datetime=$(tail -n 1000 /var/log/pacman.log |
		tac |
		rg -m1 "pacman --sync -y -u" |
		cut -d' ' -f1 |
		tr -d '[]')
	[ -z "$datetime" ] && return
	days=$(($(($(date +%s) - $(date -d "$datetime" +%s))) / 86400))
	weeks=$((days / 7))
	result=""
	if [ "$weeks" -gt 0 ]; then
		result="$result $((weeks % 4))w"
		days=$((days - weeks * 7))
	fi
	if [ "$days" -gt 0 ]; then
		result="$result ${days}d"
	fi
	if [ -z "$result" ]; then
		result=" 0d"
	fi
	printf "🔃%s" "$result"
}

printf "%s | %s" "$(resurrect)" "$(pacman)"
