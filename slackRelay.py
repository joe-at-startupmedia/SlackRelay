#!/usr/bin/env python3
#This python script creates a simple UDP server which will relay all incoming text to a Slack channel
import socketserver
import requests
import json
import sys, getopt

_webhook_url = 'https://hooks.slack.com/services/'

DEBUG = False
HOST = "127.0.0.1"
PORT = None         #UDP port to listen on
name = None         #Name of the slack channel username
channel = None      #Name of the slack channel
webhook_url = None  #The slack webhook URL

def main(argv):
  global DEBUG
  global PORT
  global name
  global channel
  global webhook_url

  try:
    opts, args = getopt.getopt(argv,"hdp:n:c:i:")
  except getopt.GetoptError:
    about_and_abort() 
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      about()
      sys.exit()
    elif opt == "-p":
      PORT = int(arg)
    elif opt == "-n":
      name  = arg
    elif opt == "-c":
      channel = arg
    elif opt == "-i":
      slack_hook_id = arg
      webhook_url = _webhook_url + slack_hook_id
    elif opt == "-d":
      DEBUG = True
  
  if PORT is None:
    about_and_abort("Port (-p) is required.")
  elif name is None:
    about_and_abort("Channel username (-n) is required.")
  elif channel is None:
    about_and_abort("Channel name (-c) is required.")
  elif webhook_url is None:
    about_and_abort("Slack Hook ID (-i) is required.")

  server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
  server.serve_forever()


def about():
  print("slackRelay.py -n [channel_username] -c [channel_name] -p [UDP port to listen on] -i [slack_hook_id]")

def about_and_abort(msg): 
  print(msg)
  about()
  sys.exit(2)

def slackpost(msg):
  slack_data = {'channel': channel, 'username': name, 'text': msg, 'icon_emoji': ':ghost:'}
  response = requests.post(
    webhook_url, data=json.dumps(slack_data),
    headers={'Content-Type': 'application/json'}
  )

class MyUDPHandler(socketserver.BaseRequestHandler):
  def handle(self):
    data = self.request[0].strip()
    socket = self.request[1]
    dataclean = str(data, errors='ignore')
    slackpost(dataclean)
    if DEBUG:
      print("{} sent:".format(self.client_address[0]))
      print(data)
      socket.sendto((data), self.client_address)

if __name__ == "__main__":
  main(sys.argv[1:])
