"""Ядро клиента Yandex Direct API v5 (JSON), только stdlib.

Документация: https://yandex.ru/dev/direct/doc/ — раздел «Справочник API (v5)».
Auth: OAuth-токен в env YANDEX_DIRECT_TOKEN (Bearer). Sandbox включается флагом.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass

PROD_BASE = "https://api.direct.yandex.com/json/v5/"
SANDBOX_BASE = "https://api-sandbox.direct.yandex.com/json/v5/"
REPORTS_PATH = "reports"


class DirectError(RuntimeError):
    """Ошибка API (тело error{} в ответе) или транспорт."""

    def __init__(self, message, code=None, detail=None, request_id=None):
        super().__init__(message)
        self.code = code
        self.detail = detail
        self.request_id = request_id


@dataclass
class Units:
    """Расход баллов из заголовка `Units`: spent/last-call/daily-limit."""
    spent: int = 0
    last: int = 0
    daily_limit: int = 0

    @classmethod
    def parse(cls, header):
        try:
            a, b, c = (header or "").split("/")
            return cls(int(a), int(b), int(c))
        except Exception:
            return cls()


class DirectClient:
    """Тонкий JSON-клиент. Один метод вызова + хелперы.

    sandbox=True (по умолчанию) — безопасная песочница, спенда нет.
    dry_run=True — payload печатается/возвращается, запрос НЕ отправляется.
    """

    def __init__(self, token=None, sandbox=True, dry_run=False, lang="ru", timeout=60):
        self.token = token or os.environ.get("YANDEX_DIRECT_TOKEN")
        self.sandbox = sandbox
        self.dry_run = dry_run
        self.lang = lang
        self.timeout = timeout
        self.base = SANDBOX_BASE if sandbox else PROD_BASE
        self.last_units = Units()
        if not self.token and not dry_run:
            raise DirectError(
                "Нет токена. Задайте env YANDEX_DIRECT_TOKEN или используйте dry_run=True."
            )

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token or 'DRY-RUN'}",
            "Accept-Language": self.lang,
            "Content-Type": "application/json; charset=utf-8",
        }

    def call(self, service, method, params):
        """Вызов {service}.{method}(params). Возвращает result или бросает DirectError."""
        url = self.base + service
        body = json.dumps({"method": method, "params": params}, ensure_ascii=False)
        if self.dry_run:
            print(f"[DRY-RUN] POST {url}\n{body}")
            return {"dry_run": True, "service": service, "method": method, "params": params}
        data = body.encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=self._headers(), method="POST")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                self.last_units = Units.parse(resp.headers.get("Units"))
                payload = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            raise DirectError(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:500]}")
        except urllib.error.URLError as e:
            raise DirectError(f"Сеть: {e}")
        if "error" in payload:
            err = payload["error"]
            raise DirectError(
                err.get("error_string", "API error"),
                code=err.get("error_code"),
                detail=err.get("error_detail"),
                request_id=err.get("request_id"),
            )
        return payload.get("result", payload)

    def get_report(self, report_definition):
        """Статистика через сервис Reports (TSV). report_definition — dict ReportDefinition.

        Заголовки: processingMode=auto, returnMoneyInMicros=false, skipReportSummary=true.
        Возвращает сырой TSV-текст (для этапа 9). В dry_run печатает запрос.
        """
        url = self.base + REPORTS_PATH
        body = json.dumps({"params": report_definition}, ensure_ascii=False)
        if self.dry_run:
            print(f"[DRY-RUN] POST {url}\n{body}")
            return ""
        headers = dict(self._headers())
        headers.update({
            "processingMode": "auto",
            "returnMoneyInMicros": "false",
            "skipReportSummary": "true",
        })
        req = urllib.request.Request(url, data=body.encode("utf-8"), headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            raise DirectError(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:500]}")
