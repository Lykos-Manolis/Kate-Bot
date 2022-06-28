from crawlers.steam_crawler import steamClient
from commands.discord_commands import ClearMessages
              
async def GetSales(ctx,amount):
    await ClearMessages(ctx,0)
    await steamClient.setSales(ctx,amount)
    await steamClient.getSale()

async def SteamSearch(ctx,searchKeywords):
    await ClearMessages(ctx,0)
    await steamClient.Search(ctx, searchKeywords)