import sqlite3
import json
from datetime import datetime
from mitmproxy import http

# Database setup
DB_PATH = "/proxy/logs/logs.db"

def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            method TEXT,
            url TEXT,
            request_headers TEXT,
            request_body TEXT,
            response_status INTEGER,
            response_headers TEXT,
            response_body TEXT,
            duration_ms REAL
        )
    ''')
    conn.commit()
    conn.close()

setup_database()

class APILogger:
    def __init__(self):
        self.flows = {}

    def request(self, flow: http.HTTPFlow) -> None:
        # Only log Mistral API calls
        if "api.mistral.ai" in flow.request.pretty_host:
            self.flows[flow] = datetime.now()

    def response(self, flow: http.HTTPFlow) -> None:
        if flow not in self.flows:
            return

        start_time = self.flows[flow]
        duration = (datetime.now() - start_time).total_seconds() * 1000

        # Extract request data
        request_body = flow.request.content.decode('utf-8', errors='replace') if flow.request.content else ""
        response_body = flow.response.content.decode('utf-8', errors='replace') if flow.response.content else ""

        # Store in database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO api_logs (
                timestamp, method, url, request_headers, request_body,
                response_status, response_headers, response_body, duration_ms
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            start_time.isoformat(),
            flow.request.method,
            flow.request.pretty_url,
            json.dumps(dict(flow.request.headers)),
            request_body,
            flow.response.status_code,
            json.dumps(dict(flow.response.headers)),
            response_body,
            duration
        ))
        conn.commit()
        conn.close()

        del self.flows[flow]

addons = [APILogger()]
