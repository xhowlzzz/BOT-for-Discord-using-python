import discord
from discord.ext import commands
import random

# Define intents
intents = discord.Intents.all()
intents.reactions = True  # Enable reaction intents

# Initialize the bot with intents
bot = commands.Bot(command_prefix='!', intents=intents)

# List to store names
name_list = []

# Command to send the message with reactions and list
@bot.command()
async def pacific(ctx):
    global name_list
    embed = discord.Embed(title="Jaf Pacific", description="React with ✅ to add your name or ❌ to remove it from the list", color=0x00ff00)
    message = await ctx.send(embed=embed)

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ['✅', '❌'] and reaction.message.id == message.id

    await message.add_reaction('✅')
    await message.add_reaction('❌')

    while True:
        reaction, user = await bot.wait_for('reaction_add', check=check)
        if str(reaction.emoji) == '✅':
            if user.display_name not in name_list:
                name_list.append(user.display_name)
        elif str(reaction.emoji) == '❌':
            if user.display_name in name_list:
                name_list.remove(user.display_name)
        
        await update_message(message)

async def update_message(message):
    global name_list
    embed = discord.Embed(title="Jaf Pacific", description="React with ✅ to add your name or ❌ to remove it from the list", color=0x00ff00)
    embed.add_field(name="Names", value="\n".join(name_list) if name_list else "No names in the list")
    await message.edit(embed=embed)

# Command to choose 2 random names from the list and send a message
@bot.command()
async def seif(ctx):
    global name_list
    if len(name_list) < 2:
        await ctx.send("There are not enough names in the list.")
        return

    chosen_names = random.sample(name_list, 2)
    await ctx.send(f"Seifarii sunt: {chosen_names[0]} și {chosen_names[1]}")

# Run the bot
bot.run('token')
