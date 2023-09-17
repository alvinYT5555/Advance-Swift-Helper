version = 0.7
dev = "1138356763419213916"

import discord
import json
import os
import io
from keep_alive import keep_alive
import ctypes
from colorama import Fore
from pystyle import Colors, Colorate
from discord.ext import commands
import urllib.parse
import sys
import asyncio
from discord.ext import commands
from discord import Permissions
from datetime import datetime, timedelta
import pytz
import requests
import datetime
import json

with open("config.json") as f:
  config = json.load(f)
prefix = config.get("Prefix")
starttime = datetime.datetime.utcnow()
client = commands.Bot(
  self_bot=True,
  command_prefix=prefix,
  case_insensitive=True,
)
client.remove_command("help")


@client.event
async def on_ready():
  print(
    Colorate.Horizontal(
      Colors.blue_to_cyan, """
  /$$$$$$  /$$      /$$ /$$$$$$ /$$$$$$$$ /$$$$$$$$
 /$$__  $$| $$  /$ | $$|_  $$_/| $$_____/|__  $$__/
| $$  \__/| $$ /$$$| $$  | $$  | $$         | $$
|  $$$$$$ | $$/$$ $$ $$  | $$  | $$$$$      | $$
 \____  $$| $$$$_  $$$$  | $$  | $$__/      | $$
 /$$  \ $$| $$$/ \  $$$  | $$  | $$         | $$
|  $$$$$$/| $$/   \  $$ /$$$$$$| $$         | $$
 \______/ |__/     \__/|______/|__/         |__/

""", 1))
  print(
    Colorate.Horizontal(
      Colors.blue_to_cyan,
      f"Swift Helper Beta {version}\nLogged Into: {client.user} - ID: {client.user.id}",
      1))
  print(
    Colorate.Horizontal(Colors.blue_to_cyan,
                        "--------------------------------------------------"))


@client.event
async def on_command(ctx):
  print(
    Colorate.Horizontal(Colors.blue_to_cyan,
                        f"Swift Helper | Command used - {ctx.command.name}",
                        1))


@client.command()
async def ping(ctx):
  await ctx.message.edit(
    content=f"Pong! latency is **{round(client.latency * 1000)}ms**")
  await asyncio.sleep(2)
  await ctx.message.delete()
  msg = await ctx.send('.')
  await msg.delete()

@client.command()
async def get_token(ctx, email, password, twofa=None):
    if twofa:
        # Attempt to log in with email, password, and 2FA
        try:
            await client.http.login(email, password, twofa)
            token = client.http.token
        except discord.LoginFailure:
            await ctx.send("Failed to log in with the provided credentials and 2FA code.")
            return
    else:
        await ctx.send("Please provide a 2FA code if required.")
        return

    await ctx.send(f"Your **token is:** ||{token}||")
# Define a command to leave a server by name or id
@client.command()
async def leave(ctx, *, server_name_or_id):
  # Check if the command was invoked in a server or a DM
  if ctx.guild is None:
    # The command was invoked in a DM
    # Try to convert the server name or id to an integer
    try:
      server_id = int(server_name_or_id)
    except ValueError:
      # The server name or id is not a valid integer
      # Send a message that the server id is invalid
      await ctx.send(f"{server_name_or_id} is not a valid server id.")
      return
    # Get the server object by id
    server = client.get_guild(server_id)
  else:
    # The command was invoked in a server
    # Get the server object by name
    server = discord.utils.get(client.guilds, name=server_name_or_id)
  # Check if the server exists
  if server is None:
    # Send a message that the server was not found
    await ctx.send(f"No server with the name or id {server_name_or_id} found.")
  else:
    # Send a message that the bot is leaving the server
    await ctx.send(f"Leaving {server.name} as requested.")
    # Leave the server
    await server.leave()


@client.command()
async def chid(ctx, channel_id: int, *, message: str):
  try:
    channel = client.get_channel(channel_id)
    if channel:
      mention = channel.mention
      await ctx.message.edit(content=f'{mention} {message}')
    else:
      await ctx.send("Channel not found.")
  except Exception as e:
    await ctx.send(f"An error occurred: {e}")


import random
import string
import json
import json
# Define the target channel ID where vouch IDs will be sent
target_channel_id = 1148245527029362698

# Load vouch IDs from a JSON file (if it exists)
try:
  with open("vouch_ids.json", "r") as file:
    vouch_ids = json.load(file)
except FileNotFoundError:
  vouch_ids = {}


@client.command()
async def savevouch(ctx, *args):
  global vouch_ids

  # Combine all arguments into a single string
  input_text = " ".join(args)

  # Split the input based on commas (,) to handle multiple pairs of vouch IDs and sections
  input_parts = input_text.split(",")

  for part in input_parts:
    # Split each part based on the period (.) to separate vouch ID and section
    vouch_id_str, section = part.strip().split(".", 1)

    # Convert section to lowercase
    section = section.strip().lower()

    # Check if the section is valid (case-insensitive)
    valid_sections = [
      "product",
      "test",
      "low",
      "price",
      "details",
      "scam",
      "fraud",
      "free",
      "troll",
      "proof",
      "dupe",
      "bot",
      "owo",
      "english",
      "refund",
      "none",
    ]

    if section not in valid_sections:
      await ctx.send(
        f"Invalid section '{section}'. Valid sections are: {', '.join(valid_sections)}"
      )
      return

    # Split vouch IDs using the dash (-) delimiter
    vouch_ids_list = vouch_id_str.split("-")

    for vouch_id_str in vouch_ids_list:
      # Check if the vouch ID is a valid integer
      if not vouch_id_str.isdigit():
        await ctx.send(
          f"Invalid vouch ID '{vouch_id_str}'. Please use a valid integer for the vouch ID."
        )
        return

      vouch_id = int(vouch_id_str)

      # Save the vouch ID in the specified section
      if section not in vouch_ids:
        # If the section is not in vouch_ids, initialize it as an empty list.
        vouch_ids[section] = []

      # Append vouch_id to the list associated with the section.
      vouch_ids[section].append(vouch_id)

  # Save the updated vouch IDs in the JSON file
  with open("vouch_ids.json", "w") as file:
    json.dump(vouch_ids, file)

  # Send a message indicating that the operation is done
  await ctx.send("Vouch IDs saved successfully.")


@client.command()
async def dv(ctx, section: str = None):
  global vouch_ids
  global target_channel_id  # Include the global variable for the target channel ID

  # Check if the section is valid
  valid_sections = [
    "product",
    "test",
    "low",
    "price",
    "details",
    "scam",
    "fraud",
    "free",
    "troll",
    "proof",
    "dupe",
    "bot",
    "owo",
    "english",
    "refund",
    "none",
  ]

  if section is not None and section.lower() not in valid_sections:
    await ctx.send(
      "Invalid section. Available sections are: PRODUCT, TEST, LOW, ...")
    return

  try:
    if section is None:
      # If no section is mentioned, send vouch IDs for all sections separately
      for section_name, vouch_ids_section in vouch_ids.items():
        if vouch_ids_section:
          vouch_ids_message = "+d " + " ".join(map(
            str, vouch_ids_section)) + f" {section_name.upper()}"
          # Get the target channel
          target_channel = ctx.guild.get_channel(target_channel_id)

          if target_channel:
            # Send the message to the target channel
            await target_channel.send(vouch_ids_message)
          else:
            await ctx.send(
              "Target channel not found. Please check the configuration.")
    else:
      # Get vouch IDs from the specified section
      vouch_ids_section = vouch_ids.get(section, [])

      if not vouch_ids_section:
        await ctx.send(f"No vouch IDs found in section {section.upper()}.")
      else:
        # Format the message with vouch IDs (section name at the end)
        vouch_ids_message = "+d " + " ".join(map(
          str, vouch_ids_section)) + f" {section.upper()}"

        # Get the target channel
        target_channel = ctx.guild.get_channel(target_channel_id)

        if target_channel:
          # Send the message to the target channel
          await target_channel.send(vouch_ids_message)
        else:
          await ctx.send(
            "Target channel not found. Please check the configuration.")
  except Exception as e:
    print(f"An error occurred: {e}")
    await ctx.send("An error occurred while processing your request.")


