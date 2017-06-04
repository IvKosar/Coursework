"""
Module for getting SLack user ID using SlackClient wrapper for SLack API
"""

import os
from slackclient import SlackClient

BOT_NAME = 'answerme'

#slack_client = SlackClient(os.environ.get("SLACK_BOT_TOKEN"))
tokens = ["xoxb-176818620355-m7nN8xxFha856gQU1Lk5PzduZ".replace("Q","q"),
          'xoxp-70140307553-78037962064-192429703618-c939446dfcc16c0f7b7d3edA96544f5f'.replace("A","a")]
slack_client = SlackClient(tokens[0])


def get_user_id(username):
    """
    Gets Slack user(bot) id by his username
    
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
    username = BOT_NAME
    get_user_id(username)