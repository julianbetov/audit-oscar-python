from typing import Any

import requests


class Persistencia:
    def __init__(self):
        self.base_url = "http://localhost:8081"
        self.timeout = 10

    def obtenerInformacionAuditoriaPorId(self, audit_id: int) -> dict:
        url = self.base_url + "/auditoria/" + str(audit_id)
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching audit data: {e}")
            return {}

    def guardarArchivos(self, audit_id: int, pdf: bytes) -> dict[str, Any]:
        url = self.base_url + "/archivo"
        data = {"auditoriaId": str(audit_id)}  # Como form data normal
        files = {
            "pdf": ("pdf", pdf, "application/pdf"),
        }
        try:
            response = requests.post(url, data=data, files=files, timeout=self.timeout)
            response.raise_for_status()
            try:
                return response.json()
            except ValueError:
                return {"status": response.status_code, "text": response.text}
        except requests.exceptions.RequestException as e:
            print(f"Error saving files: {e.response.text}")
            return e.response.json()