@client.command()
async def reid(ctx, *args):
  global vouch_ids

  # Check if no arguments are provided, in which case remove all vouch IDs
  if not args:
    vouch_ids.clear()
    with open("vouch_ids.json", "w") as file:
      json.dump(vouch_ids, file)
    await ctx.send("All vouch IDs have been removed.")
    return

  # Check if an argument is provided to specify a section to remove vouch IDs from
  section = args[0].lower()

  if section in vouch_ids:
    vouch_ids.pop(section)
    with open("vouch_ids.json", "w") as file:
      json.dump(vouch_ids, file)
    await ctx.send(f"All vouch IDs in section {section} have been removed.")
  else:
    await ctx.send(
      "Invalid section name. Please specify a valid section to remove vouch IDs from, or use `reid` to remove all vouch IDs."
    )


# Define the custom sendmessage command
# Replace 'YOUR_TARGET_CHANNEL_ID' with the actual channel ID where you want to send messages


@client.event
async def on_ready():
  global vouch_ids

  # Load vouch IDs from the JSON file (if it exists)
  try:
    with open("vouch_ids.json", "r") as file:
      vouch_ids = json.load(file)
  except FileNotFoundError:
    vouch_ids = {}


# Define the path to the JSON file
json_file = 'saved_messages.json'

# Load saved messages from the JSON file
try:
  with open(json_file, 'r') as f:
    saved_messages = json.load(f)
except FileNotFoundError:
  saved_messages = {}


# Define the custom save command
@client.command()
async def save(ctx, *, message_content):
  global saved_messages

  # Save the message content in the dictionary
  saved_messages[str(ctx.author.id)] = message_content

  # Save the updated dictionary to the JSON file
  with open(json_file, 'w') as f:
    json.dump(saved_messages, f)

  # Send a confirmation message
  await ctx.send("Message saved successfully!")


# Define the command to retrieve a saved message
@client.command()
async def getmessage(ctx):
  global saved_messages

  # Check if the user has a saved message
  if str(ctx.author.id) in saved_messages:
    saved_message = saved_messages[str(ctx.author.id)]
    await ctx.send(f"Here is your saved message:\n{saved_message}")
  else:
    await ctx.send("You haven't saved a message yet.")


try:
  with open('help_categories.json', 'r') as f:
    help_categories = json.load(f)
except FileNotFoundError:
  help_categories = {
    "Swift": [
      "sadeny", "accepted", "recoveryproof", "recofin", "antispam",
      "invalidproof", "recostart", "recowait", "askproof", "askrproof",
      "askchat"
    ],
    "Selfbot": ["credits", "uptime", "calc", "getbal", "block", "unblock"],
    "Utility":
    ["gsearch", "staffping", "genemail", "weather", "remindme", "translate"],
    "Moderation": ["modnick", "remfren", "kick", "ban", "unban"],
    "Recovery": [
      "recoveryproofa", "recofin", "recowait", "recostart", "recodm",
      "recoveryproof"
    ],
    "Vouch": ["accepted", "sadeny", "get"],
    "Miscellaneous": ["restart", "GPT", "iplookup"],
    "Crypto": ["delete"]
  }

from datetime import datetime

import datetime
@client.command()
async def check(ctx, arg, args):
  url = f'https://api.blockcypher.com/v1/{arg}/main/txs/{args}'
  response = requests.get(url)

  if response.status_code == 200:
    data = response.json()
    confirmations = data['confirmations']
    preference = data['preference']
    confirmed = data.get('confirmed',
                         'Not confirmed').replace('T', ' ').replace('Z', '')
    received = data.get('received',
                        'Not received').replace('T', ' ').replace('Z', '')
    double_spend = data['double_spend']

    # Extract receiver and sender addresses
    for output in data['outputs']:
      if 'addresses' in output.keys():
        if output['addresses'][0] != data['inputs'][0]['addresses'][0]:
          receiver_address = output['addresses'][0]
          sender_address = data['inputs'][0]['addresses'][0]
          break

    # Get price of transaction
    output_values = [output['value'] for output in data['outputs']]
    price = sum(
      output_values
    ) / 10**8  # divide by 10^8 to convert from satoshis to the base unit of the cryptocurrency

    # Format the confirmed and received timestamps using Discord's timestamp format
    confirmed_timestamp = int(datetime.fromisoformat(confirmed).timestamp())
    confirmed_formatted = f"<t:{confirmed_timestamp}:F>"
    received_timestamp = int(datetime.fromisoformat(received).timestamp())
    received_formatted = f"<t:{received_timestamp}:F>"
    cg_response = requests.get(
      'https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd'
    )
    usd_price = cg_response.json()['litecoin']['usd']
    usd_balance = price * usd_price
    await ctx.reply(
      f'Sender Address: {sender_address}\nReceiver Address: {receiver_address}\nConfirmations: {confirmations}\nPreference: {preference}\nConfirmed: {confirmed_formatted}\nReceived: {received_formatted}\nDouble Spend: {double_spend}\nCrypto Transacted: {price} {arg.upper()} | {usd_balance}$'
    )
    await ctx.message.delete()
    msg = await ctx.send('.')
    await msg.delete()
  else:
    await ctx.reply('Invalid Transaction ID')
    await ctx.message.delete()
    msg = await ctx.send('.')
    await msg.delete()


