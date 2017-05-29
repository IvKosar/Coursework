import os
from slackclient import SlackClient

BOT_NAME = 'spammer'

#slack_client = SlackClient(os.environ.get("SLACK_BOT_TOKEN"))
tokens = ["xoxb-176818620355-ehexY6lUksBblG3MX3xwizEZ",
          "xoxp-70140307553-78037962064-188319471891-172b09fd86060496fe4f98173058a3be"]
slack_client = SlackClient(tokens[0])


def get_user_id(username):
    """
    Get user id by Slack username
    
    :param username: Slack username
    :return: 
    """
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        users = api_call.get("members")
        for user in users:
            if 'name' in user and user.get('name') == username:
                print("User {0} ID is {1}".format(username, user.get('id')))
                return True

    else:
        print("Cant find token")

if __name__ == "__main__":
    username = "spammer"
    get_user_id(username)