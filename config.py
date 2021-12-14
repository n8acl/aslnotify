
# For full explanation of these variables, please see the Configuration section of the Repo.

my_nodes_list = ["12345","54321"] # This is the list of your nodes
private_nodes_list = ["1999","1998"] # This is a list of the private nodes you connect to your node. This would be like Bridges.
other_nodes_list = ["67890", "67891"] # This is a list of other nodes you host, like a clubs node, on the same server
blocked_nodes_list = ["99999"] # These are nodes that you want to block from accessing any of your nodes.

# Telegram Configuration
publish_telegram = False # Enable/Disable Telegram Bot Notification

telegram_keys = { # These are the Bot API keys.
    "apikey": "BOT API KEY HERE",
    "chat_id": "YOUR CHAT ID HERE"
}

# Discord Configuration
publish_discord = False # Enable/Disable Discord Notifiations
discord_wh_url = 'DISCORD WEBHOOK URL HERE' # Your Discord Webhook for the channel you are connecting to.

# Pushover configuration
publish_pushover = False # Enable or disable notifications via Pushover
pushover_token = "1234567890" # Your Pushover API token
pushover_user = "abcdefghijklm" # Your Pushover user key
