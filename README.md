# .config

```bash
cd ~/.config
git init
git remote add origin git@github.com:Dosx001/.config.git
git fetch
git checkout -ft origin/main
cd
find .config/dotfiles -name '.*' -exec ln -s {} ~ /;
```