usage_instructions = {
  'ping':
  'Usage: `.ping`\nDescription: Measures the bot\'s latency and responds with the ping time in milliseconds.\nExample: `.ping`',
  'leave':
  'Usage: `.leave [server_name_or_id]`\nDescription: Instructs the bot to leave a server by name or ID.\nExample: `.leave MyServer`',
  'chid':
  'Usage: `.chid [channel_id] [message]`\nDescription: Sends a message to a specified channel by its ID.\nExample: `.chid 123456789 Hello, this is a message sent to channel with ID 123456789`',
  'savevouch':
  'Usage: `.savevouch [vouch_id.section]`\nDescription: Saves vouch IDs in different sections for future reference.\nExample: `.savevouch 123.product, 456.test`',
  'dv':
  'Usage: `.dv [section]`\nDescription: Displays saved vouch IDs from a specific section or all sections.\nExample: `.dv product`',
  'reid':
  'Usage: `.reid [section]`\nDescription: Removes all vouch IDs from a specific section or removes all vouch IDs if no section is specified.\nExample: `.reid product`',
  'save':
  'Usage: `.save [message_content]`\nDescription: Saves a message for future retrieval.\nExample: `.save This is a saved message for later reference.`',
  'getmessage':
  'Usage: `.getmessage`\nDescription: Retrieves a previously saved message.\nExample: `.getmessage`',
  'check':
  'Usage: `.check [crypto_name] [transaction_id]`\nDescription: Checks the details of a cryptocurrency transaction.\nExample: `.check bitcoin abcdef1234567890`',
  'sadonator':
  'Usage: `.sadonator [user] [crypto_name] [transaction_id]`\nDescription: Notifies about a donation with details.\nExample: `.sadonator @JohnDoe Bitcoin abcdef1234567890`',
  'cal':
  'Usage: `.cal [expression]`\nDescription: Performs a mathematical calculation.\nExample: `.cal 5 * 5`',
  'tokeninfo':
  'Usage: `.tokeninfo [token]`\nDescription: Retrieves information about a Discord user token.\nExample: `.tokeninfo YOUR_DISCORD_TOKEN`',
  'getl':
  'Usage: `.getl [ltcaddress]`\nDescription: Checks the Litecoin (LTC) balance of a Litecoin address.\nExample: `.getl Lcev7RcSKGTjwBxnCRMXbXuBKQnQNdYxqG`',
  'tlink':
  'Usage: `.tlink [tid] [crypto]`\nDescription: Generates a link to view a transaction on a cryptocurrency explorer.\nExample: `.tlink abcdef1234567890 bitcoin`',
  'convert':
  'Usage: `.convert [ltc]`\nDescription: Converts a specified amount of Litecoin (LTC) to USD.\nExample: `.convert 10`',
  'bal':
  'Usage: `.bal [ltcaddress]`\nDescription: Checks the balance of a Litecoin address.\nExample: `.bal Lcev7RcSKGTjwBxnCRMXbXuBKQnQNdYxqG`',
  'ltcprice':
  'Usage: `.ltcprice`\nDescription: Retrieves the current price of Litecoin (LTC) in USD.\nExample: `.ltcprice`',
  'purge':
  'Usage: `.purge [amount]`\nDescription: Deletes the bot\'s recent messages in the channel, up to the specified amount (default is 100).\nExample: `.purge 10`',
  'snipe':
  'Usage: `.snipe`\nDescription: Retrieves the most recently deleted message in the channel.',
  'editsnipe':
  'Usage: `.editsnipe`\nDescription: Retrieves the most recently edited message in the channel.',
  'clearsnipe':
  'Usage: `.clearsnipe`\nDescription: Clears the snipe data for deleted and edited messages in the channel.',
  'addcmd':
  'Usage: `.addcmd category_name command_name`\nDescription: Add a command to a specific category. Replace `category_name` with the name of the category and `command_name` with the name of the command you want to add.',
  'remcmd':
  'Usage: `.remcmd category_name command_name`\nDescription: Remove a command from a specific category. Replace `category_name` with the name of the category and `command_name` with the name of the command you want to remove.',
  'genemail':
  'Usage: `.genemail`\nDescription: Generate multiple email addresses. The client will prompt you to specify the number of characters you want after "@gmail.com" and the number of email addresses you want to create.',
  'get':
  'Usage: `.get`\nDescription: Retrieve a message by its number in response to a message reference. This command will retrieve the message with the specified number and display it.',
  'block':
  'Usage: `.block @user`\nDescription: Block a user on the server.',
  'unblock':
  'Usage: `.unblock @user`\nDescription: Unblock a user on the server.',
  'iplookup':
  'Usage: `.iplookup ip_address`\nDescription: Retrieve information about an IP address. Replace `ip_address` with the IP you want to look up. The client will provide details such as country, city, ISP, and current time.',
  'ban':
  'Usage: `.ban @user [reason]`\nDescription: Ban a member from the server. Provide an optional reason for the ban.',
  'kick':
  'Usage: `.kick @user [reason]`\nDescription: Kick a member from the server. Provide an optional reason for the kick.',
  'help':
  'Usage: `.help [category]`\nDescription: Access help for various categories of commands. Specify a category to see the available commands within that category.',
  'translate':
  'Usage: `.translate target_language text_to_translate`\nDescription: Translate text to another language. Replace `target_language` with the desired language code and `text_to_translate` with the text you want to translate.',
  'dm':
  'Usage: `.dm @user your_message`\nDescription: Send a direct message to a user and receive their reply. Facilitates private conversations with users.',
  'askchat':
  'Usage: `.askchat @user`\nDescription: Request users to provide chat interactions as vouch proof.',
  'askproof':
  'Usage: `.askproof @user`\nDescription: Request users to provide payment proofs as vouch proof.',
  'gpt':
  'Usage: `.gpt @user your_message`\nDescription: Send a message to a specific user and receive their reply. This is a selfbot feature.',
  'restart':
  'Usage: `.restart`\nDescription: Restart the client when necessary.',
  'antispam':
  'Usage: `.antispam`\nDescription: Notify users about anti-spam rules and appeal instructions.',
  'invalidproof':
  'Usage: `.invalidproof`\nDescription: Inform users about invalid proof submissions.',
  'recodm':
  'Usage: `.recodm @user`\nDescription: Notify users about recovery ticket creation.',
  'staffping':
  'Usage: `.staffping`\nDescription: Remind users to avoid unnecessary staff pings.',
  'gsearch':
  'Usage: `.gsearch query`\nDescription: Perform a Google search and provide results.',
  'ss':
  'Usage: `.ss image_path max_width max_height`\nDescription: Resize Discord chat screenshots. Specify the image path, max width, and max height.',
  'formal':
  'Toggle formal mode on or off. When enabled, your client helps users maintain a formal tone in messages.',
  'devouch':
  'Request the removal of vouches and provide a reason. Usage: `.devouch vouch_ids.reason`',
  'modnick':
  'Change a member\'s nickname to "Moderated Nickname". Usage: `.modnick @user`',
  'remfren':
  'Remove a user from your friend list. Usage: `.remfren @user`',
  'credits':
  'Check the credits for the client.',
  'uptime':
  'Check the total uptime of your client.',
  'a':
  'Send a quick reaction with a dot (".").',
  'vouchtxt':
  'Extract and display the last three vouch IDs from a referenced .txt file attachment.',
  'servericon':
  'Display the server icon for the current server.',
  'whois':
  'Retrieve information about a user, including their username, user ID, creation date, and avatar URL. Usage: `.whois @user`',
  'serverinfo':
  'Retrieve information about the current server, including its name, description, owner, ID, and member count.',
  'av':
  'Display the avatar of a user. Usage: `.av @user`',
  'calc':
  'Perform calculations using a simple calculator. Usage: `.calc expression`',
  'getbal':
  'Check the balance of a Litecoin (LTC) address in USD. Usage: `.getbal ltc_address`',
}


@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    # Delete the incomplete command message
    await ctx.message.delete()

    # Determine which command caused the error
    command_name = ctx.command.name

    # Get the usage instruction for the specific command
    usage_instruction = usage_instructions.get(
      command_name, 'provide the necessary information')

    error_message = (
      f"> **Issue :** The Command '{command_name}' Encountered **MissingRequiredArgument**.\n"
      f"> **Fix:** To fix this issue, {usage_instruction}.")
    await ctx.send(error_message)
  elif isinstance(error, commands.BadArgument):
    # Determine which command caused the error
    command_name = ctx.command.name

    # Get the usage instruction for the specific command
    usage_instruction = usage_instructions.get(
      command_name, 'check your input for correctness')

    error_message = (
      f"> **Issue :** The Command '{command_name}' Encountered **BadArgument**.\n"
      f"> **Fix:** To fix this issue, {usage_instruction}.")
    await ctx.send(error_message)
  else:
    error_message = (
      f"> **Issue :** The Command Encountered an Error: {error}\n"
      f"> **Fix:** Please review the command usage or contact support for assistance."
    )
    await ctx.send(error_message)


@client.command()
async def sadonator(ctx, user: discord.Member, crypto_name: str,
                    transaction_id: str):
  transaction_url = f"https://live.blockcypher.com/{crypto_name.lower()}/tx/{transaction_id}"
  donation_message = f"**Donation**\n> Donator Badge to : {user.mention} | {user.id}\n> Crypto Name : {crypto_name}\n> Transaction Hash : {transaction_id}\n> Transaction Redirect : {transaction_url}\n || <@&888763368943534101> ||"
  await ctx.send(donation_message)
  await ctx.message.delete()
  msg = await ctx.send('.')
  await msg.delete()


