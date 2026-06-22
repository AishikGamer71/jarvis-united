# JARVIS Skill System

The skill system allows for procedural self-improvement and custom extensions.

## Core Concepts
- **`skills/skill_loader.py`**: A mechanism to dynamically load tools/skills at runtime.
- **`skills/skill_manifest.py`**: The strict schema validation system to ensure any new skill complies with the expected input and output parameters.

## Adding Skills
Skills are essentially new programmatic abilities. When the agent loop successfully discovers a new reliable routine (or the user manually writes a new tool), it is documented using the `skill_manifest.py` schema, enabling JARVIS to reuse it without manual hardcoding in the core engine.
