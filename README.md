# .config

```bash
cd ~/.config
git init
git remote add origin git@github.com:Dosx001/.config.git
git fetch
git checkout -ft origin/main
git submodule update --init
cd
find .config/dotfiles -name '.*' -exec ln -s {} ~ /;
```
