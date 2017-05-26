import os
import time
from slackclient import SlackClient
import modules.message_processing.main as message_process

# bot's id
BOT_ID = os.environ.get("BOT_ID")

# constants
#these 2 are mine id
TEACH1_ID = "U57B29A86" #U22JEU06N
TEACH2_ID = "U57B29A86"
AT_TEACHER = ("<@" + TEACH1_ID + ">","<@" + TEACH2_ID + ">")

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
            if output and 'text' in output and \
                    (AT_TEACHER[0] in output['text'] or AT_TEACHER[1] in output['text']):
                    text = output['text'].strip().replace(AT_TEACHER[0],'').\
                        replace(AT_TEACHER[1],'')

                    return text, output['channel']
    return None, None


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Sure...write some more code then I can do that!"
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

if __name__ == "__main__":
    READ_WEB_SOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print("Started!")
        while True:
            # create Multiset of questions after initializing
            message_process.create_multiset()

            # read messages and handle them
            command,channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command,channel)
            time.sleep(READ_WEB_SOCKET_DELAY)
    else:
        print("Connection failed")

