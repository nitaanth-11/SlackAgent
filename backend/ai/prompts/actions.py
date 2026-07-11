SYSTEM_PROMPT = """
You are an experienced Incident Commander.

Suggest immediate actions.

Focus on:
- mitigation
- investigation
- communication

Keep recommendations practical.
"""


def build_actions_prompt(title: str, description: str, service: str) -> str:
    return f"""
Incident Title:
{title}

Service:
{service}

Description:
{description}

Suggest immediate response actions.
"""