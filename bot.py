# Documentation for discord.py library: https://discordpy.readthedocs.io/en/stable/


import discord
from discord.ext import commands
import datetime
import discord.ui
import asyncio
from discord.ui import View, Button, Select
import json
import logging

# Load configuration from config.json
# For others using my code, please change this file directory
# Follow this format
#   {
#       "token": "",
#       "prefix": "!",
#       "owner_id": "",
#       "tickets_channel_id": "",
#       "mod_logs_channel_id": ""
#   }
try:
    with open('C:/Users/Ciderly/Documents/Discord bot/config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    print("Error: config.json not found.")

    

bot = commands.Bot(command_prefix=config["prefix"], intents=discord.Intents.all())
bot.remove_command("help")
# Dictionary to store the current ticket numbers for each type
ticket_numbers = {"help": 1, "coins": 1}




#Things to check when the bot runs
@bot.event
async def on_ready():
    await bot.change_presence(
    activity=discord.Game(name="Cleaning Ciderly's room"),
    status=discord.Status.online
    )

    # Configure logging
    logging.basicConfig(level=logging.INFO)  # Set the logging level to INFO or DEBUG for more detailed information
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)  # Set the logging level for the 'discord' logger

    # Create a file handler to log to a file
    file_handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='a')
    file_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

    # Add the file handler to the 'discord' logger
    logger.addHandler(file_handler)

    # Log an informational message
    logger.info('Bot is online and ready!')

    # Log a warning
    logger.warning('User attempted to use a command without permission')

    # Log an error
    logger.error('An error occurred while processing a command', exc_info=True)


    try:
        print(f"{bot.user.name} is currently online. Welcome, master.")
      

    except discord.LoginFailure:
        print("Bot failed to log in. Check the provided token.")
        # Optionally, I can raise the exception to stop the bot from continuing
        # raise

    except discord.HTTPException as e:
        print(f"An HTTP error occurred: {e}")
        # Handle HTTP exceptions, which can occur during the bot's interaction with Discord

    except Exception as e:
        print(f"An unexpected error occurred during startup: {e}")
        # Handle other exceptions that are not explicitly caught above
        # Optionally, I can raise the exception to stop the bot from continuing.. I might be too lazy to add this
        # raise

@bot.command()
async def hello(ctx):
    username = ctx.message.author.mention
    await ctx.send("Hello there, " + username + ". To use our services, head to the tickets channel to request for a ticket!")

@bot.command()
@commands.has_any_role("Developer", "Administrator")
async def rules(ctx):
    rules_embed = discord.Embed(title="Server Rules", color=0x02F0FF)

    rules_text = [
        "By joining this server, you acknowledge that you have read and agreed to the rules stated in the various ToS in each channel. Please cooperate with us in maintaining a positive experience in this server by following these rules. If you have any questions or issues, please create a ticket for assistance.",
        "Breaking the rules will result in a warning, DWC rank, or a temporary server ban, and repeated violations will lead to a permanent ban. The severity and frequency of the violations will determine the consequences.",
        "Please note that server policies are subject to change at any time, and staff have the right to ban or mute anyone for any reason without warning.",
        "1. **Be respectful:** You must respect all users, regardless of your liking towards them. Treat others the way you want to be treated.",
        "2. **No Inappropriate Language:** The use of profanity should be kept to a minimum. However, any derogatory language towards any user is prohibited.",
        "3. **No Spamming:** Don't send a lot of small messages right after each other. Do not disrupt chat by spamming.",
        "4. **No NSFW Material:** No pornographic/adult/other NSFW material outside #nsfw. This is a community server and not meant to share this kind of material.",
        "5. **No Advertisements:** We do not tolerate any kind of advertisements, whether it be for other communities or streams. You can post your content in the media channel if it is relevant and provides actual value (Video/Art)",
        "6. **No Offensive Names and Profile Pictures:** You will be asked to change your name or picture if the staff deems them inappropriate.",
        "7. **No Server Raiding:** Raiding or mentions of raiding are not allowed.",
        "8. **No Threats:** Direct & Indirect threats to other users of DDoS, Death, DoX, abuse, and other malicious threats are absolutely prohibited and disallowed.",
        "9. **Follow Discord Community Guidelines:** You can find them [here](https://discordapp.com/guidelines).",
        "10. **No Exploits, Fraudulent Activity, Spam, and Scams:** Not permitted. Use your common sense.",
        "11. **No Bullying, Harassment, Racism, Doxing:** Also, leaking personal/private information, hijacking, or compromising accounts.",
        "12. **No Malicious Links/Files:** Do not send harmful links/files or harmful threads towards other users.",
        "13. **No Advertisement of Services:** The advertisement of any services, such as boosting or unban services, is strictly prohibited.",
        "14. **Marketplace Rules:** The marketplace is exclusively for the sale of Apex Legends accounts. Sellers must be transparent about their prices and not engage in price gouging or scams.",
        "15. **Marketplace Exclusivity:** The marketplace is exclusively for Apex Legends Coins. Listings for other games, such as Valorant or Fortnite, are not allowed."
    ]

    rules_embed.description = "\n".join(rules_text)
    rules_embed.set_footer(text="Server rules are subject to change. Last updated: {3/7/2024}")
    
    await ctx.send(embed=rules_embed)
        

    information_channel = discord.utils.get(ctx.guild.channels, name="information")

