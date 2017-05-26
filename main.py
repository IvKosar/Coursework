import os
import time
from slackclient import SlackClient
import modules.message_processing.main as message_process

# bot's id
BOT_ID = os.environ.get("BOT_ID")

# constants
#these 2 are my id
TEACH1_ID = "U57B29A86" #U22JEU06N
TEACH2_ID = "U57B29A86"
AT_TEACHER = ("<@" + TEACH1_ID + ">","<@" + TEACH2_ID + ">")

# initialize questions_base
QUESTIONS_BASE = message_process.create_multiset()

# initialize slack client
slack_client = SlackClient(os.environ.get("SLACK_BOT_TOKEN"))

def parse_slack_output(slack_rtm_output):
    """
    :param slack_rtm_output: 
    :return: str
    This function parses for messages in Slack channel addressed to teachers 
    using Slack Real Time Messaging API
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output:
                    user = output['user']
                    text = output['text'].strip()
                    return text, output['channel'], user
    return None, None, None


def handle_message(message, channel, user):
    """
        Receives messages from channel and process it.
        If it's a question find most similar to given.
        If in the questions base there are no similar question
        add to questions base
    """
    if user == BOT_ID:
        # TO FINISH
        return

    answer = message_process.main(message, QUESTIONS_BASE)
    if answer:
        response = "<@" + user + ">" + " " + answer + '\n' + \
                    "Якщо відповідь була корисною відреагуйте пальцем вверх =)"
    else:
        response = "<@" + TEACH1_ID + ">" + "<@" + TEACH2_ID + ">"
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

if __name__ == "__main__":
    READ_WEB_SOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print("Started!")
        while True:
            # read messages and handle them
            message,channel, user = parse_slack_output(slack_client.rtm_read())
            if command and channel and user:
                handle_message(message,channel, user)
            time.sleep(READ_WEB_SOCKET_DELAY)
    else:
        print("Connection failed")

