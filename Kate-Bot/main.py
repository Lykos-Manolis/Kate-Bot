import os
import discord
from discord.ext import commands, tasks
from replit import db

from handlers.reddit_handler import RedditOptimizer
from handlers.reaction_handler import ReactionHandler

from crawlers.anime_crawler import animeClient
from crawlers.reddit_crawler import postGenshin
from crawlers.pinterest_crawler import postPins

import commands.steam_commands as steam_commands
import commands.discord_commands as discord_commands
import commands.genshin_commands as genshin_commands
from commands.epic_commands import epicHandler

activity = discord.Activity(type=discord.ActivityType.playing,
                            name="Genshin Impact")
client = commands.Bot(command_prefix=["Kate ", "kate "],
                      help_command=None,
                      activity=activity,
                      status=discord.Status.idle)



# EVENTS


# when bot is ready
@client.event
async def on_ready():
    print("We have logged in as {}".format(client.user.name))
    postToRedditChannels.start()
    checkResin.start()
    getPins.start()
    weeklyEpicGame.start()


# handle steam reactions
@client.event
async def on_reaction_add(reaction, user):
    await ReactionHandler(reaction, user, client)


# TASKS

@tasks.loop(minutes=30)
async def postToRedditChannels():
    
    await postGenshin(
        client.get_channel(int(os.getenv('channel'))),
        'Genshin_Impact',
        sort='hot')
    
    await postGenshin(
        client.get_channel(int(os.getenv('channel'))),
        'Genshin_Memepact',
        sort='hot')
    
    await postGenshin(
        client.get_channel(int(os.getenv('channel'))),
        'wallpaper',
        sort='top')
    
    await postGenshin(
        client.get_channel(int(os.getenv('channel'))),
        'wallpapers',
        sort='top')
    
    await optimize_redditId_db()


@tasks.loop(minutes=10)
async def checkResin():
    for user in db['genshinUsers']:  
        await genshin_commands.checkResinCap(
            client.get_channel(int(os.getenv('channel'))), 
            int(user)
        )


@tasks.loop(minutes=5)
async def getPins():
    await postPins(client.get_channel(int(os.getenv('channel'))), 'tattoos')
    await postPins(client.get_channel(int(os.getenv('channel'))), 'genshin')

    
@tasks.loop(hours=1)
async def weeklyEpicGame():
  await epicHandler(client.get_channel(int(os.getenv('channel'))))




# COMMANDS


# base #
@client.command(aliases=["hi", "hey", "yo", "heyo", "whatsup"])
async def hello(ctx):
    await discord_commands.Greet(ctx)


@client.command(aliases=['clean', 'delete'])
async def clear(ctx, amount=1):
    await discord_commands.ClearMessages(ctx, amount)

@client.command()
async def help(ctx):
    await discord_commands.ShowHelp(ctx)

# genshin #
@client.command(aliases=['register genshin'])
async def register(ctx, ltuid, ltoken, uid):
    await discord_commands.ClearMessages(ctx, 0)
    await genshin_commands.registerUser(
        ctx, 
        str(ctx.message.author.id), 
        ltuid,
        ltoken, 
        uid
    )


@client.command(aliases=['unregister genshin'])
async def unregister(ctx):
    await discord_commands.ClearMessages(ctx, 0)
    await genshin_commands.unregisterUser(ctx, str(ctx.message.author.id))


@client.command(aliases=['comissions', 'resin'])
async def activities(ctx):
    await genshin_commands.getActivities(ctx, ctx.message.author.id)


@client.command(aliases=['daily', 'claim-dailies', 'claim'])
async def dailies(ctx):
    await genshin_commands.getDailies(ctx, ctx.message.author.id)


@client.command(aliases=['charactercount', 'cc'])
async def charcnt(ctx):
    await genshin_commands.getCharacterCount(ctx, ctx.message.author.id)


@client.command(aliases=['characters', 'c'])
async def chars(ctx):
    await genshin_commands.getCharacters(ctx, ctx.message.author.id)


@client.command(aliases=['primos', 'primogems'])
async def diary(ctx):
    await genshin_commands.getDiary(ctx, ctx.message.author.id)


# reddit #
@client.command()
async def optimize_redditId_db():
    RedditOptimizer()


@client.command()
async def restart_reddit(ctx):
    postToRedditChannels.restart()
    await ctx.send("Posted to reddit channels.")


# steam #
@client.command(aliases=['sales', 'steam'])
async def sale(ctx, amount=0):
    await steam_commands.GetSales(ctx, amount)


@client.command(aliases=['steamSearch', 'steamsearch', 'ss'])
async def steam_search(ctx, *, searchKeywords):
    await steam_commands.SteamSearch(ctx, searchKeywords)


# anime #
@client.command(aliases=['searchanime'])
async def anime(ctx, *, name):
    await clear(ctx, 0)
    await animeClient.setAnime(ctx, name)
    await animeClient.getAnime()

    
# run bot
client.run(os.getenv('TOKEN'))