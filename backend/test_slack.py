import config
from slack.client import get_slack_app

app = get_slack_app()

print("AUTH")
print(app.client.auth_test())

print("\nCHANNEL")
print(app.client.conversations_info(
    channel=config.DEFAULT_SLACK_CHANNEL
))

print("\nJOIN")
print(app.client.conversations_join(
    channel=config.DEFAULT_SLACK_CHANNEL
))

print("\nMEMBERS")
print(app.client.conversations_members(
    channel=config.DEFAULT_SLACK_CHANNEL
))