# Ban command
@bot.command()
@commands.has_any_role("Developer", "Administrator")
async def ban(ctx, member: discord.Member, *, reason=None):
    if reason is None:
        reason = f"This user was banned by {ctx.author.display_name}"
    await member.ban(reason=reason)
    
    modlogs = int(config["mod_logs_channel_id"])
    await modlogs.send(f"{member.name} was successfully banned by {ctx.author.display_name} for reason: {reason}")
    
    await ctx.send(f"Successfully banned {member.mention} for reason: {reason}")

# Kick command
@bot.command()
@commands.has_any_role("Developer", "Administrator")
async def kick(ctx, member: discord.Member, *, reason=None):
    if reason is None:
        reason = f"This user was kicked by {ctx.author.display_name}"
    await member.kick(reason=reason)
    
    modlogs = int(config["mod_logs_channel_id"])
    await modlogs.send(f"{member.name} was successfully kicked by {ctx.author.display_name} for reason: {reason}")
    
    await ctx.send(f"Successfully kicked {member.mention} for reason: {reason}")


# Mute command
@bot.command()
@commands.has_any_role("Developer", "Administrator")
async def mute(ctx, member:discord.Member, timelimit):
    if "s" in timelimit:
        gettime = timelimit.strip("s")
        if int(gettime) > 2419000:
            await ctx.send("Mute time amount cannot be bigger than 28 days. Are you stupid, master?")
        else:
            newtime = datetime.timedelta(seconds=int(gettime))
            await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
            modlogs = int(config["mod_logs_channel_id"])
            await ctx.send(f"{member.name} was successfuly muted by {ctx.message.author.mention} for {str(gettime)} seconds")
    elif "m" in timelimit:
        gettime = timelimit.strip("m")
        if int(gettime) > 40320:
            await ctx.send("Mute time amount cannot be bigger than 28 days. Are you stupid, master?")
        else:
            newtime = datetime.timedelta(minutes=int(gettime))
            await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
            modlogs = int(config["mod_logs_channel_id"])
            await ctx.send(f"{member.name} was successfuly muted by {ctx.message.author.mention} for {str(gettime)} minutes")    
    elif "h" in timelimit:
        gettime = timelimit.strip("h")
        if int(gettime) > 672:
            await ctx.send("Mute time amount cannot be bigger than 28 days. Are you stupid, master?")
        else:
            newtime = datetime.timedelta(hours=int(gettime))
            await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
            modlogs = int(config["mod_logs_channel_id"])
            await ctx.send(f"{member.name} was successfuly muted by {ctx.message.author.mention} for {str(gettime)} hours")    
    elif "d" in timelimit:
        gettime = timelimit.strip("d")
        if int(gettime) > 28:
            await ctx.send("Mute time amount cannot be bigger than 28 days. Are you stupid, master?")
        else:
            newtime = datetime.timedelta(days=int(gettime))
            await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
            modlogs = int(config["mod_logs_channel_id"])
            await ctx.send(f"{member.name} was successfuly muted by {ctx.message.author.mention} for {str(gettime)} days")

    mod_logs_channel_id = int(config["mod_logs_channel_id"])  # Replace with your mod logs channel ID
    mod_logs_channel = bot.get_channel(mod_logs_channel_id)

    if mod_logs_channel:
        log_message = f"{member.name} was muted by {ctx.author.mention} for {gettime} seconds"
        embed = discord.Embed(
            title="Member Muted",
            description=log_message,
            color=0xFF0000  # Red color for emphasis
        )
        await mod_logs_channel.send(embed=embed)