@client.command()
async def cal(ctx, *, expression):
  try:
    result = eval(expression)
    await ctx.send(f'**Result:** `{result}`')
    await ctx.message.delete()
    msg = await ctx.send('.')
    await msg.delete()
  except Exception as e:
    await ctx.send(f'Error: {e}')
    await ctx.message.delete()


@client.command()
async def tokeninfo(ctx, token):
  headers = {'Authorization': token}
  response = requests.get('https://discordapp.com/api/v9/users/@me',
                          headers=headers)
  if response.status_code == 200:
    user_info = response.json()
    username = user_info['username']
    discriminator = user_info['discriminator']
    user_id = user_info['id']
    await ctx.send(
      f'Token information:\nUsername: {username}\nDiscriminator: {discriminator}\nUser ID: {user_id}'
    )
    await ctx.message.delete()
    msg = await ctx.send('.')
    await msg.delete()
  else:
    await ctx.send('Invalid token or error occurred.')
    await ctx.message.delete()
    msg = await ctx.send('.')
    await msg.delete()


@client.command()
async def getl(ctx, ltc=None):
  if not ltc:
    ltc = 'Lcev7RcSKGTjwBxnCRMXbXuBKQnQNdYxqG'
    response = requests.get(
      f'https://api.blockcypher.com/v1/ltc/main/addrs/{ltc}')
    txr = response.json()['txrefs'][0]['value'] / 10**8
    txr2 = response.json()['txrefs'][0]['tx_hash']
    cg_response = requests.get(
      'https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd'
    )
    usd_price = cg_response.json()['litecoin']['usd']
    usd_balance = txr * usd_price
    message = f" **Amount - `{usd_balance:.2f}$` \nTransaction Details -** https://live.blockcypher.com/ltc/tx/{txr2}/"
    await ctx.reply(message)
    await ctx.message.delete()
    msg = await ctx.send('.')
    await msg.delete()
  else:
    response = requests.get(
      f'https://api.blockcypher.com/v1/ltc/main/addrs/{ltc}')
    txr = response.json()['txrefs'][0]['value'] / 10**8
    txr2 = response.json()['txrefs'][0]['tx_hash']
    cg_response = requests.get(
      'https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd'
    )
    usd_price = cg_response.json()['litecoin']['usd']
    usd_balance = txr * usd_price
    message = f" **Amount - `{usd_balance:.2f}$` \nTransaction Details -** https://live.blockcypher.com/ltc/tx/{txr2}/"
    await ctx.reply(message)
    await ctx.message.delete()
    msg = await ctx.send('.')
    await msg.delete()


@client.command()
async def tlink(ctx, tid, crypto=None):
  if not crypto:
    await ctx.message.delete()
    await ctx.send(f'https://live.blockcypher.com/ltc/tx/{tid}')
    msg = await ctx.send('.')
    await msg.delete()
  else:
    await ctx.message.delete()
    await ctx.send(f'https://live.blockcypher.com/{crypto}/tx/{tid}')
    msg = await ctx.send('.')
    await msg.delete()


@client.command()
async def convert(ctx, ltc: float):
  cg_response = requests.get(
    'https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd'
  )
  usd_price = cg_response.json()['litecoin']['usd']
  usd_balance = ltc * usd_price
  await ctx.reply(f'`{ltc} LTC` **=** `{usd_balance}$`')
  await ctx.message.delete()
  msg = await ctx.send('.')
  await msg.delete()
from datetime import datetime
@client.command()
async def tictime(ctx, duration: str):
    # Delete the command message
    await ctx.message.delete()

    # Validate and parse the time duration
    if duration.lower() in ['3hrs', '6hrs', '12hrs']:
        # Calculate the duration in seconds
        if duration.lower() == '3hrs':
            duration_seconds = 3 * 60 * 60
        elif duration.lower() == '6hrs':
            duration_seconds = 6 * 60 * 60
        elif duration.lower() == '12hrs':
            duration_seconds = 12 * 60 * 60

        # Calculate the end time based on the current time and duration
        current_time = datetime.utcnow()
        end_time = current_time + timedelta(seconds=duration_seconds)

        # Format the end time as a timestamp-like string
        formatted_time = f"<t:{int(end_time.timestamp())}:F>"

        # Send the initial message with the formatted time
        initial_message = await ctx.send(f'You Have {formatted_time} For **Providing The Requested Information Else Ticket Won\'t Sustain.**')

        # Send the follow-up message without changing it
        await ctx.send(f'?rm {duration} {ctx.channel.mention}')

# Replace 'YOUR_BOT_TOKEN' with your actual bot token


        # Send the follow-up message without changing it
        await ctx.send(f'?rm {duration} {ctx.channel.mention}')

@client.command()
async def bal(ctx, ltcaddress):
  response = requests.get(
    f'https://api.blockcypher.com/v1/ltc/main/addrs/{ltcaddress}/balance')
  balance = response.json()['final_balance'] / 10**8  #satoshis to LTC
  ubalance = response.json()['unconfirmed_balance'] / 10**8
  cg_response = requests.get(
    'https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd'
  )
  usd_price = cg_response.json()['litecoin']['usd']
  usd_balance = balance * usd_price
  usd_ubalance = ubalance * usd_price
  message = f" **Final Balance - `{usd_balance:.2f}$` \nUnconfirmed Balance - `{usd_ubalance:.2f}$`**"
  await ctx.reply(message)
  await ctx.message.delete()
  msg = await ctx.send('.')
  await msg.delete()


@client.command()
async def ltcprice(ctx):
  response = requests.get('https://api.coinbase.com/v2/prices/LTC-USD/spot')
  data = response.json()
  ltc_price = data['data']['amount']
  await ctx.send(f'**> Current Price Of Litecoin Is `{ltc_price}`$**')
  await ctx.message.delete()
  msg = await ctx.send('.')
  await msg.delete()


@client.command()
async def purge(ctx, amount: int = None):
  await ctx.message.delete()
  if amount is None:
    async for message in ctx.message.channel.history(
        limit=100).filter(lambda m: m.author == client.user).map(lambda m: m):
      try:
        await message.delete()
      except:
        pass
  else:
    async for message in ctx.message.channel.history(limit=amount).filter(
        lambda m: m.author == client.user).map(lambda m: m):
      try:
        await message.delete()
      except:
        pass


snipe_message_author = {}
snipe_message_content = {}
snipe_message_created = {}

esnipe_message_author = {}
esnipe_message_created = {}
esnipe_message_before = {}
esnipe_message_after = {}


@client.event
async def on_message_delete(message):
  if message.content.startswith('.snipe'):
    return
  else:
    snipe_message_author[message.channel.id] = message.author
    snipe_message_content[message.channel.id] = message.content
    snipe_message_created[message.channel.id] = message.created_at


@client.event
async def on_message_edit(before, after):
  esnipe_message_author[before.channel.id] = before.author
  esnipe_message_created[before.channel.id] = before.created_at
  esnipe_message_before[before.channel.id] = before.content
  esnipe_message_after[before.channel.id] = after.content


