from typing import Dict, Any, Optional
from backend.models.incident import Incident

def get_incident_modal() -> Dict[str, Any]:
    return {
        "type": "modal",
        "callback_id": "create_incident_modal",
        "title": {
            "type": "plain_text",
            "text": "Report an Incident"
        },
        "submit": {
            "type": "plain_text",
            "text": "Submit"
        },
        "close": {
            "type": "plain_text",
            "text": "Cancel"
        },
        "blocks": [
            {
                "type": "input",
                "block_id": "title_block",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "title_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Brief title summarizing the issue"
                    }
                },
                "label": {
                    "type": "plain_text",
                    "text": "Title"
                }
            },
            {
                "type": "input",
                "block_id": "severity_block",
                "element": {
                    "type": "static_select",
                    "action_id": "severity_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select severity level"
                    },
                    "options": [
                        {
                            "text": {"type": "plain_text", "text": "🔵 Low"},
                            "value": "low"
                        },
                        {
                            "text": {"type": "plain_text", "text": "🟡 Medium"},
                            "value": "medium"
                        },
                        {
                            "text": {"type": "plain_text", "text": "🟠 High"},
                            "value": "high"
                        },
                        {
                            "text": {"type": "plain_text", "text": "🔴 Critical"},
                            "value": "critical"
                        }
                    ]
                },
                "label": {
                    "type": "plain_text",
                    "text": "Severity"
                }
            },
            {
                "type": "input",
                "block_id": "description_block",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "description_input",
                    "multiline": True,
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Describe the details, impact, and steps to reproduce if applicable"
                    }
                },
                "label": {
                    "type": "plain_text",
                    "text": "Description"
                }
            }
        ]
    }

def get_announcement_blocks(incident: Incident, acknowledged_by: Optional[str] = None) -> list:
    severity_emoji = {
        "low": "🔵 Low",
        "medium": "🟡 Medium",
        "high": "🟠 High",
        "critical": "🔴 Critical"
    }.get(incident.severity.lower(), incident.severity)

    status_str = "Acknowledged" if acknowledged_by else "Open"
    status_emoji = "⏳" if acknowledged_by else "🚨"

    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"Incident #{incident.id or 'TBD'}: {incident.title}"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Description:*\n{incident.description}"
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"*Severity:* {severity_emoji}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Status:* {status_emoji} {status_str}"
                }
            ]
        }
    ]

    if acknowledged_by:
        blocks.append({
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"👤 *Acknowledged by:* <@{acknowledged_by}>"
                }
            ]
        })

    # Action buttons: Acknowledge and Resolve
    actions = []
    
    if not acknowledged_by:
        actions.append({
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "Acknowledge"
            },
            "style": "primary",
            "value": str(incident.id),
            "action_id": "acknowledge_incident"
        })

    actions.append({
        "type": "button",
        "text": {
            "type": "plain_text",
            "text": "Resolve"
        },
        "style": "danger",
        "value": str(incident.id),
        "action_id": "resolve_incident"
    })

    blocks.append({
        "type": "actions",
        "elements": actions
    })

    return blocks

def get_resolved_blocks(incident: Incident, resolved_by: str) -> list:
    severity_emoji = {
        "low": "🔵 Low",
        "medium": "🟡 Medium",
        "high": "🟠 High",
        "critical": "🔴 Critical"
    }.get(incident.severity.lower(), incident.severity)

    return [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"✅ Incident #{incident.id or 'TBD'} Resolved: {incident.title}"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Description:*\n{incident.description}"
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"*Severity:* {severity_emoji}"
                },
                {
                    "type": "mrkdwn",
                    "text": "*Status:* ✅ Resolved"
                },
                {
                    "type": "mrkdwn",
                    "text": f"👤 *Resolved by:* <@{resolved_by}>"
                }
            ]
        }
    ]
