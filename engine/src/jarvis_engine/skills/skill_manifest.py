from pydantic import BaseModel
from typing import List, Optional

class SkillManifest(BaseModel):
    name: str
    description: str
    version: str
    author: Optional[str] = "JARVIS"
    entry_point: str
    dependencies: List[str] = []
    permissions: List[str] = []