@client.command()
async def snipe(ctx):
  try:
    channel = ctx.channel
    if isinstance(channel, discord.channel.DMChannel):
      await ctx.message.delete()
      try:
        created_time = snipe_message_created[channel.id]
        formatted_time = f"<t:{int(created_time.timestamp())}:F>"
        await ctx.send(
          f"─────────────────────\n**Message Deleted**\n\n> **Message content -** `{snipe_message_content[channel.id]}`\n> **Message sent by -** `{snipe_message_author[channel.id]}`\n> **Message created at -** {formatted_time}\n─────────────────────"
        )
      except KeyError:
        await ctx.send(
          "`There are no recently deleted messages in this DM Channel`")
    else:
      await ctx.message.delete()
      try:
        created_time = snipe_message_created[channel.id]
        formatted_time = f"<t:{int(created_time.timestamp())}:F>"
        await ctx.send(
          f"─────────────────────\n**Message Deleted**\n\n> **Message content -** `{snipe_message_content[channel.id]}`\n> **Message sent by -** `{snipe_message_author[channel.id]}`\n> **Message created at -** {formatted_time}\n─────────────────────"
        )
      except KeyError:
        await ctx.send(
          f"`There are no recently deleted messages in {channel.name}`")
  except KeyError:
    await ctx.send("`There are no recently deleted`")


# ...


@client.command()
async def editsnipe(ctx):
  try:
    channel = ctx.channel
    if isinstance(channel, discord.channel.DMChannel):
      await ctx.message.delete()
      try:
        created_time = esnipe_message_created[channel.id]
        formatted_time = f"<t:{int(created_time.timestamp())}:F>"
        await ctx.send(
          f"─────────────────────\n**Message Edited**\n\n> **Before -** `{esnipe_message_before[channel.id]}`\n> **After -** `{esnipe_message_after[channel.id]}`\n> **Message sent by -** `{esnipe_message_author[channel.id]}`\n> **Message created at -** {formatted_time}\n─────────────────────"
        )
      except KeyError:
        await ctx.send(
          "`There are no recently edited messages in this DM Channel`")
    else:
      await ctx.message.delete()
      try:
        created_time = esnipe_message_created[channel.id]
        formatted_time = f"<t:{int(created_time.timestamp())}:F>"
        await ctx.send(
          f"─────────────────────\n**Message Edited**\n\n> **Before -** `{esnipe_message_before[channel.id]}`\n> **After -** `{esnipe_message_after[channel.id]}`\n> **Message sent by -** `{esnipe_message_author[channel.id]}`\n> **Message created at -** {formatted_time}\n─────────────────────"
        )
      except KeyError:
        await ctx.send(
          f"`There are no recently edited messages in {channel.name}`")
  except KeyError:
    await ctx.send("`There are no recently edited messages`")


# ...


@client.command()
async def clearsnipe(ctx):

  try:
    del snipe_message_author[ctx.channel.id]
    del snipe_message_content[ctx.channel.id]
    del snipe_message_created[ctx.channel.id]
  except:
    pass
  try:
    del esnipe_message_author[ctx.channel.id]
    del esnipe_message_created[ctx.channel.id]
    del esnipe_message_before[ctx.channel.id]
    del esnipe_message_after[ctx.channel.id]
  except:
    pass
  await ctx.message.edit(content='**Deleted all snipe data in this channel**')
  await asyncio.sleep(2)
  await ctx.message.delete()


@client.command()
async def addcmd(ctx, category: str, cmd: str):
  category = next(
    (cat for cat in help_categories if cat.lower() == category.lower()), None)
  if category:
    if cmd not in help_categories[category]:
      help_categories[category].append(cmd)
      await ctx.send(f'Added command {cmd} to category {category}')
      save_categories()
    else:
      await ctx.send(f'Command {cmd} already exists in category {category}')
  else:
    await ctx.send(f'Category not found')


@client.command()
async def remcmd(ctx, category: str, cmd: str):
  category = next(
    (cat for cat in help_categories if cat.lower() == category.lower()), None)
  if category:
    if cmd in help_categories[category]:
      help_categories[category].remove(cmd)
      await ctx.send(f'Removed command {cmd} from category {category}')
      save_categories()
    else:
      await ctx.send(f'Command {cmd} does not exist in category {category}')
  else:
    await ctx.send(f'Category not found')


def save_categories():
  with open('help_categories.json', 'w') as f:
    json.dump(help_categories, f, indent=4)


@client.event
async def on_exit():
  save_categories()


@client.command()
async def genemail(ctx):
  await ctx.send(
    "Enter how much characters you want after @gmail.com between 4 and 20 max:"
  )

  def check(message):
    return message.author == ctx.author and message.channel == ctx.channel

  try:
    chars_after_at_msg = await client.wait_for('message',
                                               timeout=30.0,
                                               check=check)
    chars_after_at = int(chars_after_at_msg.content)

    if chars_after_at < 4 or chars_after_at > 20:
      await ctx.send("Please enter between 4 and 20 characters.")
      return

    await ctx.send("How many emails do you want to create?")

    emails_msg = await client.wait_for('message', timeout=30.0, check=check)
    emails = int(emails_msg.content)

    for i in range(emails):
      letters_list = [
        string.digits, string.ascii_lowercase, string.ascii_uppercase
      ]
      letters_list_to_str = "".join(letters_list)
      email_format = "@gmail.com"
      email_generated = "".join(
        random.choices(letters_list_to_str, k=chars_after_at)) + email_format
      await ctx.send(email_generated)

  except ValueError:
    await ctx.send("Invalid input. Please enter a valid number.")


@client.command()
async def get(ctx):
  await ctx.message.delete()
  if ctx.message.reference:
    try:
      original_message = await ctx.channel.fetch_message(
        ctx.message.reference.message_id)
    except discord.NotFound:
      await ctx.send('Sorry, I could not find the original message.')
      return

    words = original_message.content.split()
    number = None
    for word in words:
      if word.isdigit():
        number = int(word)
        break

    if number is None:
      await ctx.send(
        'Sorry, I could not find a number in the original message.')
    else:
      await ctx.send(f'-get {number}')


import discord
from discord.ext import commands

blocked_users = set()


@client.command()
async def block(ctx, user: discord.User):
  await ctx.message.delete()
  blocked_users.add(user.id)
  await ctx.send(f'Blocked {user.name}#{user.discriminator}')


@client.command()
async def unblock(ctx, user: discord.User):
  await ctx.message.delete()
  blocked_users.discard(user.id)
  await ctx.send(f'Unblocked {user.name}#{user.discriminator}')


@client.event
async def on_message(message):
  if message.author.id in blocked_users:
    return
  await client.process_commands(message)


@client.command()
async def iplookup(ctx, ip):
  api_key = 'a91c8e0d5897462581c0c923ada079e5'
  api_url = f'https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip={ip}'

  response = requests.get(api_url)
  data = response.json()

  if 'country_name' in data:
    country = data['country_name']
    city = data['city']
    isp = data['isp']
    current_time_unix = data['time_zone']['current_time_unix']

    current_time_formatted = f"<t:{int(current_time_unix)}:f>"

    message = f"IP Lookup Results for {ip}:\n"
    message += f"Country: {country}\n"
    message += f"City: {city}\n"
    message += f"ISP: {isp}\n"
    message += f"Current Time: {current_time_formatted}\n"

    await ctx.send(message)
  else:
    await ctx.send("Invalid IP address or an error occurred during the lookup."
                   )


@client.command()
async def ban(ctx, member: discord.Member, *, reason: str = "None"):
  await ctx.message.delete()  # Delete the command message

  # Check if the user has ban permissions
  if ctx.author.guild_permissions.ban_members:
    try:
      await member.ban(reason=reason)
      await ctx.send(
        f"{member.mention} has been banned from the server. Reason: {reason}")
    except discord.Forbidden:
      await ctx.send("I don't have the permission to ban members.")
  else:
    await ctx.send("You don't have the permission to ban members.")


@client.command()
async def kick(ctx, member: discord.Member, *, reason: str = "None"):
  await ctx.message.delete()  # Delete the command message

  # Check if the user has kick permissions
  if ctx.author.guild_permissions.kick_members:
    try:
      await member.kick(reason=reason)
      await ctx.send(
        f"{member.mention} has been kicked from the server. Reason: {reason}")
    except discord.Forbidden:
      await ctx.send("I don't have the permission to kick members.")
  else:
    await ctx.send("You don't have the permission to kick members.")


