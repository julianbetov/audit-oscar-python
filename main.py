import json

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from AuditAnalyzer import AuditAnalyzer
from report.builder import ReportBuilder
from report.pdf import render_pdf_bytes
from servicios.OpenRouter import OpenRouter
from servicios.Persistencia import Persistencia


def load_file_from_resource(file_name, file_type):
    with open(f"./recursos/{file_name}.{file_type}", "r") as file:
        return file.read()


def extract_json_block(text: str) -> str:
    return text.strip().removeprefix("```json").removesuffix("```").strip()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analisis")
async def analisis(auditoria_id: int):
    load_dotenv()

    # ----- Inicializar servicios -----
    ai_client = OpenRouter()
    servicio_persistencia = Persistencia()

    # ----- Construir propmts para IA -----
    audit_analysis_response_format = load_file_from_resource("analysis_response_format", "json")
    audit_analysis_prompt = load_file_from_resource("audit_analysis_prompt", "txt").replace(
        "{{ANALYSIS_RESPONSE_FORMAT}}", audit_analysis_response_format)
    chart_analysis_prompt = load_file_from_resource("chart_analysis_prompt", "txt")
    audit_data_json = servicio_persistencia.obtenerInformacionAuditoriaPorId(auditoria_id)
    audit_analysis_prompt = audit_analysis_prompt.replace("{{AUDIT_DATA}}", json.dumps(audit_data_json, indent=4))

    # ----- Obtener analisis de IA -----
    audit_analysis_json = ai_client.analyze(audit_analysis_prompt)
    audit_analysis_json = extract_json_block(audit_analysis_json)
    audit_analysis_json = json.loads(audit_analysis_json)
    # audit_analysis_json = json.loads(load_file_from_resource("example_analysis_response", "json"))

    # ----- Generar graficas -----
    charts_analyzer = AuditAnalyzer(chart_analysis_prompt, audit_analysis_json, ai_client)
    charts_results = charts_analyzer.generate_all_statistics()

    # ----- Generar un reporte HTML y PDF -----
    builder = ReportBuilder(template_path="report/templates/base.html")
    html_page = builder.build_complete_html(audit_analysis_json, audit_data_json, charts_results)
    pdf_bytes = render_pdf_bytes(html_page)

    # ----- Enviar resultados al servicio de java -----
    return servicio_persistencia.guardarArchivos(auditoria_id, pdf_bytes)
