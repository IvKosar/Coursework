# Gets messages from Slack channel
#
# Created by Ivan Kosarevych 04.05.17 18:01:34

from slackclient import SlackClient

TOKEN = 'xoxp-70140307553-78037962064-188319471891-172b09fd86060496fe4f98173058a3be'

# initialize slackclient
slackclient = SlackClient(TOKEN)

# programming_2016_2017 channel id
CHANNEL_ID = "G4K508JUA"
# Andriy Romanyuk's ID
TEACHER0_ID = "U2B5102ES"
# Oles's ID
TEACHER1_ID = "U22JEU06N"


def test():
    return slackclient.api_call("api.test").get("ok")

def get_channels_id(channel_name):
    response = slackclient.api_call("groups.list")
    groups = response.get("groups")
    for group in groups:
        if group.get("name_normalized") == channel_name:
            return (group.get("id"))


def get_messages(channel_id):
    response = slackclient.api_call("groups.history",
                                    channel=channel_id, count=26)
    messages = response.get("messages")
    return messages

def write_to_file(data):
    with open("new_messages","a") as file:
        res_str = ''
        for element in data:
            res_str += str(element) + '\n'

        file.write(res_str)

if __name__ == "__main__":
    from pprint import pprint
    #get_channels_id("programming_2016_2017")
    pprint(get_messages(CHANNEL_ID))
    #write_to_file(get_messages(CHANNEL_ID))