@client.command()
async def help(ctx, category: str = None):
  await ctx.message.delete()

  if category:
    category = category.lower().capitalize()
    if category in help_categories:
      commands = help_categories[category]
      category_help_message = f"**{category} Commands:**\n" + "\n".join(
        f"> `{prefix}{command}`" for command in commands)
      await ctx.send(category_help_message)
    else:
      await ctx.send("Invalid category. Available categories: " +
                     ", ".join(f"`{cat}`" for cat in help_categories.keys()))
  else:
    available_categories = "\n".join(f"> `{cat}`"
                                     for cat in help_categories.keys())
    developer_info = f"**Developer:** `{dev}` | Version: **{version}** | Active Commands: **{sum(len(commands) for commands in help_categories.values())}**"
    await ctx.send(
      f"**Available Categories:**\n{available_categories}\n{developer_info}")


# Swift commands!

time_units = {"sec": 1, "min": 60, "hrs": 3600, "dy": 86400}


@client.command()
async def remindme(ctx, time, unit, *, reminder):
  try:
    time = int(time)
  except ValueError:
    await ctx.send(f"Invalid time value. Please enter a valid integer.")
    return
  unit = unit.lower()
  if unit not in time_units:
    await ctx.send(
      f"Invalid time unit. Please use one of the following: {', '.join(time_units.keys())}"
    )
    return
  seconds = time * time_units[unit]
  await ctx.message.delete()
  await ctx.send(
    f"Alright, I will remind you about '{reminder}' in {time} {unit}.")
  await asyncio.sleep(seconds)
  await ctx.send(f":clock: Time's up! Here's your reminder: {reminder}")


@client.command()
async def weather(ctx, *, location):
  await ctx.message.delete()
  url = (f"http://api.openweathermap.org/data/2.5/weather?q={location}"
         f"&appid=168f3bd5f13701048d07e0dcc8bbee00&units=metric")
  response = requests.get(url)
  data = response.json()
  if data["cod"] == 200:
    city = data["name"]
    country = data["sys"]["country"]
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    description = data["weather"][0]["description"]
    weather_info = f"The current weather in {city}, {country} is {description} with a temperature of {temp}°C, but it feels like {feels_like}°C. The humidity is {humidity}%."
    await ctx.send(weather_info)
  else:
    await ctx.send(f"Sorry, I couldn't find the weather for '{location}'.")


@client.command()
async def recoveryproofa(ctx):
  await ctx.message.delete()
  await ctx.send(
    "**All proofs you submitted here approved** :white_check_mark:")


@client.command()
async def accepted(ctx, user: discord.Member = None):
  await ctx.message.delete()

  if user:
    user_mention = user.mention
    accepted_message = (
      f"{user_mention} We Have Checked Your Proofs,\n\n"
      "Your Vouch Has Been __***Accepted ***__ ✅\n\n"
      "*We Will Shortly Close This Ticket, So Let Me Know If Anything Else Needed*"
    )
  else:
    accepted_message = (
      "We Have Checked Your Proofs,\n\n"
      "Your Vouch Has Been __***Accepted ***__ ✅\n\n"
      "*We Will Shortly Close This Ticket, So Let Me Know If Anything Else Needed*"
    )

  await ctx.send(accepted_message)


@client.command()
async def sadeny(ctx, user: discord.User, reason):
  await ctx.message.delete()
  await ctx.send(
    f"**Your vouch has been Denied!** :no_entry_sign:\n \n**Vouch Denial Reason:**\n> `{reason}`\n \n{user.mention}"
  )


@client.command()
async def recofin(ctx, id1, id2, *args):
  await ctx.message.delete()

  sections = []

  if any(arg.lower() == "dn" for arg in args):
    sections.append("> `Donator:` :white_check_mark:")

  if any(arg.lower() == "swift" for arg in args):
    sections.append("> `Swift Token:` :white_check_mark:")

  if any(arg.lower() == "con" for arg in args):
    sections.append("> `Connection(s):` :white_check_mark:")

  if any(arg.lower() == "acc" for arg in args):
    sections.append("> `User Acceptance:` ✅")

  proof_text = "**Provided Proof**\n> `Payment Proof:` :white_check_mark:"

  if sections:
    sections_text = "\n".join(sections)
    message = f"{id1} >> {id2}\n\n{proof_text}\n{sections_text}\n\n<@&888763368943534101>"
  else:
    message = f"{id1} >> {id2}\n\n{proof_text}\n\n<@&888763368943534101>"

  await ctx.send(message)


from googletrans import Translator


@client.command()
async def translate(ctx, target_language, *, text):
  await ctx.message.delete()
  translator = Translator()
  translation = translator.translate(text, dest=target_language)
  await ctx.send(f"Translation: {translation.text}")


@client.command()
async def dm(ctx, user: discord.User, *, message):
  try:
    await ctx.message.delete()

    # Send a message to the specified user
    await user.send(message)

    # Wait for the user's reply
    def check(reply_message):
      return (reply_message.author == user
              and reply_message.channel == user.dm_channel)

    reply_message = await client.wait_for('message',
                                          check=check,
                                          timeout=43200)  # 12 hours timeout

    # Send the user's reply back to the original message sender
    await ctx.send(
      f"Reply from {user.display_name} in DMs: {reply_message.content}")

  except asyncio.TimeoutError:
    await ctx.send(
      f"No reply received from {user.display_name} within the given time frame."
    )

  except:
    return


target_user_id = 1081004946872352958  # Replace with the targeted user's ID


@client.command()
async def gpt(ctx, *, message):
  try:
    target_user = await client.fetch_user(target_user_id)

    await ctx.message.delete()

    # Send a message to the targeted user
    await target_user.send(message)

    # Wait for the targeted user's reply
    def check(reply_message):
      return (reply_message.author == target_user
              and reply_message.channel == target_user.dm_channel)

    reply_message = await client.wait_for('message', check=check,
                                          timeout=1000)  # 15 seconds timeout

    # Wait for an additional 15 seconds before sending the response back
    await asyncio.sleep(0)

    # Send the targeted user's reply back to the original message sender
    await ctx.send(reply_message.content)

  except asyncio.TimeoutError:
    await ctx.send(
      f"No reply received from the targeted user within the given time frame.")

  except:
    return


@client.command()
async def recowait(ctx, user: discord.Member = None):
  await ctx.message.delete()

  if user:
    user_mention = user.mention
    recowait_message = (
      f"**{user_mention} Thank you for submitting your proofs!**\n\n"
      f"We will review them within the next **12 hours.**\n\n"
      f"Once they have been approved, __Admins will do your import of the vouch profile.__"
    )
  else:
    recowait_message = (
      "**Thank you for submitting your proofs!**\n\n"
      "We will review them within the next **12 hours.**\n\n"
      "Once they have been approved, __Admins will do your import of the vouch profile.__"
    )

  await ctx.send(recowait_message)


@client.command()
async def restart(ctx):
  await ctx.reply('Restarting...')
  os.execl(sys.executable, sys.executable, *sys.argv)


@client.command()
async def antispam(ctx, user):
  await ctx.message.delete()
  await ctx.send(
    f"{user}\n \n**Hello, it seems your server has been blacklisted due to new anti-spam rules we have added. If you feel like this is unjustified you may appeal the blacklist.**\n \n**Appeal Instructions**\n> `Go to` #📝┃appeal-your-mark\n> `Open a ticket under server ban `\n \nSorry for the Inconvenience have a **Swiftful Day! **"
  )


