#!/bin/bash
set -e

echo "🚀 Setting up Python development environment..."

# Workspace root (postCreateCommand runs from the workspace folder).
WORKSPACE_FOLDER="$(pwd)"

# Install uv if not present
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Sync dependencies
echo "📦 Syncing dependencies with uv..."
uv sync

# Set up SSH keys permissions
if [ -d "$HOME/.ssh" ]; then
    echo "🔐 Configuring SSH keys..."
    chmod 700 "$HOME/.ssh"
    chmod 600 "$HOME/.ssh/id_*" 2>/dev/null || true
    chmod 644 "$HOME/.ssh/*.pub" 2>/dev/null || true
    chmod 644 "$HOME/.ssh/known_hosts" 2>/dev/null || true
fi

# Install oh-my-zsh plugins if not already installed
if [ -d "$HOME/.oh-my-zsh" ]; then
    echo "🎨 Setting up zsh plugins..."
    ZSH_CUSTOM="${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}"

    # Install zsh-autosuggestions
    if [ ! -d "$ZSH_CUSTOM/plugins/zsh-autosuggestions" ]; then
        git clone https://github.com/zsh-users/zsh-autosuggestions "$ZSH_CUSTOM/plugins/zsh-autosuggestions"
    fi

    # Install fast-syntax-highlighting
    if [ ! -d "$ZSH_CUSTOM/plugins/fast-syntax-highlighting" ]; then
        git clone https://github.com/zdharma-continuum/fast-syntax-highlighting.git "$ZSH_CUSTOM/plugins/fast-syntax-highlighting"
    fi

    # Install zsh-history-substring-search
    if [ ! -d "$ZSH_CUSTOM/plugins/zsh-history-substring-search" ]; then
        git clone https://github.com/zsh-users/zsh-history-substring-search.git "$ZSH_CUSTOM/plugins/zsh-history-substring-search"
    fi

    # Install powerlevel10k theme
    if [ ! -d "$ZSH_CUSTOM/themes/powerlevel10k" ]; then
        git clone --depth=1 https://github.com/romkatv/powerlevel10k.git "$ZSH_CUSTOM/themes/powerlevel10k"
    fi
fi

# Install the Powerlevel10k config shipped with this repo
if [ -f "$WORKSPACE_FOLDER/.devcontainer/p10k.zsh" ]; then
    echo "🎨 Installing Powerlevel10k config..."
    cp "$WORKSPACE_FOLDER/.devcontainer/p10k.zsh" "$HOME/.p10k.zsh"
fi

# Configure zsh with your custom settings
echo "⚙️  Configuring zsh..."
cat > "$HOME/.zshrc" << 'ZSHRC_EOF'
# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# Path to your Oh My Zsh installation.
export ZSH="$HOME/.oh-my-zsh"

# Powerlevel10k theme
ZSH_THEME="powerlevel10k/powerlevel10k"

# Disable magic functions (url-quote-magic etc.) — they make paste extremely slow.
DISABLE_MAGIC_FUNCTIONS="true"

# Plugins
plugins=(
    git
    zsh-autosuggestions
    zsh-history-substring-search
    fast-syntax-highlighting
)

# Disable git dirty-check in prompt (slow on big repos)
DISABLE_UNTRACKED_FILES_DIRTY="true"

source $ZSH/oh-my-zsh.sh

# Editor
export VISUAL=vim
export EDITOR="$VISUAL"

# Add local bin to PATH
export PATH="$HOME/.local/bin:$PATH"

# Aliases
alias gca='git commit --amend --no-edit --no-verify'

# Arrow keys for history substring search
bindkey '^[[A' history-substring-search-up
bindkey '^[[B' history-substring-search-down

# Speed up paste: clear autosuggestions during bracketed paste so
# zsh-autosuggestions does not re-fetch a suggestion per pasted char.
# https://github.com/zsh-users/zsh-autosuggestions/issues/238
ZSH_AUTOSUGGEST_CLEAR_WIDGETS+=(bracketed-paste)

# Tab accepts autosuggestion if one is shown; otherwise normal completion.
_tab_autosuggest_or_complete() {
  if [[ -n "$POSTDISPLAY" ]]; then
    zle autosuggest-accept
  else
    zle expand-or-complete
  fi
}
zle -N _tab_autosuggest_or_complete
bindkey '^I' _tab_autosuggest_or_complete

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

# Project aliases (if setup script exists)
WORKSPACE_FOLDER="${containerWorkspaceFolder:-$(pwd)}"
if [ -f "$WORKSPACE_FOLDER/scripts/setup-aliases.sh" ]; then
    source "$WORKSPACE_FOLDER/scripts/setup-aliases.sh"
fi
ZSHRC_EOF

# Set zsh as default shell
if [ "$SHELL" != "$(which zsh)" ]; then
    echo "🐚 Setting zsh as default shell..."
    sudo chsh -s "$(which zsh)" "$(whoami)" || echo "Note: Shell change may require container restart"
fi

# Configure git (if not already configured)
if [ -z "$(git config --global user.name)" ]; then
    echo "📝 Git not configured. Please run:"
    echo "   git config --global user.name 'Your Name'"
    echo "   git config --global user.email 'your.email@example.com'"
fi

# Install pre-commit hooks via prek
echo "🪝 Installing pre-commit hooks..."
prek install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push || echo "Note: Pre-commit hooks installation skipped"

echo "✅ Development environment setup complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Configure git: git config --global user.name 'Your Name'"
echo "   2. Test SSH: ssh -T git@github.com"
echo "   3. Run tests: uv run pytest"
echo "   4. Start coding! 🎉"
