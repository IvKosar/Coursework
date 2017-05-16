import os
from slackclient import SlackClient

BOT_NAME = 'spammer'

slack_client = SlackClient(os.environ.get("SLACK_BOT_TOKEN"))


if __name__ == "__main__":
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        users = api_call.get("members")
        for user in users:
            if 'name' in user and user.get('name') == 'kosarevych':
                print("My ID is",user.get('id'))
            else:
                print("Can not find bot user")

    else:
        print("Cant find token")