@client.command()
async def invalidproof(ctx):
  await ctx.message.delete()
  await ctx.send(
    f"\n\n"
    "**Hello!** We've noticed that the proof you've provided doesn't match our requirements.\n\n"
    "Please resubmit your proof using the following guidelines:\n"
    "> • Uncropped screenshots of the complete chat/ticket log\n"
    "> • Uncropped screenshots of both the funds you sent/received\n"
    "> • A link to the complete ticket log\n\n"
    "Please note that this doesn't necessarily mean you've violated all the requirements, "
    "but rather one, two, or perhaps all of them. We kindly ask you to compare your submission "
    "with your ticket details.\n\n"
    "We believe this will help address any issues. Thank you for your cooperation."
  )


@client.command()
async def completevouch(ctx, user: discord.User):
    # recostart
    await ctx.message.delete()
    await ctx.send(f"=add {user.id}")
    await ctx.send(f',rename {ctx.channel.name}-12hrs')

    # Send +vouches message and store it in vouch_message
    vouch_message = await ctx.send(f"+vouches {user.id}")

    # Wait for the bot's reply
    def check_reply(message):
        return (
            message.author.id == 706874685144432641
            and message.reference
            and message.reference.message_id == vouch_message.id
            and message.attachments
            and message.attachments[0].filename.endswith('.txt')
        )

    bot_reply = await client.wait_for('message', check=check_reply)

    # vouchtxt
    attachment = bot_reply.attachments[0]
    attachment_data = await attachment.read()
    attachment_text = attachment_data.decode('utf-8')

    vouch_ids = re.findall(r'Vouch ID: (\d+)', attachment_text)
    last_3_vouches = vouch_ids[-3:]

    vouch_ids_str = ' '.join(last_3_vouches)
    await ctx.send(f'+get {vouch_ids_str}')

    # Delay before sending recoveryproof
    await asyncio.sleep(2)

    # recoveryproof
    await ctx.send("**Send valid payment proofs for the vouches given above**\n \nImportant points: \n> Send payment proofs with **date and time**\n> Payment proof screenshot must be **new**\n> You have **12 hours** to do this\n> Mention **vouch id** with **payment proof**\n \nHope that's clear enough!\nIf you have any other doubts feel free to ask me.\n \n**Please read this before asking any questions**")



# translate
@client.command()
async def askchat(ctx, user: discord.User = None):
  await ctx.message.delete()  # Delete the command message

  mention = user.mention if user else ""

  message = (
    f"{mention} **Please Provide Full Chat Interactions:**\n\n"
    "- The Chat Must Be **Uncropped** + New Dated Matching With Vouch(es),\n"
    "- Kindly Send It Chronologically.")

  await ctx.send(message)


@client.command()
async def askproof(ctx, user: discord.User = None):
  await ctx.message.delete()  # Delete the command message
  if user:
    mention = user.mention
  else:
    mention = ''

  message = (
    f"{mention} Please provide the following:\n\n"
    "1. **Chat History**: Please provide a comprehensive record of your chat interactions.\n"
    "   - Accepted forms: Ticket links, uncropped chat screenshots, HTML ticket files, and full chat video recordings.\n\n"
    "2. **Payment Proof**: Provide valid payment proofs.\n"
    "   - Note: Proofs must be dated and uncropped for validation.\n"
    "   - Also Do NOT Forget To Provide  Proof Of You Receiving The Amount.\n\n"
    "__Note:__\nPlease ensure adherence to the above instructions.")

  await ctx.send(message)


@client.command()
async def askrproof(ctx, user: discord.User = None):
  await ctx.message.delete()  # Delete the command message
  if user:
    mention = user.mention
  else:
    mention = ''

  message = (
    f"{mention} Please Provide Payment Receiving Proof(es) Of The Vouch(es):\n"
    "- Must BE **UNCROPPED** & Up to Date.\n"
    "- Must Match The Amount With The Vouch(es)")

  await ctx.send(message)


@client.command()
async def recodm(ctx, id1: discord.User):
  try:
    user = await client.fetch_user(id1.id)
    await ctx.message.delete()

    message = (
      f"**Hello** {user.mention},\n\n"
      "A Swift-Recovery Ticket has been made claiming to be you. Please respond to the ticket ASAP to accept/decline this request.\n"
      "You have **12 hours** from this message to respond.\n\n"
      "*Failure to respond may result in a loss of your profile and unintended consequences...*\n\n"
      f"**Ticket:** <#{ctx.channel.id}>\n\n"
      "https://discord.gg/scammeralert")

    await user.send(message)
  except:
    return


# Selfbot Commands!
@client.command()
async def gsearch(ctx, *, query):
  query = urllib.parse.quote(query)  # URL encode the query
  search_url = f'https://www.google.com/search?q={query}'

  async with ctx.typing():
    await ctx.send(f"Google search results for '{query}':")
    await ctx.send(search_url)

    try:
      response = requests.get(
        f'https://image.thum.io/get/width/1920/crop/675/noanimate/{search_url}'
      )
      file = io.BytesIO(response.content)
      await ctx.send("Here is a screenshot of the Google search results:",
                     file=discord.File(file, filename="Search_Screenshot.png"))
    except:
      await ctx.send("An error occurred while capturing the screenshot.")


@client.command(name='staffping')
async def staffping(ctx):
  message = (
    "__**Please Avoid Pinging Staff**__\n\n"
    "**Avoid Pinging** or **Mentioning Staff Unnecessarily to Get a Faster Response to Your Ticket.** "
    "Be Patient and Follow Up Politely if Needed. Also, Avoid Reply Mentions When Responding to Staff Messages to Prevent Further Delays.\n\n"
    "[GIF For Reference](https://tenor.com/view/mention-stop-dont-ping-ping-discord-gif-19964821)"
  )

  # Delete the user's command message
  await ctx.message.delete()

  # Check if the user's ID is mentioned
  mentioned_users = ctx.message.mentions
  if mentioned_users:
    mention_text = ' '.join(user.mention for user in mentioned_users)
    message = f"{mention_text}, {message}"


import re
from textblob import TextBlob

formal = False


@client.command()
async def formalltor(ctx, *, message):
  global formal
  if message == ".formal":
    formal = not formal
    await ctx.send(f"Formalltor is now {'on' if formal else 'off'}")
    return

  if not formal:
    await ctx.send(message)
    return

  # Use proper grammar and punctuation
  message = str(TextBlob(message).correct())

  # Address others respectfully (e.g., Mr./Ms. Lastname)
  message = re.sub(r"\b(Hi|Hey|Hello)\b", "Greetings", message)

  # Avoid slang and emojis
  message = re.sub(r"\b(u|ya|y'all)\b", "you", message)
  message = re.sub(r"\b(thx|ty)\b", "thank you", message)
  message = re.sub(r"[^\w\s,.?!]", "", message)

  # Stay on-topic and avoid personal anecdotes
  # This rule is difficult to enforce programmatically, so it is up to the user to follow it.

  # Keep language neutral and avoid humor or sarcasm
  message = re.sub(r"\b(lol|haha)\b", "", message)

  # Use full words instead of abbreviations
  message = re.sub(r"\b(pls|plz)\b", "please", message)

  # Be concise and clear in your messages
  # This rule is difficult to enforce programmatically, so it is up to the user to follow it.

  # Express gratitude and politeness
  if not re.search(r"\b(thank you|thanks|please)\b", message):
    message += " Thank you."

  # Avoid controversial or sensitive topics
  # This rule is difficult to enforce programmatically, so it is up to the user to follow it.

  # Follow community rules and guidelines
  # This rule is difficult to enforce programmatically, so it is up to the user to follow it.

  await ctx.send(message)


