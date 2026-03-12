# Changelog / Änderungsprotokoll

---

## [0.2.0] - 2026-03-12

### English

#### Added
- Session counter: tracks progress through a 4-session Pomodoro cycle
- Long break (25 min) automatically offered after every 4 sessions
- Press Enter during a session or break to exit/skip without Ctrl+C
- Desktop notifications via `notify-send` (Linux) and `osascript` (macOS) when a session or break ends
- CLI arguments: `--work`, `--short-break`, `--long-break` to customize durations

#### Fixed
- Countdown timer was invisible — animation and timer now render together, updating every second
- Animation frame drift: switched from a fixed 10-second tick to wall-clock time
- Global mutable state (`is_running`) replaced with thread-safe `threading.Event`

#### Changed
- ASCII frames now switch every 5 seconds instead of every second
- `start_pomodoro_timer` and `start_break_timer` unified into a single `run_timer()` function
- All UI strings translated to English
- Corrected spelling: "racoon" → "raccoon" throughout the project

---

### Deutsch

#### Hinzugefügt
- Sitzungszähler: zeigt den Fortschritt im 4-Session-Pomodoro-Zyklus an
- Lange Pause (25 Min.) wird automatisch nach jeder 4. Session angeboten
- Enter-Taste beendet eine Session oder überspringt eine Pause — kein Ctrl+C nötig
- Desktop-Benachrichtigungen über `notify-send` (Linux) und `osascript` (macOS) am Ende jeder Session oder Pause
- CLI-Argumente: `--work`, `--short-break`, `--long-break` zur individuellen Anpassung der Zeiten

#### Fehlerbehebungen
- Countdown-Timer war unsichtbar — Animation und Timer werden jetzt gemeinsam jede Sekunde neu gerendert
- Animations-Drift behoben: fester 10-Sekunden-Takt durch Echtzeit-Messung ersetzt
- Globaler veränderlicher Zustand (`is_running`) durch thread-sicheres `threading.Event` ersetzt

#### Geändert
- ASCII-Frames wechseln nun alle 5 Sekunden statt jede Sekunde
- `start_pomodoro_timer` und `start_break_timer` zu einer einzigen `run_timer()`-Funktion zusammengeführt
- Alle UI-Texte ins Englische übersetzt
- Tippfehler korrigiert: „racoon" → „raccoon" im gesamten Projekt

---

## [0.1.3] - 2024

### English

#### Changed
- Renamed package folder to match Python packaging conventions
- Minor internal fixes

---

### Deutsch

#### Geändert
- Paketordner umbenannt für korrekte Python-Paketstruktur
- Kleinere interne Korrekturen

---

## [0.1.0] - 2024

### English

#### Added
- Initial release
- 25-minute Pomodoro timer with 5-minute break
- ASCII raccoon animations during work and break sessions
- Coloured progress bar with phase-based colours
- Platform-native sound alerts (Linux & Windows)
- Motivational messages throughout the session
- Automatic break timer after each Pomodoro session

---

### Deutsch

#### Hinzugefügt
- Erstveröffentlichung
- 25-Minuten-Pomodoro-Timer mit 5-Minuten-Pause
- ASCII-Waschbär-Animationen während der Arbeits- und Pausenphasen
- Farbige Fortschrittsleiste mit phasenbasierten Farben
- Plattformnative Signaltöne (Linux & Windows)
- Motivierende Nachrichten während der Session
- Automatischer Pausentimer nach jeder Pomodoro-Session
