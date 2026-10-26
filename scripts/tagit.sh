#!/bin/bash

if [[ -e build.zig.zon ]]; then
	version=$(rg '\.version' build.zig.zon | cut -d'"' -f2)
elif [[ -e package.json ]]; then
	version=$(jq -r '.version' package.json)
elif [[ -e Cargo.toml ]]; then
	version=$(rg version Cargo.toml | cut -d'"' -f2)
else
	echo 'Not supported'
	exit
fi

git tag -a "${version}" -m "${version}" && git push --tags
