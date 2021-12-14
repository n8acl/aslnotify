# Import Libraries
import config
import sys
import os
import json
import http.client, urllib
from discord_webhook import DiscordWebhook

# Define Variables

status = "ALLSTAR ALERT: "
my_node = sys.argv[2]
their_node = sys.argv[3]
conn_status = sys.argv[1]

def send(status):
    if config.publish_telegram: # Send telegram message
        cmd = 'curl -s "https://api.telegram.org/bot' + config.telegram_keys["apikey"] + "/sendmessage?chat_id=" + config.telegram_keys["chat_id"] + "&text=" + status +'"'
        os.system(cmd)

    if config.publish_discord: # Send Status to Discord
        webhook = DiscordWebhook(url=config.discord_wh_url, content=status)
        response = webhook.execute()

    if config.publish_pushover: # Send Status to Pushover
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
            urllib.parse.urlencode({
            "token": config.pushover_token,
            "user": config.pushover_user,
            "message": status,
            }), { "Content-type": "application/x-www-form-urlencoded" })
        conn.getresponse()  

# Check if their node is a blocked node and if it is disconnect it automatically and send a message that was disconnected
# Otherwise, send it through the notificaton control code.

if (their_node in config.blocked_nodes_list) and (my_node not in config.other_nodes_list):
    # Disconnect the node
    cmd = 'asterisk -rx "rpt fun ' + str(my_node) + ' *1' + str(their_node) + '"'
    os.system(cmd)

    # Notify me that it was auto disconnected
    status = status + "Blocked node " + str(their_node) + " was auto disconnected from " + str(my_node) + "."

    # send message
    send(status)
else:
    #build connect/disconnect message
    if (their_node not in config.my_nodes_list):
        status = status + "Node " + str(their_node) 
        if int(conn_status) == 1:
            status = status + " connected to "
        else:
            status = status + " disconnected from "

        # send message
        send(status)
