from slack_bolt import App

def register_events(app: App):
    @app.event("app_mention")
    def handle_app_mentions(body, say, logger):
        logger.info("Received app_mention event.")
        try:
            user_id = body["event"]["user"]
            say(f"Hello <@{user_id}>! I am *OpsPilot*. You can use the `/incident` command to report and track incidents directly from Slack.")
        except Exception as e:
            logger.error(f"Error handling app_mention: {e}")
