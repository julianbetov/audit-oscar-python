import matplotlib.pyplot as plt

from BaseChart import BaseChart


class ResponseDistributionChart(BaseChart):
    def __init__(self):
        super().__init__(
            name="Distribución de Respuestas",
            description=(
                "Reads 'overall_summary.yes_count', 'overall_summary.no_count', "
                "'overall_summary.other_count', and 'overall_summary.total_questions' "
                "to render a pie chart of response distribution."
            ),
        )

    def draw(self, data) -> plt.Figure:
        fig, ax = plt.subplots(figsize=(10, 8))
        labels = ["Sí", "No", "Otro"]
        values = [
            data.get_summary_number("yes_count"),
            data.get_summary_number("no_count"),
            data.get_summary_number("other_count"),
        ]
        colors = ["#2ecc71", "#e74c3c", "#95a5a6"]
        explode = (0.05, 0.05, 0.0)
        wedges, texts, autotexts = ax.pie(
            values,
            labels=labels,
            colors=colors,
            autopct="%1.1f%%",
            explode=explode,
            shadow=False,
            startangle=90,
            textprops={"fontsize": 12, "weight": "bold"},
        )
        for autotext in autotexts:
            autotext.set_color("white")
            autotext.set_fontsize(14)
            autotext.set_weight("bold")

        total_q = int(data.get_summary_number("total_questions"))
        ax.set_title(f"Distribución de Respuestas\nTotal de Preguntas: {total_q}", fontsize=16, fontweight="bold",
                     pad=20)
        plt.tight_layout()

        # Remove this: (do not generate the image, just return the base64)
        plt.savefig("charts_image/" + self.name, dpi=300, bbox_inches="tight")
        return fig