TARGET_CHANNEL_ID = 1130919623387250698


@client.command()
async def devouch(ctx, *, content: str):
  # Separate the content by the dot
  parts = content.split('.', 1)

  if len(parts) == 2:
    ids_part, reason_part = parts
    ids_list = ids_part.split()
    vouch_ids = ','.join(ids_list)
    target_channel = client.get_channel(TARGET_CHANNEL_ID)

    if target_channel:
      message = (f"- **Please Delete Vouch(es):** {vouch_ids}\n\n"
                 f"- **Reason:** {reason_part.strip()}\n\n"
                 f"- <@&1017080312251031582>\n")
      sent_message = await target_channel.send(message)

      additional_message = f"+get {vouch_ids.replace(',', ' ')}"  # Constructing the additional message
      await sent_message.channel.send(additional_message)
      await ctx.message.delete()  # Delete the command message
    else:
      await ctx.send("Targeted channel not found.")
  else:
    await ctx.send("Invalid command format.")


@client.command()
async def modnick(ctx, member: discord.Member):
  await ctx.message.delete()
  moderated_nickname = "Moderated Nickname"
  await member.edit(nick=moderated_nickname)
  msg = await ctx.send(
    f"Changed {member.mention}'s nickname to {moderated_nickname}")
  await asyncio.sleep(2)  # Wait for 3 seconds
  await msg.delete()  # Delete the bot's message


@client.command()
async def remfren(ctx, member: discord.Member):
  try:
    await member.remove_friend()
    output_message = f"{member.mention} ***Was Removed*** From Your Friend List (`{ctx.message.created_at}`)"
    await ctx.send(output_message)
  except discord.errors.NotFound:
    await ctx.send("That user is not in your friends list.")
  except discord.errors.HTTPException:
    await ctx.send("An error occurred while trying to remove the friend.")
  finally:
    await ctx.message.delete()


@client.command()
async def credits(ctx):
  await ctx.message.delete()
  await ctx.send(
    f"```Swift Helper```\n**Credits**\n> `Owner & Dev - {dev}`\n> `User & Lover - {client.user}`"
  )


@client.command()
async def uptime(ctx):
  await ctx.message.delete()
  uptime = datetime.datetime.utcnow() - starttime
  uptime = str(uptime).split('.')[0]
  await ctx.send(f"```Swift Helper```\n**Uptime**\n> `{uptime}`")


import re
import random


@client.command()
async def a(ctx):
  await ctx.message.delete()
  msg = await ctx.send('.')
  await msg.delete()


@client.command()
async def vouchtxtr(ctx):
  await ctx.message.delete()
  if ctx.message.reference:
    referenced_message = await ctx.channel.fetch_message(
      ctx.message.reference.message_id)
    if referenced_message.attachments:
      attachment = referenced_message.attachments[0]
      if attachment.filename.endswith('.txt'):
        attachment_data = await attachment.read()
        attachment_text = attachment_data.decode('utf-8')

        vouch_ids = re.findall(r'Vouch ID: (\d+)', attachment_text)

        # Check if there are at least 3 vouch IDs
        if len(vouch_ids) >= 3:
          random_vouches = random.sample(vouch_ids, 3)
        else:
          random_vouches = vouch_ids

        vouch_ids_str = ' '.join(random_vouches)
        await ctx.send(f'+get {vouch_ids_str}')


import re


@client.command()
async def vouchtxt(ctx):
  await ctx.message.delete()
  if ctx.message.reference:
    referenced_message = await ctx.channel.fetch_message(
      ctx.message.reference.message_id)
    if referenced_message.attachments:
      attachment = referenced_message.attachments[0]
      if attachment.filename.endswith('.txt'):
        attachment_data = await attachment.read()
        attachment_text = attachment_data.decode('utf-8')

        vouch_ids = re.findall(r'Vouch ID: (\d+)', attachment_text)
        last_3_vouches = vouch_ids[-3:]

        vouch_ids_str = ' '.join(last_3_vouches)
        await ctx.send(f'+get {vouch_ids_str}')


@client.command()
async def servericon(ctx):
  await ctx.message.delete()
  await ctx.send(
    f"```Swift Helper```\n**{ctx.guild.name}'s Server Icon**\n> ||{ctx.guild.icon_url}||"
  )


@client.command()
async def whois(ctx, user: discord.User):
  await ctx.message.delete()
  await ctx.send(
    f"```Swift Helper```\n**User Name**\n> `{user.name}#{user.discriminator}`\n**User ID**\n> `{user.id}`\n**Created At**\n> `{user.created_at}`\n**User Avatar Url**\n> `{user.avatar_url}`\n"
  )


@client.command()
async def serverinfo(ctx):
  await ctx.message.delete()
  guild = ctx.guild
  name = guild.name
  description = guild.description
  owner = guild.owner
  id = guild.id
  member_count = guild.member_count
  icon = guild.icon.url if guild.icon else None

  info = '**Server Information**\n\n'
  info += f'**Name:** {name}\n'
  info += f'**Description:** *{description}*\n'
  info += f'**Owner:** {owner}.\n'
  info += f'**ID:** {id}\n'
  info += f'**Member Count:** {member_count}\n'

  await ctx.send(info)


@client.command()
async def av(ctx, user: discord.User):
  await ctx.message.delete()
  await ctx.send(
    f"```Swift Helper```\n**{user}'s Avatar**\n> {user.avatar_url}")


@client.command()
async def calc(ctx, *, expression):
  try:
    result = eval(expression)
    await ctx.send(f'Result: {result}')
  except Exception as e:
    await ctx.send(f'Error: {e}')


@client.command()
async def getbal(ctx, ltcaddress):
  # Make a request to the BlockCypher API to get the balance of the LTC address
  response = requests.get(
    f'https://api.blockcypher.com/v1/ltc/main/addrs/{ltcaddress}/balance')

  balance = response.json()['final_balance'] / 10**8  # Convert satoshis to LTC

  # Make a request to the CoinGecko API to get the current price of LTC in USD
  cg_response = requests.get(
    'https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd'
  )
  usd_price = cg_response.json()['litecoin']['usd']

  # Convert the balance from LTC to USD
  usd_balance = balance * usd_price
  # Format the response message
  message = f" **The balance of `{ltcaddress}` is \n\n{usd_balance:.2f}$**"

  # Send the message to the user who invoked the command
  await ctx.reply(message)
@client.command()
async def any(ctx):
    await ctx.message.delete()
    await ctx.send("*Is there Any Thing Else We Can Help You With?*")


@client.command()
async def theme(ctx, theme):
  headers = {
    'authorization':
    TOKEN,
    "user-agent":
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9001 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36"
  }
  await ctx.message.delete()
  if theme == "dark":
    requests.patch("https://canary.discordapp.com/api/v9/users/@me/settings",
                   headers=headers,
                   json={'theme': "dark"})
    await ctx.send(f"```Swift Helper```\n**Discord Theme**\n> Dark Theme")
  if theme == "light":
    requests.patch("https://canary.discordapp.com/api/v9/users/@me/settings",
                   headers=headers,
                   json={'theme': "light"})
    await ctx.send(f"```Swift Helper```\n**Discord Theme**\n> Light Theme")
keep_alive()
try:
  tokenbot = os.getenv('TOKEN')
  client.run(tokenbot)
except discord.errors.LoginFailure:
  print(
    f"{Fore.CYAN}Swift Helper | {Fore.RED}ERROR: TOKEN IS INVALID!\n{Fore.RESET}Please put a valid token into config.json.\nTo get your token follow the tutorial here! https://www.youtube.com/watch?v=UN-8hBoDJYw"
  )
  os.system('pause >NUL')
