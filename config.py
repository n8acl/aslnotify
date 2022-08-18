
# For full explanation of these variables, please see the Configuration section of the Repo.

my_nodes_list = ["54321","12345"] # This is the list of your nodes
private_nodes_list = ["1998","1997"] # This is a list of the private nodes you connect to your node. This would be like Bridges.
other_nodes_list = ["56789"] # This is a list of other nodes you host, like a clubs node, on the same server
blocked_nodes_list = ["99999"] # These are nodes that you want to block from accessing any of your nodes.
echolink_node = 1999 # This is your echolink node if you are using Echolink.
node_db = "/etc/asterisk/astdb.txt" # This is the location of the astdb.txt database. This could be in your Allmon2 directory or in your Asterisk Directory
db_deliminater = "|" # This is the deliminater used in the astdb.txt file.

# Telegram Configuration
publish_telegram = False # Enable/Disable Telegram Bot Notification

telegram_keys = { # These are the Bot API keys.
    "apikey": "BOT API KEY HERE",
    "chat_id": "YOUR CHAT ID HERE"
}

# Discord Configuration
publish_discord = True # Enable/Disable Discord Notifiations
discord_wh_url = ['YOUR DISCORD HOOK HERE','YOUR SECOND DISCORD HOOK HERE'] # Your Discord Webhook for the channel you are connecting to.

# Pushover configuration
publish_pushover = False # Enable or disable notifications via Pushover
pushover_token = "1234567890" # Your Pushover API token
pushover_user = "abcdefghijklm" # Your Pushover user key
