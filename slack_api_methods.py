from slacker import Slacker

slack = Slacker('xoxp-70140307553-78037962064-162829128855-0e7cdf3560227ebb451d21d66a2fd0db')

response = slack.users.list()
users = response.body['members']
#print(users)

response = slack.channels.list()
print(response.body)
