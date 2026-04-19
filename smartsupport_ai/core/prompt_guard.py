import re
from fastapi import HTTPException, Request

MALICIOUS_PATTERNS = [
    r"ignore previous instructions",
    r"system prompt",
    r"delete all",
    r"drop table",
    r"bypass safety",
    r"reveal your secrets"
]

class PromptGuard:
    @staticmethod
    def scan(text: str):
        for pattern in MALICIOUS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

async def prompt_guard_middleware(request: Request, call_next):
    if request.method == "POST":
        body = await request.form()
        message = body.get("message", "")
        if PromptGuard.scan(message):
            raise HTTPException(
                status_code=403, 
                detail="Security Alert: Malicious prompt pattern detected."
            )
    return await call_next(request)
