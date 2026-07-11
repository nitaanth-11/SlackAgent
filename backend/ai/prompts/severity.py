SYSTEM_PROMPT = """
You are an SRE.

Predict the incident severity.

Return:
- label
- confidence
- reason

Do not invent information.
"""


def build_severity_prompt(title: str, description: str, service: str) -> str:
    return f"""
Incident Title:
{title}

Service:
{service}

Description:
{description}

Predict the severity.
"""