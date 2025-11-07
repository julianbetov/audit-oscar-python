from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class ChartResult:
    name: str
    image_b64: str
    analysis: Optional[str] = None

    def to_dict(self) -> Dict[str, str]:
        return {"name": self.name, "image": self.image_b64, "analysis": self.analysis or ""}