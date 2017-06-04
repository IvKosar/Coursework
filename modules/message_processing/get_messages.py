# Test Python wrapper for Slack
# Get messages from Slack channel, Slack channel id
# Created by Ivan Kosarevych 04.05.17 18:01:34

from slackclient import SlackClient

TOKEN = 'xoxp-70140307553-78037962064-192429703618-c939446dfcc16c0f7b7d3edA96544f5f'.replace("A","a")

# initialize slackclient
slackclient = SlackClient(TOKEN)

def test():
    return slackclient.api_call("api.test").get("ok")

def get_channels_id(channel_name):
    """
    Get Slack channel id by its name

    :param channel_name: str
    :return: str
    """
    response = slackclient.api_call("groups.list")
    groups = response.get("groups")
    for group in groups:
        if group.get("name_normalized") == channel_name:
            return (group.get("id"))


def get_messages(channel_id):
    """
    Get messages of given Slack channel

    :param channel_id: Slack channel ID
    :return: list(dict)
    """
    response = slackclient.api_call("groups.history",
                                    channel=channel_id)
    messages = response.get("messages")
    return messages

def write_to_file(data):
    """
    Write read messages to text file

    :param data: list
    :return: None
    """
    import os

    with open(os.getcwd() + "/docs/origin_messages.txt","w") as file:
        res_str = ''
        for element in data:
            res_str += str(element) + '\n'

        file.write(res_str)

if __name__ == "__main__":
    from pprint import pprint
    get_channels_id("programming_2016_2017")
    pprint(get_messages(CHANNEL_ID))
    write_to_file(get_messages(CHANNEL_ID))