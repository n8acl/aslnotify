# Allstarlink Notify (ASLNotify)
Notification/Access Control script for Allstarlink Nodes

---

## Description
[Allstarlink](https://www.allstarlink.org/) (ASL) is a VOIP Ham Radio Application that allows the linking of repeaters and radios and is based on the Asterisk PBX Telephony System.

ASL has a built in ability to run a script on the connection or disconnection of one node to another node. Many node owners use this functionality as a notification method to know when someone connects/disconnects to thier system. This is done via either email or text message, depending on how the owner has the script setup.

This script will send a notification to Telegram, Discord or via Pushover when a node connects or disconnects from your Allstarlink System. It will also allow you to block any nodes you would like to keep them from being able to connect to any of your nodes on your system. This is an easier blacklist then what is built into Allstarlink itself.

Since ASL only runs on Linux, the instructions here are based on that.

---

## Disclaimer
Know that you modify your ASL installation at your own risk. If you break your ASL system, I am not responsible, so make sure to read and make the best decisions for you.

---

## Installation/Setup
First make sure your system is up to date
```bash
sudo apt-get update && sudo apt-get -y upgrade
```

Next you will need to install Python3 and pip3 on your system if they are not already.
```bash
sudo apt-get install python3 python3-pip
```

Next you will need to install the discord-webhook python library if it's not already. This is for sending the notification to Discord:
```bash
pip3 install discord-webhook --upgrade
```

---

### API Keys Needed
If you are going to use Telegram for your notifications, you will need to get API keys for the following:
1. You will need to first either create a Telegram bot or use an existing one you own. If this is your first bot, you can use the [steps here](https://core.telegram.org/bots#6-botfather) and talk to @BotFather to create your bot. 
2. You will also need your Telegram chat id. This can be obtained once your bot is up and running by sending a message to your bot and using the Telegram API by going to this url: [https://api.telegram.org/bot'API-access-token'/getUpdates?offset=0](https://api.telegram.org/bot<API-access-token>/getUpdates?offset=0) replacing 'API-access-token' with your bot access token you obtained in the previous step, sans the single quotes. You will see some json and you will be able to find your ID there in the From stanza.
    * Note that Influx DB provides some examples of what to look for for the above 2 steps as well. You can go to their page by [clicking here](https://docs.influxdata.com/kapacitor/v1.5/event_handlers/telegram/).

If you are going to use Discord, you will need to setup a channel and then setup a webhook for that channel and then copy that webhook URL into the config file in the correct place.

If you are going to use Pushover, you will need to get an API token and have your User Key available from your account.

---

### Configure the Script
Once you have your API Keys, you will need to enter them into the configuration file along with modiying the variabls you need to make it all work. 

You will need to open the config.py file in your favorite text/Python editor and start editing. The following is an explanation of what all the variables mean and what they do.

#### Variables
- my_nodes_list = ["12345","54321"] 
  - This is a list of your personal nodes. If you have multiple personal nodes on the same server, list them here.
- private_nodes_list = ["1999","1998"] 
  - This is a list of the private nodes you connect to your node. This would be things like Bridges or voters or something. This list is used to verify against so that when private nodes are connected you don't get spammed with notifications.
- other_nodes_list = ["67890", "67891"] 
  - This is a list of other nodes you host, like a club's node or a friends node, on the same server as your personal nodes.
- blocked_nodes_list = ["99999"]
  - These are nodes that you want to block from accessing any of the nodes on your Allstar system.

- publish_telegram = False
  - Enable/Disable Telegram Bot Notification
    - Set True to Enable, False to disable

- telegram_keys = {
    "apikey": "BOT API KEY HERE",
    "chat_id": "YOUR CHAT ID HERE"
}
  - These are the keys you get from the BotFather and are your chat ID as mentioned above.

- publish_discord = False 
  - Enable/Disable Discord Notifiations
    - Set True to Enable, False to Disable
  
- discord_wh_url = 'DISCORD WEBHOOK URL HERE'
  - Your Discord Webhook for the channel you are connecting to.

- publish_pushover = False # Enable or disable notifications via Pushover
  - Enable/Disable Pushover Notifiations
    - Set True to Enable, False to Disable

- pushover_token = "1234567890"
  - Your Pushover API token
- pushover_user = "abcdefghijklm" 
  - Your Pushover user key

When editing the config file and copying in your keys, make sure to leave the single and double quotes around tokens, otherwise the program will not know how to handle the token keys.

Once you are finished editing the config file, save it and close it and then you can test the scripts by using the following command:

```bash
python3 </full/path/to>/aslnotify/conn_bot.py 1 12345 54321
```

You should get a "connected" message from your bot on your system of choice.

### Configure Allstarlink
Once you have created your bot (if you are not using an existing one you own already), have the files in place and have updated your tokens in the config.py file, you will now need to configure Allstarlink to use these scripts to notify you.

SSH into your Allstar Node Server (if you are not already) and then you will need to edit the rpt.conf file in the /etc/asterisk folder.

```bash
sudo nano /etc/asterisk/rpt.conf
```

When the editor opens, you will need to find the lines in the node stanza that reference:

* connpgm = 
* discpgm = 

These will have a path after them for an example. This where you will put the following:

```bash
connpgm = python3 </full/path/to>/aslnotify/conn_bot.py 1
discpgm = python3 </full/path/to>/aslnotify/conn_bot.py 0
```

You will need to put these into all the public nodes stanzas that you host on that server. 

To test these scripts, you can connect to another ASL system and you should get a notification from your bot on your service of choice that the node has connected. If you disconnect, you should get a message that your node has disconnected.

These 2 functions automatically send two arguements to your scripts: 
* your node number 
* their Node number

The alert is formated as "Node THEIR_NODE connected to YOUR_NODE".

So if their node is 1999 and your node is 12345, you will get a notification similiar to the following example.

Example:
```bash
ALLSTAR ALERT: Node 1999 connected to 12345
```
---

## Contact
If you have questions, please feel free to reach out to me. You can reach me in one of the following ways:

- Twitter: @n8acl
- Mastodon: @n8acl@mastodon.radio
- E-mail: n8acl@qsl.net

If you reach out to me, please include what error you are getting and what you were doing. I may also ask you to send me certain files to look at. 
