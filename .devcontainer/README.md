# DevContainer Setup

This directory contains the configuration for the Python development container environment.

## Features

- **Python 3.14** development environment
- **zsh** with **Oh My Zsh** and **Powerlevel10k** theme
- **SSH keys** mounted from host for seamless Git access
- **Docker-in-Docker** support for containerized development
- **GitHub CLI** for repository management
- **Pre-configured VS Code extensions**:
  - Python (ms-python.python)
  - Ruff (charliermarsh.ruff)
  - Mypy Type Checker (ms-python.mypy-type-checker)
  - Docker (ms-azuretools.vscode-docker)
  - GitLens (eamodio.gitlens)
  - Error Lens (usernamehw.errorlens)
  - And more...

## Quick Start

1. **Open in VS Code**: Open the project folder in VS Code
2. **Reopen in Container**: Press `F1` → `Dev Containers: Reopen in Container`
3. **Wait for setup**: The container will build and run the post-create script
4. **Start coding**: Everything is ready!

## First-Time Setup

After the container starts, you may need to:

1. **Configure Git** (if not already done):

   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

2. **Test SSH connection**:

```bash
   ssh -T git@github.com
   ```

3.**Verify environment**:

   ```bash
python --version
   uv --version
   ```

## Port Forwarding

The following ports are forwarded for development:

- **8000**: API server (if needed)
- **5432**: PostgreSQL database (if needed)
- **6379**: Redis cache (if needed)

## Customization

### zsh Configuration

The zsh configuration matches the WSL host setup with:

- Powerlevel10k theme, with `.p10k.zsh` shipped in `.devcontainer/p10k.zsh` and copied to `~/.p10k.zsh` (no first-run wizard)
- p10k instant prompt enabled
- Plugins: git, zsh-autosuggestions, zsh-history-substring-search, fast-syntax-highlighting
- History substring search with arrow keys
- `DISABLE_MAGIC_FUNCTIONS` and `DISABLE_UNTRACKED_FILES_DIRTY` for paste/prompt speed
- Bracketed-paste autosuggest clear and Tab-to-accept autosuggestion
- `gca` alias (`git commit --amend --no-edit --no-verify`)

To change the prompt, edit `.devcontainer/p10k.zsh` (tracked in the repo) — `~/.p10k.zsh` is regenerated from it on container create.

### SSH Keys

Your SSH keys from `~/.ssh` are automatically mounted into the container at `/home/vscode/.ssh` with proper permissions.

### VS Code Settings

All VS Code settings from `.vscode/settings.json` are applied in the container, including:

- Ruff as default formatter
- Format on save
- Mypy type checking
- Pytest configuration
- File exclusions for cache folders

## Troubleshooting

### Container won't start

- Check Docker is running: `docker ps`
- Check VS Code Dev Containers extension is installed
- Review container logs in VS Code

### SSH keys not working

- Verify keys exist in `~/.ssh` on host
- Check permissions: `chmod 700 ~/.ssh && chmod 600 ~/.ssh/id_*`
- Test SSH: `ssh -T git@github.com`

### Python version issues

- The container uses Python 3.14 as required by the project
- Verify Python version: `python --version`

### Dependencies not syncing

- Run manually: `uv sync`
- Check `uv.lock` is up to date
- Verify network connectivity

## Rebuilding the Container

To rebuild the container with fresh dependencies:

1. **Command Palette**: `F1` → `Dev Containers: Rebuild Container`
2. Or delete the container image and rebuild

## Additional Resources

- [Dev Containers Specification](https://containers.dev/implementors/spec/)
- [VS Code Dev Containers Documentation](https://code.visualstudio.com/docs/devcontainers/containers)
