from pathlib import Path
from typing import Dict, Any, List


class ReportBuilder:
    def __init__(self, template_path: str | None = None):
        self.template_path = Path(template_path) if template_path else None

    def _load_template(self) -> str:
        if self.template_path and self.template_path.is_file():
            return self.template_path.read_text(encoding="utf-8")
        return (
            "<!DOCTYPE html>"
            "<html lang='en'><head><meta charset='UTF-8'>"
            "<title>Reporte de Auditoria</title>"
            "<style>"
            "body{font-family:Arial,sans-serif;margin:40px;background:#f9f9f9}"
            "h2{color:#2c3e50}"
            "section{background:#fff;padding:24px;border-radius:8px;box-shadow:0 2px 8px #ccc;margin-bottom:40px}"
            "img{max-width:600px;display:block;margin:0 auto 16px auto}"
            "</style></head><body>"
            "<h1>Reporte de Auditoria</h1>"
            "{{EQUIPO_AUDITOR}}"
            "{{AUDIT_INFO}}"
            "{{REGISTRIES}}"
            "{{RESULT_SECTIONS}}"
            "</body></html>"
        )

    def render_audit_info(self, data: Dict[str, Any]) -> str:
        id = data.get("id", "")
        fecha = data.get("fecha", "")
        totalDeRegistros = data.get("totalDeRegistros", "")
        return (
            "<section>"
            "<h2>Información y Metadatos</h2>"
            "<table style='width:100%;border-collapse:collapse;background:#fff'>"
            "<tbody>"
            "<tr><th style='border:1px solid #ccc;padding:8px;text-align:left'>Fecha de Registro</th>"
            f"<td style='text-align:center; border:1px solid #ccc;padding:8px'>{fecha}</td></tr>"
            "<tr><th style='border:1px solid #ccc;padding:8px;text-align:left'>Identificador de la Auditoria</th>"
            f"<td style='text-align:center; border:1px solid #ccc;padding:8px'>{id}</td></tr>"
            "<tr><th style='border:1px solid #ccc;padding:8px;text-align:left'>Cantidad de Preguntas Analizadas</th>"
            f"<td style='text-align:center; border:1px solid #ccc;padding:8px'>{totalDeRegistros}</td></tr>"
            "</tbody></table></section>"
        )

    def render_registries_table(self, data: Dict[str, Any]) -> str:
        registries = data.get("registros", [])
        rows = "".join(
            [
                (
                    "<tr>"
                    f"<td style='border:1px solid #ccc;padding:8px'>{reg.get('pregunta', '')}</td>"
                    f"<td style='border:1px solid #ccc;padding:8px'>{reg.get('respuesta', '')}</td>"
                    f"<td style='border:1px solid #ccc; padding:8px'>{reg.get('observacion', '')}</td>"
                    "</tr>"
                )
                for reg in registries
            ]
        )
        return (
            "<section>"
            "<h2>Registros de la Auditoria</h2>"
            "<table style='width:100%;border-collapse:collapse;background:#fff'>"
            "<thead>"
            "<tr>"
            "<th style='border:1px solid #ccc;padding:8px'>Pregunta</th>"
            "<th style='border:1px solid #ccc;padding:8px'>Respuesta</th>"
            "<th style='border:1px solid #ccc;padding:8px'>Observacion</th>"
            "</tr>"
            "</thead>"
            f"<tbody>{rows}</tbody></table></section>"
        )

    def render_students_data(self) -> str:
        return (
            "<section>"
            "<h2>Equipo Auditor</h2>"
            "<table style='width:100%;border-collapse:collapse;background:#fff'>"
            "<tbody>"
            "<tr><th style='border:1px solid #ccc;padding:8px;text-align:left'>Nombre Completo</th>"
            "<th style='border:1px solid #ccc;padding:8px;text-align:left'>Código Institucional</th></tr>"
            "<tr><td style='border:1px solid #ccc;padding:8px'>Jaider Alexander Rodriguez Castañeda</td>"
            "<td style='border:1px solid #ccc;padding:8px'>118695</td></tr>"
            "<tr><td style='border:1px solid #ccc;padding:8px'>Oscar Daniel Ramirez Arias</td>"
            "<td style='border:1px solid #ccc;padding:8px'>111876</td></tr>"
            "<tr><td style='border:1px solid #ccc;padding:8px'>Jinneth Valentina Guayazan Guerrero</td>"
            "<td style='border:1px solid #ccc;padding:8px'>118695</td></tr>"
            "</tbody></table></section>"
        )

    def render_complete_analysis(self, data: Dict[str, Any]) -> str:
        complete_analysis = data.get("analysis_metadata", "").get("complete_analysis", "")
        return (
            "<section>"
            "<h2>Análisis Completo de Auditoria - Conclusiones y Recomendaciones</h2>"
            f"<p>{complete_analysis}</p>"
            "</section>"
        )

    def render_chart_sections(self, data: List[Dict[str, str]]) -> str:
        sections = []
        for result in data:
            title = (result.get("name") or "").replace("_", " ").title()
            img_b64 = result.get("image", "")
            analysis = result.get("analysis", "") or ""
            sections.append(
                "<section>"
                f"<h2>{title}</h2>"
                f"<img src='data:image/png;base64,{img_b64}' alt='{result.get('name', 'chart')}'>"
                f"<p>{analysis}</p>"
                "</section>"
            )
        return "".join(sections)

    def build_complete_html(self, json_data: Dict, audit_json: Dict[str, Any], results: List[Dict[str, str]]) -> str:
        template = self._load_template()
        html = template.replace("{{AUDIT_ANALYSIS}}", self.render_complete_analysis(json_data))
        html = html.replace("{{EQUIPO_AUDITOR}}", self.render_students_data())
        html = html.replace("{{AUDIT_INFO}}", self.render_audit_info(audit_json))
        html = html.replace("{{REGISTRIES}}", self.render_registries_table(audit_json))
        html = html.replace("{{RESULT_SECTIONS}}", self.render_chart_sections(results))
        return html
