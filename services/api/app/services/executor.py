import json
import httpx
from app.services.crypto import decrypt_value

async def execute_http_tool(tool, key_record, arguments: dict):
    config = json.loads(tool.config_json) if isinstance(tool.config_json, str) else tool.config_json

    method = config["method"]
    url = config["url"]

    headers = {"Content-Type": "application/json"}
    if key_record:
        headers["Authorization"] = f"Bearer {decrypt_value(key_record.encrypted_value)}"

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.request(method=method, url=url, headers=headers, json=arguments)

        content_type = response.headers.get("content-type", "")
        body = response.json() if "application/json" in content_type else response.text

        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": body,
        }