# Unmute command
@bot.command()
@commands.has_any_role("Developer", "Administrator")
async def unmute(ctx, member:discord.Member):
    await member.edit(timed_out_until=None)

    mod_logs_channel_id = int(config["mod_logs_channel_id"])  # Replace with your mod logs channel ID
    mod_logs_channel = bot.get_channel(mod_logs_channel_id)

    if mod_logs_channel:
        log_message = f"{member.name} was unmuted by {ctx.author.mention}"
        embed = discord.Embed(
            title="Member Unmuted",
            description=log_message,
            color=0x00FF00  # Green color for emphasis
        )
        await mod_logs_channel.send(embed=embed)


# Help command
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Command Help",
        description="Below is a list of commands available for Stella.",
        color=0x02F0FF
    )
    embed.add_field(name="`!ban`", value="Ban a user. Requires the Master's permission.", inline=False)
    embed.add_field(name="`!kick`", value="Kick a user. Requires the Master's permission.", inline=False)
    embed.add_field(name="`!mute`", value="Mute a user. Requires the Master's permission.", inline=False)
    embed.add_field(name="`!unmute`", value="Unmute a user. Requires the Master's permission.", inline=False)
    embed.set_footer(text="Bot created with love by Ciderly")
    embed.set_thumbnail(url="https://i.pinimg.com/originals/05/6c/58/056c584d9335fcabf080ca43e583e3c4.gif")
    embed.set_author(name="Ciderly", url="https://github.com/Ciderlyy")

    # Additional information about the #ticket channel
    ticket_channel = discord.utils.get(ctx.guild.channels, name="ticket")
    owner_mention = ctx.guild.owner.mention if ctx.guild.owner else "the server owner"

    if ticket_channel:
        embed.add_field(
            name="Support and Apex Coins",
            value=f"For delightful support or to buy Apex Coins, please head to {ticket_channel.mention} and use the command !ticket.",
            inline=False
        )
    else:
        embed.add_field(
            name="Support and Apex Coins",
            value=f"For delightful support or to buy Apex Coins, please head to the #ticket channel and use the command !ticket.",
            inline=False
        )

    # Encourage users to go to the #ticket channel and ping the owner
    embed.add_field(
        name="Need assistance?",
        value=f"If you have any issues or questions, don't hesitate to ping {owner_mention}.",
        inline=False
    )

    await ctx.send(embed=embed)


# Creates a ticket (P.S: This shit gave me the worst headache. I dont know why it doesnt work when i use buttons, so i just used a dropdown instead)
@bot.command()
async def ticket(ctx):
    try:
        # Your existing code for ticket creation here

        guild = ctx.guild
        overwrites = {}  # Define your overwrites as needed

        select = discord.ui.Select(options=[
            discord.SelectOption(label="Help Ticket", value="help", emoji="😊", description="Opens a help ticket"),
            discord.SelectOption(label="Buy coins", value="coins", emoji="💰", description="Opens a ticket to buy apex coins")
        ])

        async def my_callback(interaction):
            try:
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    ctx.author: discord.PermissionOverwrite(read_messages=True)
                }

                selected_value = interaction.data["values"][0]

                # Default category name for unmatched options
                default_category_name = "Other"

                if selected_value == "help":
                    category_name = "Tickets"
                elif selected_value == "coins":
                    category_name = "Tickets"
                else:
                    category_name = default_category_name

                category = discord.utils.get(guild.categories, name=category_name)

                if category is None:
                    print(f"Category '{category_name}' not found. Creating channel in the default category.")
                    category = discord.utils.get(guild.categories, name=default_category_name)

                # Get the next available ticket number based on the type of ticket
                ticket_number = get_next_ticket_number(guild, category, selected_value)

                # Update the ticket_numbers dictionary
                ticket_numbers[selected_value] = ticket_number + 1

                # Determine the channel name based on the type of ticket
                ticket_type_prefix = "helpticket" if selected_value == "help" else "cointicket"
                username = ctx.author.name  # Use ctx.author.name to get the username
                channel_name = f"{username}-{ticket_type_prefix}{ticket_number:03d}"

                print(f"Creating channel: {channel_name} in category: {category.name} with ticket number: {ticket_number}")

                # Create the text channel
                channel = await guild.create_text_channel(channel_name, category=category, overwrites=overwrites)
                await interaction.response.send_message(f"Created ticket - <#{channel.id}>", ephemeral=True)
                await channel.send(f"Hello, how can I help? Please ping my master {ctx.guild.owner.mention} if needed. he's a really lazy person...")

            except Exception as ticket_creation_error:
                print(f"An unexpected error occurred during ticket creation: {ticket_creation_error}")
                # Log the error or handle it appropriately

        select.callback = my_callback
        view = discord.ui.View(timeout=None)
        view.add_item(select)
        await ctx.send("Choose an option below", view=view)

    except Exception as command_error:
        print(f"An unexpected error occurred during the 'ticket' command: {command_error}")
        # Log the error or handle it appropriately

