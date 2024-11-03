import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands
import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = discord.Bot()


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.slash_command(name='roll', description='Rolls a random number from 0 - 100.')
async def random_roll(ctx: discord.ApplicationContext):
    response = f"🎲 {ctx.author.mention} rolled a {random.randrange(0, 100, 1)}! 🎲"
    await ctx.respond(response)


@bot.slash_command(name='raidtime', description='Returns the time of the raid.')
async def raid_time(ctx: discord.ApplicationContext):
    weekday = int(datetime.datetime.now().strftime("%w"))
    raidDays = [0]
    hour = int(datetime.datetime.now().strftime("%H"))
    tillRaid = 20 - hour
    tillRaid = 0 if tillRaid < 0 else tillRaid

    if weekday in raidDays:
        response = f"{ctx.author.mention}, raid time is at 8pm EST Sundays! There is a raid today at 8pm EST!\n\n There are approximately {tillRaid} hours until the next raid!"
    else:
        response = f"{ctx.author.mention}, raid time is at 8pm EST Sundays!"
    await ctx.respond(response)


@bot.slash_command(name='slap', description='Makes the Quan-Bot slap someone!')
async def slap(ctx: discord.ApplicationContext, user: discord.Member):
    await ctx.respond(f"{user.mention}"
                      f"```"
                      f"{bot.user.name} slaps {user.display_name}! 🫲"
                      f"```")


@bot.slash_command(name='bid', description='Places a bid on an item in the item-requests channel.')
async def bid(ctx: discord.ApplicationContext, reputation=None):
    try:
        channel = str(ctx.channel.parent)
        username = ctx.author.display_name
        itemname = str(ctx.channel.name)

        if channel == "item-requests":
            try:
                reputation = int(reputation)
            except (ValueError, TypeError):
                reputation = "Unknown"

            await ctx.respond(f"```"
                              f"{username} has bid on the item. ☝ \n\n"
                              f"*Roll: {random.randrange(0, 100, 1)}\n"
                              f"*Reputation: {reputation}\n"
                              f"```")
            msg = f"Thank you, {username}. We have received your bid for the {itemname} and it will be considered. \nGood luck!"
            user = await bot.fetch_user(ctx.author.id)
            await user.send(msg)
        else:
            await ctx.respond("Sorry, you can only bid in the item requests forum.", ephemeral=True)
    except AttributeError:
        await ctx.respond("Sorry, you can only bid in the item requests forum.", ephemeral=True)


class MyView(discord.ui.View):  # Create a class called MyView that subclasses discord.ui.View
    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.primary, emoji="😎")  # Create a button with the label "😎 Click me!" with color Blurple
    async def button_callback(self, button, interaction):
        await interaction.response.send_message("You clicked the button!")  # Send a message when the button is clicked


@bot.slash_command()  # Create a slash command
async def button(ctx):
    await ctx.respond("This is a button!", view=MyView())  # Send a message with our View class that contains the button


bot.run(TOKEN)
