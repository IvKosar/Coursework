"""
# This module is bot interface.
# Connect to SlackClient via generated token
# Check for events through Slack Real Time Messaging API
# Detect messages(search for text in output)
# Handle these messages by calling function from module main in message_processing package
# Give response to the message if it was a question
"""

import os
import time
import modules.message_processing.main as message_process
from slackclient import SlackClient
from modules.my_multiset.questions_dict import Questions_dict

# bot's id
BOT_ID = "U56Q2J8AF"

# Slack ids of teachers
# currently these 2 are my id as I don't have enough permissions
TEACH1_ID = "U57B29A86" #U22JEU06N
TEACH2_ID = "U57B29A86"

# initialize questions_base
QUESTIONS_BASE = message_process.create_multiset()
NON_ANSWERED_QUESTIONS = Questions_dict()

# initialize slack client
slack_client = SlackClient("xoxb-176818620355-eHexY6lUksBblG3MX3xwizEZ".replace("H","h"))

def parse_slack_output(slack_rtm_output):
    """
    Parse for messages in Slack channel Slack Real Time Messaging API
    Return text, channel, user, who typed this message

    :param slack_rtm_output: json file with events in Slack converted to dict
    :return: tuple(str)
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
        Process received messages by delegating it to supporting function
        Based on response from this function post message with answer or call teachers
        or do nothing if it wasn't a question

        :param message: text of received message
        :param channel: channel id where message was posted
        :param user: user id, who posted message
        :return: None
    """
    # Don't answer to himself
    if user == BOT_ID:
        return

    # process message in supporting function
    # if its response is str and is not a part of the message post answer to the channel
    # if it responses with str and it's a part of message(addressee removed)
    #  (means the message was a question but there is no similar in question base)
    # call teachers to answer
    # if response is 1 means the message was the answer to unanswered question,
    # post thankful message to teacher
    # if it responses with 0, means the message was neither a question nor an answer
    answer = message_process.main(message, QUESTIONS_BASE, NON_ANSWERED_QUESTIONS, user)
    if answer and answer is not 1 and answer not in message:
        response = "<@" + user + ">" + " " + answer + '\n' + \
                    "Якщо відповідь була корисною відреагуйте пальцем вверх =)"
    elif answer in message:
        response = "<@" + TEACH1_ID + ">" + "<@" + TEACH2_ID + ">" + " " + message + \
            "\n" + "Please answer to " + "<@" + user + ">" +\
            "using this this tag"
    elif answer is 1:
        response = "Thank you for the answer!"
    else:
        return

    # post response to the channel
    if response:
        slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

if __name__ == "__main__":
    READ_WEB_SOCKET_DELAY = 1
    # connect to Slack RTM API
    if slack_client.rtm_connect():
        print("Started!")
        while True:
            # read messages and handle them
            message,channel, user = parse_slack_output(slack_client.rtm_read())
            if message and channel and user:
                handle_message(message,channel, user)
            time.sleep(READ_WEB_SOCKET_DELAY)
    else:
        print("Connection failed")