# Takes next ticket number
def get_next_ticket_number(guild, category, ticket_type):
    # Get the current ticket number for the given type
    current_ticket_number = ticket_numbers.get(ticket_type, 1)

    # Return the current ticket number
    return current_ticket_number


    

@bot.command()
async def close_ticket(ctx):
    # Check if the channel has a category and the category name is "Tickets"
    if ctx.channel.category and ctx.channel.category.name == "Tickets":
        # Ask for confirmation
        embed = discord.Embed(
            title="Close Ticket Confirmation",
            description="Are you sure you want to close this ticket?",
            color=discord.Color.gold()
        )
        confirmation_message = await ctx.send(embed=embed, delete_after=60.0)
        
        # Add reactions for confirmation
        await confirmation_message.add_reaction("✅")  # Checkmark emoji
        await confirmation_message.add_reaction("❌")  # Cross emoji

        def check(reaction, user):
            # Check if the reacting user is a moderator
            is_moderator = discord.utils.get(ctx.guild.roles, name="Developer") in user.roles
            return is_moderator and reaction.message.id == confirmation_message.id

        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=60.0, check=check)

            if str(reaction.emoji) == "✅":
                # User confirmed, close the ticket
                await ctx.channel.delete()
                await ctx.send("Ticket closed successfully.", delete_after=5.0)
            else:
                # User canceled the operation
                await ctx.send("Ticket closure canceled.", delete_after=5.0)
        except TimeoutError:
            # User didn't react within the timeout period
            await ctx.send("Ticket closure timed out. Operation canceled.", delete_after=5.0)
    else:
        # Inform non-moderators that only moderators can close tickets (ephemeral message)
        await ctx.send("Only moderators can close tickets.", delete_after=5.0)



@bot.event
# This is for join and leave logs
async def on_member_join(member):

    welcome_message = (
        f"Welcome to the server, {member.mention}!\n\n"
        "Feel free to use the `!tickets` command to buy apex coins from us!"
    )
    await member.send(welcome_message)
    logschannel = bot.get_channel(1215192401736507453)
    embed = discord.Embed(title="New Member Joined", description=f"{member.mention} joined the server!", color=0x71FFAA)
    embed.set_thumbnail(url="https://gifdb.com/images/high/beautiful-anime-cute-wave-zid7nvnjycvq4p7k.gif")
    embed.set_footer(text="Welcome to project inu!")
    await logschannel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    farewell_message = f"Goodbye, {member.name}! We hope to see you again soon."
    await member.send(farewell_message)
    logschannel = bot.get_channel(1215192401736507453)
    embed = discord.Embed(title="A Member Just Left", description=f"{member.name} left the server...", color=0x71FFAA)
    embed.set_thumbnail(url="https://i.pinimg.com/originals/32/82/a8/3282a83025d5f2eb8bfa799bbf13874b.gif")
    embed.set_footer(text="Farewell from project inu!")
    await logschannel.send(embed=embed)

@bot.event
async def on_message_delete(message):
    mod_logs_channel_id = 1215195521266745364  # Replace with your mod logs channel ID
    mod_logs_channel = bot.get_channel(mod_logs_channel_id)

    if mod_logs_channel:
        deleted_message_info = f"Author: {message.author.mention}\n"
        deleted_message_info += f"Channel: {message.channel.mention}\n"
        deleted_message_info += f"Deleted Message: {message.content}"

        embed = discord.Embed(
            title="Message Deleted",
            description=deleted_message_info,
            color=0xFF0000  # Red color for emphasis
        )

        await mod_logs_channel.send(embed=embed)

