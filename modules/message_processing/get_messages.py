# Gets messages from Slack channel
#
# Created by Ivan Kosarevych 04.05.17 18:01:34

from slackclient import SlackClient

TOKEN = 'xoxp-70140307553-78037962064-164065837697-e33f8b961930b0ceb61674d4172d1063'

# initialize slackclient
slackclient = SlackClient(TOKEN)

# programming_2016_2017 channel id
CHANNEL_ID = "G4K508JUA"
# Romanyuk's ID
TEACHER0_ID = "U2B5102ES"
# Oles's ID
TEACHER1_ID = "U22JEU06N"


def test():
    return slackclient.api_call("api.test").get("ok")

def get_user_id(username):
    response = slackclient.api_call("users.list")
    members = response.get("members")
    for member in members:
        if member.get("name") == username:
            return member.get("id")


def get_channels_id(channel_name):
    response = slackclient.api_call("groups.list")
    groups = response.get("groups")
    for group in groups:
        if group.get("name_normalized") == channel_name:
            return (group.get("id"))


def get_messages(channel_id):
    response = slackclient.api_call("groups.history",
                                    channel=channel_id)
    messages = response.get("messages")
    print(len(messages))
    return (messages)

def write_to_file(data):
    with open("messages","w") as file:
        res_str = ''
        for element in data:
            res_str += str(element) + '\n'

        file.write(res_str)

if __name__ == "__main__":
    #get_channels_id("programming_2016_2017")
    #print(get_messages(CHANNEL_ID))
    #print(get_user_id("a.romanyuk"))
    write_to_file(get_messages(CHANNEL_ID))