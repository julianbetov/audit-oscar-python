# python
from typing import List, Optional, Dict

from AuditData import AuditData
from ChartRegistry import ChartRegistry
from ChartResult import ChartResult
from servicios.OpenRouter import OpenRouter


class AuditAnalyzer:
    def __init__(
            self,
            base_prompt: str,
            json_data: Dict,
            ai_client: Optional[OpenRouter] = None,
            registry: Optional[ChartRegistry] = None,
            # analyze_with_ai: bool = False,
    ):
        self.base_prompt = base_prompt or ""
        self.data = AuditData(json_data)
        self.ai = ai_client
        self.registry = registry or ChartRegistry().default_register_all()

    def generate_all_statistics(self) -> List[Dict[str, str]]:
        results: List[ChartResult] = []

        for chart in self.registry.all():
            # Render image
            image_b64 = chart.render(self.data)

            prompt = chart.build_ai_prompt(self.base_prompt, self.data.raw)
            analysis = self.ai.analyze(prompt)

            results.append(ChartResult(name=chart.name, image_b64=image_b64, analysis=analysis))

        return [r.to_dict() for r in results]
