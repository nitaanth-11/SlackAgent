from slack_bolt import App

try:
    import config
except ImportError:
    from backend import config


_slack_app = None


def get_slack_app() -> App:
    global _slack_app

    if _slack_app is None:
        _slack_app = App(
            token=config.SLACK_BOT_TOKEN,
            signing_secret=config.SLACK_SIGNING_SECRET,
        )

    return _slack_app