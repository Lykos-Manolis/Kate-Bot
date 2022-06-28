from crawlers.steam_crawler import steamClient
from crawlers.anime_crawler import animeClient

async def ReactionHandler(reaction,user,client):
    if(hasattr(steamClient, 'message') and reaction.message.id == steamClient.message.id):
        if(user.id != client.user.id):
          if reaction.emoji == "▶":
            steamClient.itemIndex += 1
            await reaction.remove(user)
            await steamClient.getSale()
          elif reaction.emoji == "◀":
            steamClient.itemIndex -= 1
            await reaction.remove(user)
            await steamClient.getSale()
          elif reaction.emoji == "⏸":
            steamClient.itemIndex = 0
            await steamClient.message.delete()
    elif(hasattr(animeClient, 'message') and reaction.message.id == animeClient.message.id):
        if(user.id != client.user.id):
          if reaction.emoji == "▶":
            animeClient.itemIndex += 1
            await reaction.remove(user)
            await animeClient.getAnime()
          elif reaction.emoji == "◀":
            animeClient.itemIndex -= 1
            await reaction.remove(user)
            await animeClient.getAnime()
          elif reaction.emoji == "⏸":
            animeClient.itemIndex = 0
            await animeClient.message.delete()