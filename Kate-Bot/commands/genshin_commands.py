import genshin
import discord
from replit import db


# register
async def registerUser(ctx, usr, ltuid, ltoken, uid):
    if (usr in db['genshinUsers'].keys()):
        await ctx.send(
            'You are already registered. If you want to unregister use the "Kate unregister" command'
        )
        return

    db['genshinUsers'] = {usr: {'ltuid': ltuid, 'ltoken': ltoken, 'uid': uid}}
    db["hasCapped"] = {usr:False}
    await ctx.send("You have been successfully registered!")


# unregister
async def unregisterUser(ctx, usr):
    if (usr not in db['genshinUsers'].keys()):
        await ctx.send('You are not registered')
        return
    del db['genshinUsers'][usr]
    await ctx.send(
        'You are no longer registered. Use the "Kate register" command to register.'
    )


# log in client
async def login(usr, ctx):
    global gClient
    global ltuid
    global ltoken
    global uid

    # check if user is registered
    if (str(usr) not in db['genshinUsers'].keys()):
        await ctx.send(
            'You are not registered. Use the command "Kate register" to register'
        )
        return False

    # set client details for current user
    ltuid = int(db['genshinUsers'][str(usr)]['ltuid'])
    ltoken = db['genshinUsers'][str(usr)]['ltoken']
    uid = int(db['genshinUsers'][str(usr)]['uid'])

    # create client instance
    gClient = genshin.GenshinClient()
    # set client and cookies
    cookies = {"ltuid": ltuid, "ltoken": ltoken}
    gClient.set_cookies(cookies)
    return True


# log out client
async def logout():
    # await gClient.close()
    pass


# get activities:
async def getActivities(ctx, usr):
    if (not await login(usr, ctx)):
        return
    notes = await gClient.get_notes(int(uid))
    embed = discord.Embed(title="Your Daily Activities Progression:",
                          color=13632027)
    embed.add_field(name="Comissions",
                    value="{}/{}".format(4 - notes.completed_commissions, 4),
                    inline=True)
    embed.add_field(name="Resin",
                    value="{}/{}".format(notes.current_resin, notes.max_resin),
                    inline=True)
    await ctx.send(embed=embed)
    await logout()


# alert if resin has maxed
async def checkResinCap(ctx, usr):
    if (not await login(usr, ctx)):
        return
    notes = await gClient.get_notes(int(uid))
    if notes.current_resin < 160 and db["hasCapped"][str(usr)] == True:
        db["hasCapped"][str(usr)] = False
    if notes.current_resin == 160 and db["hasCapped"][str(usr)] == False:
        embed = discord.Embed(
            title="IMPORTANT!",
            colour=discord.Colour(0xff001f),
            description="<@{}> your resin has maxed out!".format(usr))
        embed.set_image(
            url=
            "https://static.wikia.nocookie.net/gensin-impact/images/6/66/Icon_Emoji_015_Aether_Alert.png"
        )
        embed.add_field(name="...............", value="`160/160`")
        await ctx.send(embed=embed)
        db["hasCapped"][str(usr)] = True

    await logout()


# get dailies
async def getDailies(ctx, usr):
    if (not await login(usr, ctx)):
        return
        
    try:
        reward = await gClient.claim_daily_reward()
    except genshin.AlreadyClaimed:
        embed = discord.Embed(title="Your Dailies Progression",
                              description="Daily rewards already claimed",
                              color=13632027)
        embed.set_image(
            url=
            "https://static.wikia.nocookie.net/gensin-impact/images/8/83/Icon_Emoji_085_Yanfei_No_problem.png"
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Your Dailies Progression",
                              description="Claimed {}x{}".format(
                                  reward.amount, reward.name),
                              color=13632027)
        embed.set_image(
            url=
            "https://static.wikia.nocookie.net/gensin-impact/images/a/a7/Icon_Emoji_088_Yanfei_Pleased.png"
        )
        await ctx.send(embed=embed)
    await logout()


# get character count
async def getCharacterCount(ctx, usr):
    if (not await login(usr, ctx)):
        return
    user = await gClient.get_user(uid)
    await ctx.send(
        "Currently, you have {} characters in your account.\nUse 'characters' command to view them."
        .format(len(user.characters)))
    await logout()


# get characters
async def getCharacters(ctx, usr):
    if (not await login(usr, ctx)):
        return
    user = await gClient.get_user(uid)
    charactersLeft = len(user.characters)
    characterIndex = 0
    embedTitle = "Your Characters:"

    while (charactersLeft > 0):
        embed = discord.Embed(title=embedTitle, color=13632027)

        for i in range(24):
            embed.add_field(
                name=user.characters[characterIndex].name,
                value="Level {} with {}".format(
                    user.characters[characterIndex].level,
                    user.characters[characterIndex].weapon.name))
            # manage indexes
            charactersLeft -= 1
            characterIndex += 1
            if (charactersLeft == 0):
                break
        # send embed
        await ctx.send(embed=embed)
        # change title in case of multiple embeds
        embedTitle = ""
    await logout()


# get diary
async def getDiary(ctx, usr):
    if (not await login(usr, ctx)):
        return
        
    diary = await gClient.get_diary()
    embed = discord.Embed(
        title="You have earned {} primogems this month.".format(
            diary.data.current_primogems),
        description=
        "========================================================",
        color=13632027)

    for category in diary.data.categories:
        embed.add_field(
            name="{} ({}%)".format(category.name, category.percentage),
            value="Gave you {} primogems".format(category.amount))
    await ctx.send(embed=embed)
    await logout()
