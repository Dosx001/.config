# .config

```bash
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
```

```bash
cd ~
mkdir .zsh
cd .zsh
git clone https://github.com/BuonOmo/yarn-extra-completion
git clone https://github.com/jeffreytse/zsh-vi-mode
git clone https://github.com/zdharma-continuum/fast-syntax-highlighting
git clone https://github.com/zsh-users/zsh-autosuggestions
source ~/.zshrc
```

## FireFox

extensions.webextensions.restrictedDomains  
privacy.resistFingerprinting.block_mozAddonManager
