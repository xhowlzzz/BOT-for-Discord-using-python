import os
import discord
from discord.ext import commands
import asyncio
import random
from flask import Flask
from threading import Thread

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

reacted_users = []  # Define reacted_users as a global variable

app = Flask('')

@app.route('/')
def home():
    return "<b>Hack The Planet</b>"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global reacted_users  # Reference the global variable

    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('!'):
        await message.delete()  # Delete the user's message if it starts with '!'

@bot.command(name='pacific')
async def pacific(ctx):
    global reacted_users  # Reference the global variable

    # Send message asking for reactions
    react_message = await ctx.send('@everyone react pentru pacific')
    # Add verify reaction
    await react_message.add_reaction('✅')

    # Initialize reaction count
    reaction_count = 0
    reacted_users = []  # Reset the reacted_users list
    while reaction_count < 21:
        # Wait for reactions
        reaction, user = await ctx.bot.wait_for('reaction_add')
        # If the reaction is on the correct message
        if reaction.message.id == react_message.id and str(reaction.emoji) == '✅':
            reacted_users.append(user.name)
            reaction_count += 1
        # If someone reacts and they go over the limit, delete their reaction
        if reaction_count >= 21:
            await reaction.remove(user)

    # Create and send list of users who reacted
    react_list = '\n'.join(reacted_users)
    await ctx.send(f"Lista cu reacturile:\n{react_list}")

@bot.command(name='seif')
async def choose(ctx):
    global reacted_users  # Reference the global variable

    if len(reacted_users) >= 2:  # Check if there are at least 2 users to choose from
        chosen_users = random.sample(reacted_users, k=2)
        await ctx.send(f"Seifarii sunt: {chosen_users[0]} and {chosen_users[1]}")

        # Send list of users who reacted
        react_list = '\n'.join(reacted_users)
        await ctx.send(f"List of users who reacted:\n{react_list}")

        reacted_users.clear()  # Clear the reacted_users list after choosing users
    else:
        await ctx.send("Nu sunt destule reacturi.")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command.")

try:
    token = os.getenv("TOKEN") or ""
    if token == "":
        raise Exception("Please add your token to the Secrets pane.")
    keep_alive()  # Start the Flask app
    bot.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
        print("Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
    else:
        raise e
