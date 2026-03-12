# 🦝 Pomodoro Raccoon 🍅

A cute CLI Pomodoro timer with ASCII raccoon animations to keep you productive!

## Features

- 🍅 **Pomodoro sessions** with short (5 min) and long (25 min) breaks
- 🔄 **Session tracking** — counts your Pomodoros and automatically offers a long break after every 4 sessions
- 🦝 **ASCII raccoon animations** that switch every 5 seconds
- 🎨 **Coloured progress bar** with phase-based colours
- ⏱ **Live countdown** displayed alongside the animation
- ⌨️ **Press Enter** to end a session early or skip a break — no Ctrl+C needed
- 🔔 **Desktop notifications** when a session or break ends (Linux & macOS)
- 🔊 **Sound alerts** on session start and end (Linux & Windows)
- ⚙️ **Configurable durations** via CLI arguments

## Installation

The recommended way to install CLI tools is with **pipx**, which keeps everything isolated without needing to manage a venv manually:

```bash
pipx install pomodoro-raccoon
```

Don't have pipx? Install it first:
```bash
# Linux (Debian/Ubuntu)
sudo apt install pipx

# macOS
brew install pipx

# Windows (run in PowerShell)
pip install pipx
pipx ensurepath
# Restart your terminal after running ensurepath
```

Alternatively with pip (inside a virtual environment):
```bash
pip install pomodoro-raccoon
```

## Usage

```bash
pomodoro-raccoon
```

Custom durations:
```bash
pomodoro-raccoon --work 50 --short-break 10 --long-break 30
```

## CLI Options

| Option | Default | Description |
|---|---|---|
| `--work MIN` | 25 | Work session duration in minutes |
| `--short-break MIN` | 5 | Short break duration in minutes |
| `--long-break MIN` | 25 | Long break duration in minutes |

## Preview

```
       🍅
     (\_/)
     ( •_•)
     / >🍵   Focusing...

  Session 1
  [████████████████--------------] 53%
  ⏱  11:44 remaining
  💬 Keep it up, champ! 🦝💪

  [Press Enter to end session early]
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for the full release history.

## License

MIT License — see [LICENSE](LICENSE).
