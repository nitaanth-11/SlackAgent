from slack_bolt import App


def register_events(app: App):

    @app.event("app_mention")
    def handle_app_mention(body, say, logger):
        """Respond when someone @mentions the bot."""
        logger.info("Received app_mention event.")
        try:
            user_id = body["event"]["user"]
            say(
                f"Hey <@{user_id}>! :wave: I'm *OpsPilot*.\n\n"
                f"Use `/incident` to report a new incident.\n"
                f"I'll track severity, ownership, and resolution right here in Slack."
            )
        except Exception as e:
            logger.error(f"Error handling app_mention: {e}")
