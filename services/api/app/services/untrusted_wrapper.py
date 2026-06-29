import json

def wrap_output(source: str, raw: dict) -> str:
    payload = json.dumps(raw, ensure_ascii=False, indent=2)
    return f"""UNTRUSTED DATA - SOURCE: {source} - START
!!!!
{payload}
!!!!
UNTRUSTED DATA - SOURCE: {source} - END"""
