# Import Libraries
import config
import csv
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
node_db = config.node_db
node_db_deliminater = config.node_db_deliminater
node_info = ""

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

# Build Node Information
# Open Node Database
csvfile = open(node_db, "r", encoding="Latin-1")
csvfile.seek
reader = csv.reader(csvfile, dialect='excel', delimiter=node_db_deliminater, quotechar="'")

# Search cvs for the node string

for line in reader:
    if their_node in line:
      node_info = " (" + line[1] + " in " + line[3] + ")"
    else:
      node=info = " (Info not in db)"

csvfile.close()


# Check if their node is a blocked node and if it is disconnect it automatically and send a message that was disconnected
# Otherwise, send it through the notificaton control code.

if (their_node in config.blocked_nodes_list) and (my_node not in config.other_nodes_list):
    # Disconnect the node
    cmd = 'asterisk -rx "rpt fun ' + str(my_node) + ' *1' + str(their_node) + '"'
    os.system(cmd)

    # Notify me that it was auto disconnected
    status = status + "Blocked node " + str(their_node) + str(node_info) + " was auto disconnected from " + str(my_node) + "(Technology First Hub)."

    # send message
    send(status)
else:
    #build connect/disconnect message
    if (their_node not in config.my_nodes_list) and (their_node not in config.private_nodes_list):
        status = status + "Node " + str(their_node) + str(node_info)
        if int(conn_status) == 1:
            status = status + " connected to " + str(my_node) + "."
        else:
            status = status + " disconnected from " + str(my_node) + "."

        # send message
        send(status)
