from ai.mock import mock_ai
def build_incident_blocks(incident: dict) -> list:
    """Build Block Kit blocks for an incident card in Slack."""

    severity_map = {
        "LOW": ":large_blue_circle: Low",
        "MEDIUM": ":large_yellow_circle: Medium",
        "HIGH": ":large_orange_circle: High",
        "CRITICAL": ":red_circle: Critical",
    }

    status_map = {
        "OPEN": ":rotating_light: Open",
        "ASSIGNED": ":eyes: Assigned",
        "INVESTIGATING": ":mag: Investigating",
        "RESOLVED": ":white_check_mark: Resolved",
    }

    severity_str = severity_map.get(incident.get("severity", "").upper(), incident.get("severity", ""))
    status_str = status_map.get(incident.get("status", "").upper(), incident.get("status", ""))
    owner = incident.get("owner") or "_Unassigned_"
    ai = incident.get("ai_enrichment", {})

    summary = ai.get("summary", "Not available")

    severity_ai = ai.get("severity", {})
    severity_text = (
        f"{severity_ai.get('label', 'Unknown')} "
        f"({int(severity_ai.get('confidence', 0) * 100)}%)"
    )

    causes = ai.get("probable_causes", [])
    cause_text = (
        causes[0]["cause"]
        if causes else "Unknown"
    )

    actions = ai.get("suggested_actions", [])
    actions_text = "\n".join(
        f"• {action}" for action in actions
    )
    incident_id = incident.get("incident_id", "???")

    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f":rotating_light: Incident Created",
                "emoji": True,
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*ID:*\n`{incident_id}`"},
                {"type": "mrkdwn", "text": f"*Severity:*\n{severity_str}"},
                {"type": "mrkdwn", "text": f"*Service:*\n{incident.get('service', 'N/A')}"},
                {"type": "mrkdwn", "text": f"*Status:*\n{status_str}"},
            ],
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Title:*\n{incident.get('title', '')}",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Description:*\n{incident.get('description', '')}",
            },
        },
        {
            "type": "context",
            "elements": [
                {"type": "mrkdwn", "text": f"*Owner:* {owner}"},
            ],
        },

        {"type": "divider"},

        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    "*🤖 AI Incident Analysis*\n\n"
                    f"*Summary:*\n{summary}\n\n"
                    f"*Predicted Severity:*\n{severity_text}\n\n"
                    f"*Most Likely Cause:*\n{cause_text}\n\n"
                    f"*Recommended Actions:*\n{actions_text}"
                ),
            },
        },

        {"type": "divider"},
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": ":bust_in_silhouette: Assign Owner", "emoji": True},
                    "style": "primary",
                    "value": incident_id,
                    "action_id": "assign_owner",
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": ":speech_balloon: Generate Update", "emoji": True},
                    "value": incident_id,
                    "action_id": "generate_update",
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": ":white_check_mark: Resolve", "emoji": True},
                    "style": "danger",
                    "value": incident_id,
                    "action_id": "resolve_incident",
                },
            ],
        },
    ]

    return blocks


def build_updated_blocks(incident: dict) -> list:
    """Build Block Kit blocks for an updated incident card (no action buttons if resolved)."""

    severity_map = {
        "LOW": ":large_blue_circle: Low",
        "MEDIUM": ":large_yellow_circle: Medium",
        "HIGH": ":large_orange_circle: High",
        "CRITICAL": ":red_circle: Critical",
    }

    status_map = {
        "OPEN": ":rotating_light: Open",
        "ASSIGNED": ":eyes: Assigned",
        "INVESTIGATING": ":mag: Investigating",
        "RESOLVED": ":white_check_mark: Resolved",
    }

    severity_str = severity_map.get(incident.get("severity", "").upper(), incident.get("severity", ""))
    status_str = status_map.get(incident.get("status", "").upper(), incident.get("status", ""))
    owner = incident.get("owner") or "_Unassigned_"
    incident_id = incident.get("incident_id", "???")
    is_resolved = incident.get("status", "").upper() == "RESOLVED"

    header_text = ":white_check_mark: Incident Resolved" if is_resolved else ":rotating_light: Incident Update"

    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": header_text,
                "emoji": True,
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*ID:*\n`{incident_id}`"},
                {"type": "mrkdwn", "text": f"*Severity:*\n{severity_str}"},
                {"type": "mrkdwn", "text": f"*Service:*\n{incident.get('service', 'N/A')}"},
                {"type": "mrkdwn", "text": f"*Status:*\n{status_str}"},
            ],
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Title:*\n{incident.get('title', '')}",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Description:*\n{incident.get('description', '')}",
            },
        },
        {
            "type": "context",
            "elements": [
                {"type": "mrkdwn", "text": f"*Owner:* {owner}"},
            ],
        },
    ]

    if not is_resolved:
        blocks.append({"type": "divider"})
        blocks.append({
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": ":bust_in_silhouette: Assign Owner", "emoji": True},
                    "style": "primary",
                    "value": incident_id,
                    "action_id": "assign_owner",
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": ":speech_balloon: Generate Update", "emoji": True},
                    "value": incident_id,
                    "action_id": "generate_update",
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": ":white_check_mark: Resolve", "emoji": True},
                    "style": "danger",
                    "value": incident_id,
                    "action_id": "resolve_incident",
                },
            ],
        })
    else:
        resolved_at = incident.get("resolved_at", "N/A")
        blocks.append({
            "type": "context",
            "elements": [
                {"type": "mrkdwn", "text": f":clock3: *Resolved at:* {resolved_at}"},
            ],
        })

    return blocks
