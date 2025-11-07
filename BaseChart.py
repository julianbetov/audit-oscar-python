import io
import base64
from abc import ABC, abstractmethod
from typing import Optional

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class BaseChart(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        sns.set_style("whitegrid")
        plt.rcParams.update({
            "figure.figsize": (12, 8),
            "font.size": 10,
            "axes.titlesize": 14,
            "axes.labelsize": 12,
        })

    @abstractmethod
    def draw(self, data) -> plt.Figure:
        ...

    def fig_to_b64(self, fig: plt.Figure) -> str:
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
        plt.close(fig)
        buf.seek(0)
        img_b64 = base64.b64encode(buf.read()).decode("utf-8")
        buf.close()
        return img_b64

    def render(self, data) -> str:
        fig = self.draw(data)
        print(f"        - Rendering {self.name} chart...")
        return self.fig_to_b64(fig)

    def build_ai_prompt(self, base_prompt: str, data_json: dict) -> str:
        return f"{base_prompt}\nTHE FUNCTION YOU WORK WITH:\n{self.description}\nJSON AUDIT ANALYSIS RESULTS:\n{data_json}"
