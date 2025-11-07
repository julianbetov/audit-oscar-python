# python
from typing import Dict, Iterable, Optional

from BaseChart import BaseChart
from Charts.OverallCompliance import OverallComplianceChart


class ChartRegistry:
    def __init__(self):
        self._charts: Dict[str, BaseChart] = {}

    def register(self, chart: BaseChart) -> None:
        self._charts[chart.name] = chart

    def get(self, name: str) -> Optional[BaseChart]:
        return self._charts.get(name)

    def all(self) -> Iterable[BaseChart]:
        return self._charts.values()

    def default_register_all(self) -> "ChartRegistry":
        self.register(OverallComplianceChart())
        return self