# Global variable to store the role selection message ID
role_selection_message_id = None

import discord

@bot.command()
async def setroles(ctx):
    await send_role_selection_message(ctx, "Gender", ["Male", "Female", "Non-Binary"])
    await send_role_selection_message(ctx, "Region", ["Global", "Europe", "Asia", "Other"])
    await send_yes_no_selection_message(ctx, "Announcements")

async def send_role_selection_message(ctx, category, options):
    # Emoji constants
    GENDER_EMOJI_OPTIONS = ["👨", "👩", "👦"]
    REGION_EMOJI_OPTIONS = ["🌍", "🌐", "🌏", "🏡"]
    YES_NO_EMOJI = ["✅", "❌"]

    # Use different emoji options based on the category
    emoji_options = GENDER_EMOJI_OPTIONS if category == "Gender" else REGION_EMOJI_OPTIONS

    # Create an embed
    embed = discord.Embed(title=f"Role Selection - {category}", color=discord.Color.blue())
    embed.description = f"Welcome! Let's set up your roles. Please react to the corresponding emoji for each selection."

    # Add options to the embed
    for emoji, option in zip(emoji_options[:len(options)], options):
        embed.description += f"\n{emoji} {option}"

    # Send the embed
    role_message = await ctx.send(embed=embed)

    # Add reactions for options
    for emoji in emoji_options[:len(options)]:
        await role_message.add_reaction(emoji)

async def send_yes_no_selection_message(ctx, category):
    # Emoji constants
    YES_NO_EMOJI = ["✅", "❌"]

    # Create an embed
    embed = discord.Embed(title=f"Role Selection - {category}", color=discord.Color.blue())
    embed.description = f"Lastly, would you like to receive announcements? React accordingly."

    # Add options to the embed
    for emoji, option in zip(YES_NO_EMOJI, ["Yes", "No"]):
        embed.description += f"\n{emoji} {option}"

    # Send the embed
    role_message = await ctx.send(embed=embed)

    # Add reactions for options
    for emoji in YES_NO_EMOJI:
        await role_message.add_reaction(emoji)




#purge messages
@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx):
    # Check if the user has the 'Manage Messages' permission
    await ctx.channel.purge(limit=None)
    await ctx.send("By your command, the chat has been purged.", delete_after=5.0)

#clean messages
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clean(ctx, amount: int):
    # Check if the user has the 'Manage Messages' permission
    await ctx.channel.purge(limit=amount + 1)  # +1 to include the command itself
    await ctx.send(f"Master, {amount} messages have been cleaned.", delete_after=5.0)
#check for permissions
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the required permissions to use this command.")



#apex channel ticket
@bot.command()
async def apexcoins(ctx):
    # Create an embed with the desired formatting and emojis
    embed = discord.Embed(
        title="Discounted Apex Coins",
        description="We are reintroducing Cheap Apex Coins - this time it works a bit differently! It works on all platforms",
        color=discord.Color.green()
    )
    
    embed.add_field(name="🚀 Instant top up", value="$80 for 11.0K Coins (Normally $120)\n$140 for 22.0K Coins (Normally $240)\n$200 for 34.5K Coins (Normally $360)", inline=False)
    embed.add_field(name="🚀 Instant topup", value="We do it on your main account", inline=False)
    embed.add_field(name="💼 Smurf top up", value="$65 for 11.0K Coins (Normally $120)\n$110 for 22.0K Coins (Normally $240)\n$160 for 34.5K Coins (Normally $360)", inline=False)
    embed.add_field(name="💼 Smurf top up", value="We top up your smurf account (Has to be low level otherwise it will be considered a main account)", inline=False)

    # Send the embed
    await ctx.send(embed=embed)
    
    # Add a simple text message with a link to the tickets channel
    tickets_channel = bot.get_channel(int(config["tickets_channel_id"]))
    await ctx.send(f"🎫 Click [here](https://discord.com/channels/{ctx.guild.id}/{config['ticket_channel_id']}) to open a ticket!(Type !tickets)")

bot.run(config["token"])