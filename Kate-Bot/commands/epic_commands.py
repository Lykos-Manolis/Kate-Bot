from epicstore_api import EpicGamesStoreAPI
from datetime import datetime
from replit.database import db


async def epicHandler(ctx):
    if (db["hasPostedEpic"] == False and datetime.today().weekday() == 3 and datetime.now().hour > 18):
        await getFreeGames(ctx)
        db["hasPostedEpic"] = True
    if (datetime.today().weekday() != 3 and db["hasPostedEpic"] == True):
        db["hasPostedEpic"] = False


async def getFreeGames(ctx):
    slugs = []
    api = EpicGamesStoreAPI()
    freeGames = api.get_free_games()
    elements = freeGames['data']['Catalog']['searchStore']['elements']

    
    for game in elements:
        if (game['promotions'] != None and len(game['promotions']['promotionalOffers']) > 0):
            try:
                slugs.append(game['catalogNs']['mappings'][0]['pageSlug'])
            except Exception as e:
                print(e)

    await ctx.send('--------------------------FREE EPIC GAMES----------------------------')
    for game in slugs:
        await ctx.send('https://store.epicgames.com/en-US/p/' + game)
    del slugs, api, freeGames, elements
