import matplotlib.pyplot as plt
import numpy as np

from BaseChart import BaseChart


class OverallComplianceChart(BaseChart):
    def __init__(self):
        super().__init__(
            name="cumplimiento_general",
            description=(
                "This function extracts 'overall_summary.compliance_percentage', "
                "'overall_summary.yes_count', and 'overall_summary.no_count' to calculate "
                "the global compliance rate. It maps the percentage to a semicircular gauge "
                "plot by converting the compliance ratio into an angular span (0–π radians). "
                "The gauge’s fill arc reflects performance proportionally, and color-coding "
                "follows thresholds: green for >=80%, orange for 60–79%, and red for <60%. "
                "This visualization quantifies and categorizes the audit’s overall compliance status."
            ),
        )

    def draw(self, data) -> plt.Figure:
        fig, ax = plt.subplots(figsize=(10, 8))
        compliance = data.summary.get('compliance_percentage', 0)
        if compliance >= 80:
            color = '#2ecc71'
            status = 'BUENO'
        elif compliance >= 60:
            color = '#f39c12'
            status = 'REGULAR'
        else:
            color = '#e74c3c'
            status = 'DEFICIENTE'

        theta = np.linspace(0, np.pi, 100)
        r = 1
        ax.plot(r * np.cos(theta), r * np.sin(theta), 'lightgray', linewidth=25, alpha=0.3)
        theta_cumplimiento = np.linspace(0, np.pi * (compliance / 100), 100)
        ax.plot(r * np.cos(theta_cumplimiento), r * np.sin(theta_cumplimiento),
                color=color, linewidth=25)
        ax.text(0, 0.3, f'{compliance:.1f}%',
                ha='center', va='center', fontsize=48, fontweight='bold', color=color)
        ax.text(0, -0.1, status,
                ha='center', va='center', fontsize=20, color=color, weight='bold')
        ax.text(0, -0.35, 'Cumplimiento General',
                ha='center', va='center', fontsize=14, color='gray')
        for angle, label in [(0, '0%'), (np.pi / 2, '50%'), (np.pi, '100%')]:
            x = 1.15 * np.cos(angle)
            y = 1.15 * np.sin(angle)
            ax.text(x, y, label, ha='center', va='center', fontsize=10, color='gray')
        ax.set_xlim(-1.4, 1.4)
        ax.set_ylim(-0.5, 1.4)
        ax.axis('off')
        ax.set_title('Indicador de Cumplimiento Global', fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()

        # Remove this: (do not generate the image, just return the base64)
        plt.savefig("charts_image/" + self.name, dpi=300, bbox_inches="tight")
        return fig
