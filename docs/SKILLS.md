# JARVIS Skill System

The skill system replaces the old `/actions` directory. It uses a dynamic hot-reloading mechanism (`skill_loader.py`) and strict validation (`skill_manifest.py`).

## Builtin Skills
- `computer/`: OS interactions (launching apps, changing settings).
- `files/`: File system operations.
- `web/`: Browsing, scraping.
- `comms/`: Emails, messaging.
- `data/`: Data pipelines.
- `schedule/`: Reminders, calendars.

## External Skills
Users can drop Python modules into `engine/skills/external/` to extend JARVIS dynamically without restarting the engine.
