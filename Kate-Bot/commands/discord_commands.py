from replit import db
import discord
import random

async def Greet(ctx):
    greet = ["Hey!","Sup.","Greetings Traveler","Wassup.. bitch.","Hello!","Greetings!","Ad astra abyssosque."]
    await ctx.send(random.choice(greet))

async def ClearMessages(ctx, amount):
    await ctx.channel.purge(limit=amount+1)

async def PlayRPS(ctx,userChoice):
    await ClearMessages(ctx,0)
    choiceList = ['rock','paper','scissors']
  
    if(userChoice == None):
        userChoice = random.choice(choiceList)
    else:
        userChoice = userChoice.lower()

    botChoice = random.choice(choiceList)
  
    if(userChoice not in choiceList):
        await ctx.send('{} is not an option'.format(userChoice.capitalize()))
    else:
        indexDif = choiceList.index(botChoice) - choiceList.index(userChoice)
        if(indexDif == 0):
            endMessage = "Uh oh.. it's a tie"
        elif(indexDif == 1 or indexDif == -2):
            endMessage = 'I won!'
            db["score"]['bot'] += 1
        else:
            endMessage = 'You won!'
            db["score"]['users'] += 1

    if(userChoice == 'paper'):
        userChoice = 'scroll'
    if(botChoice == 'paper'):
        botChoice = 'scroll'
  
    embed = discord.Embed(title="Rock Paper Scissors", colour=discord.Colour(0xff379b))
    embed.add_field(name="------------------------------", value="```Me: {}   You: {}```".format(db["score"]['bot'],db["score"]['users']),inline=False)
    embed.add_field(name=":{}: `vs` :{}:".format(userChoice,botChoice), value="\n\n{}".format(endMessage),inline=False)
    await ctx.send(embed=embed)  

async def ShowHelp(ctx):
    embed = discord.Embed(title="💥 My Commands 💥", colour=discord.Colour(0xff0081), description="-------------------------------------")

    embed.add_field(name="🧼 -- __clear an amount of messages__", value="`kate clear (amount)  {delete/clean}`", inline=False)
    embed.add_field(name="👋🏻 -- __greet me__", value="`kate hello  {any greeting message}`", inline=False)
    embed.add_field(name="🏷 -- __get steam sales__", value="`kate sales [amount]  {sale/steam}`", inline=False)
    embed.add_field(name="🔎 -- __search steam games__", value="`kate steam_search [game] {steamsearch/steamSearch/ss}`", inline=False)
    embed.add_field(name="💢 -- __search anime__", value="`kate anime [name] {searchAnime}`", inline=False)
    embed.add_field(name="📥 -- __register genshin account__", value="`kate register [ltuid ltoken uid]`", inline=False)
    embed.add_field(name="📤 -- __unregister genshin account__", value="`kate unregister`", inline=False)
    embed.add_field(name="📃 -- __view your genshin activities__", value="`kate activities {resin/commisions}`", inline=False)
    embed.add_field(name="💰 -- __get genshin daily rewards__", value="`kate dailies  {daily/claim dailies/claim}`", inline=False)
    embed.add_field(name="🔢 -- __get the number of your genshin characters__", value="`kate character count  {charcnt/cc}`", inline=False)
    embed.add_field(name="🦸‍♀️ -- __get a list of your genshin characters__", value="`kate characters  {chars/c}`", inline=False)
    embed.add_field(name="📚 -- __view your genshin diary__ (primos spent)", value="`kate diary  {primos/primogems}`", inline=False)
    embed.add_field(name="🔧 -- __reset reddit database__ (dev)", value="`kate reset_db`", inline=False)
    embed.add_field(name="🔨 -- __force post to reddit channels__ (dev)", value="`kate restart_reddit`", inline=False)
  
    await ctx.send(embed=embed)