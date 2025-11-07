from typing import Any, Dict, List


class AuditData:
    def __init__(self, json_data: Dict[str, Any]):
        self.raw = json_data or {}
        self.summary: Dict[str, Any] = self.raw.get("overall_summary", {}) or {}
        self.themes: List[Dict[str, Any]] = self.raw.get("themes_overview", []) or []
        self.remarks: Dict[str, Any] = self.raw.get("remarks_analysis", {}) or {}
        self.stats: Dict[str, Any] = self.raw.get("statistical_summary", {}) or {}
        self.data_quality: Dict[str, Any] = self.raw.get("data_quality", {}) or {}
        self.metadata: Dict[str, Any] = self.raw.get("analysis_metadata", {}) or {}

    # Safe getters with defaults
    def get_summary_number(self, key: str, default: float = 0.0) -> float:
        return float(self.summary.get(key, default) or 0)

    def get_stats_number(self, key: str, default: float = 0.0) -> float:
        return float(self.stats.get(key, default) or 0)

    def get_quality_number(self, key: str, default: float = 0.0) -> float:
        return float(self.data_quality.get(key, default) or 0)
