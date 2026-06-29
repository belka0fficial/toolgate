def classify_wrapped_output(text: str) -> dict:
    flags = []
    lower = text.lower()

    suspicious_patterns = [
        "ignore previous instructions",
        "system prompt",
        "developer message",
        "reveal secrets",
        "authorization:",
        "call tool",
    ]

    for pattern in suspicious_patterns:
        if pattern in lower:
            flags.append(pattern)

    return {
        "risk_level": "high" if flags else "low",
        "flags": flags,
    }
