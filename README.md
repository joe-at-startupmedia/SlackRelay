# SlackRelay
Relay Input to a Slack Channel. This is designed for anyone wishing to share any text input (including a log file) in real time to a Slack channel. 

### Create Incoming Webhook

To get working, you will need to create an Incoming Webhook URL for your Slack team (https://api.slack.com/incoming-webhooks). 

### Start The Server

```
slackRelay.py -n [channel_username] -c [channel_name] -p [UDP port to listen on] -i [slack_hook_id]
```

The slack_hook_id is obtained from the webookurl: 

https://hooks.slack.com/services/ZZZZZZZZ/YYYYYYY/XXXXXXXXXXXXXXXXXXXXXXX

```
./slackRelay.py -p 9999 -n "Debugger" -c "#debugging" -i "ZZZZZZZZ/YYYYYYY/XXXXXXXXXXXXXXXXXXXXXXX"
```

This will listen on UDP port 9999 and post to the #debugging slack channel with the username Debuger.

### Send Data To The Server

Then pipe some log files at it. I suggest using netcat (nc), but any raw UDP client should work fine. Example:

```
tail -F /var/log/apache2/error.log | nc -u 127.0.0.1 9999
```
