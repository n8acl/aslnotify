# Import Libraries
import config as cfg
import csv
import sys
import os
import json
import http.client, urllib
from datetime import datetime, date, time, timedelta
from discord_webhook import DiscordWebhook
from matrix_client.api import MatrixHttpApi

# Define Variables

status = ""
my_node = sys.argv[2]
their_node = sys.argv[3]
conn_status = sys.argv[1]
db_deliminater = "|"
node_info = ""

def send(status):
    if cfg.publish_matrix: # Send Matrix message
        matrix = MatrixHttpApi(cfg.matrix_server, token=cfg.matrix_token)
        response = matrix.send_message(cfg.matrix_room, status)

    if cfg.publish_telegram: # Send telegram message
        conn = http.client.HTTPSConnection("api.telegram.org")
        url = f"/bot{cfg.telegram_keys['apikey']}/sendMessage"
        payload = {
            "chat_id": cfg.telegram_keys["chat_id"],
            "text": status
        }
        payload_json = json.dumps(payload)
        headers = {
            "Content-Type": "application/json"
        }
        conn.request("POST", url, body=payload_json, headers=headers)
        conn.getresponse()

    if cfg.publish_discord: # Send Status to Discord
        for wh in cfg.discord_wh_url:
            webhook = DiscordWebhook(url=wh, content=status)
            response = webhook.execute()

    if cfg.publish_pushover: # Send Status to Pushover
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
            urllib.parse.urlencode({
            "token": cfg.pushover_token,
            "user": cfg.pushover_user,
            "message": status,
            }), { "Content-type": "application/x-www-form-urlencoded" })
        conn.getresponse()

def node_info(node_db):
    # Build Node Information
    # Open Node Database
    csvfile = open(node_db, "r", encoding="Latin-1")
    csvfile.seek
    reader = csv.reader(csvfile, dialect='excel', delimiter=db_deliminater, quotechar="'")

    # Search cvs for the node string

    for line in reader:
        if their_node in line:
            node_info = "(" + line[1] + " in " + line[3] + ")"
            break
        else:
            node_info = "(Info not in db)"

    csvfile.close()

    return node_info


# Check if their node is a blocked node and if it is disconnect it automatically and send a message that was disconnected
# Otherwise, send it through the notificaton control code.

if (their_node in cfg.blocked_nodes_list) and (my_node not in cfg.other_nodes_list):
    # Disconnect the node
    cmd = 'asterisk -rx "rpt fun ' + str(my_node) + ' *1' + str(their_node) + '"'
    os.system(cmd)

    # Notify me that it was auto disconnected
    status = status + "Blocked node " + str(their_node) + " " + node_info(cfg.node_db) + " was auto disconnected from " + str(my_node) + "."

    # send message
    send(status)
else:
    now = datetime.now()
    #build connect/disconnect message
    if (their_node not in cfg.my_nodes_list) and (their_node not in cfg.private_nodes_list):
        status = status + "Node " + str(their_node) + " " + node_info(cfg.node_db)
        if int(conn_status) == 1:
            status = status + " connected to "
        else:
            status = status + " disconnected from "

        if my_node == cfg.echolink_node:
            status = status + "Echolink (" + str(my_node) + ")"
        else:
            status = status + str(my_node)

        # send message
        status = status + " at " + now.strftime("%H:%M:%S")
        send(status)
