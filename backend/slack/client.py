import os
from slack_bolt import App

_slack_app = None

def get_slack_app() -> App:
    global _slack_app
    if _slack_app is None:
        token = os.environ.get("SLACK_BOT_TOKEN")
        signing_secret = os.environ.get("SLACK_SIGNING_SECRET") or os.environ.get("SLACK_SIGNINIG_SECRET")
        
        _slack_app = App(
            token=token,
            signing_secret=signing_secret
        )
    return _slack_app
