import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask
import threading

app = Flask('')


@app.route('/')
def home():
    return "Bot is running!"


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = threading.Thread(target=run)
    t.start()


# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Define the intents for the bot to use
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# Create the bot client with a command prefix '!'
bot = commands.Bot(command_prefix='!', intents=intents)

# Remove the default help command to use your custom help command
bot.remove_command('help')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


# Command to say hello
@bot.command(name='hello')
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.mention}!')



# Command to respond with pong
@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('Pong!')


# Command to provide custom help (replaces default help)
@bot.command(name='help')
async def custom_help(ctx):
    embed = discord.Embed(title="Available commands",
                          color=discord.Color.blue())

    # Add the commands and their descriptions
    embed.add_field(name="!hello",
                    value="Sends a hello message.",
                    inline=False)
    embed.add_field(name="!ping",
                    value="Responds with 'Pong!'.",
                    inline=False)
    embed.add_field(name="!help",
                    value="Displays all the commands.",
                    inline=False)

    # Send the embed in the channel
    await ctx.send(embed=embed)


# Command to test welcome message
@bot.command(name='welcome-test')
async def welcome_test(ctx):
    channel_id = 123456789012345678  # Replace with your channel ID
    channel = bot.get_channel(channel_id)
    if channel is not None:
        embed = discord.Embed(
            title=f"Welcome {ctx.author.display_name}",
            description=
            f"to {ctx.guild.name}\nYou are the {len(ctx.guild.members)}th user!",
            color=discord.Color.blue())
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await channel.send(embed=embed)


@bot.event
async def on_member_join(member):
    # Replace 123456789012345678 with your channel's ID
    channel_id = 123456789012345678  # Replace with your channel ID
    channel = member.guild.get_channel(channel_id)
    if channel is not None:
        embed = discord.Embed(
            title=f"Welcome {member.display_name}",
            description=
            f"to {member.guild.name}\nYou are the {len(member.guild.members)}th user!",
            color=discord.Color.blue())
        embed.set_thumbnail(url=member.avatar.url)
        await channel.send(embed=embed)


@bot.event
async def on_member_remove(member):
    # Replace 123456789012345678 with your channel's ID
    channel_id = 1217890877398319154  # Replace with your channel ID
    channel = member.guild.get_channel(channel_id)
    if channel is not None:
        embed = discord.Embed(
            title=f"Goodbye {member.display_name}",
            description=
            f"{member.display_name} has left {member.guild.name}. We now have {len(member.guild.members)} members.",
            color=discord.Color.red())
        embed.set_thumbnail(url=member.avatar.url)
        await channel.send(embed=embed)


# Run the bot
keep_alive()
bot.run(TOKEN)
