import requests
import discord
from bs4 import BeautifulSoup

class AnimeCrawler:
    itemIndex = 0
    reactions = ['◀','▶','⏸']
    
    def __init__(self):
        self.resetVariables()
          
    # SET ANIME 
    async def setAnime(self, ctx, keyWord):
        self.message = await ctx.send("Getting anime..")
        self.resetVariables()

        # get site data
        URL = "https://gogoanime.fi"
        searchURLext = "//search.html?keyword="
        page = requests.get(URL+searchURLext+keyWord)
        soup = BeautifulSoup(page.content, "html.parser")
        items = soup.find('ul',class_='items')

        # store items
        names_Urls = items.find_all('p',class_='name')
        pictures = items.find_all('div',class_='img')
      
        # store names, urls pics
        for anime in names_Urls:
            self.names.append(anime.find('a')['title'])
            self.links.append(URL+(anime.find('a')['href']))
        for animePic in pictures:
            self.pictures.append(animePic.find('a').find('img')['src'])   
            
              
    # GET ANIME  
    async def getAnime(self):
        # in case there are no results
        if(not self.names):
            await self.message.edit(content='No results..')
            return
          
        # remove dub anime
        for anime in reversed(range(len(self.names))):
            if '(Dub)' in self.names[anime]:
                self.names.pop(anime)
                self.links.pop(anime)
                self.pictures.pop(anime)    
               
        # get length of items 
        self.maxItems = len(self.names)
      
        # check loop
        if(self.itemIndex >= self.maxItems):
          self.itemIndex = 0
        elif(self.itemIndex < 0):
          self.itemIndex = self.maxItems-1
          
        # get embed values
        try:
            animeTitle = self.names[self.itemIndex]
            animeLink = self.links[self.itemIndex]
            animeImage = self.pictures[self.itemIndex]
        except Exception as ex:
            print(ex)
            
        # create embed
        embed = discord.Embed(title='{}. {}'.format(self.itemIndex+1,animeTitle), colour=discord.Colour(0xffb3), url=animeLink)
        embed.set_image(url=animeImage)
        await self.message.edit(content='{} items to show'.format(self.maxItems),embed=embed)
      
      # add reactions
        for r in self.reactions:
            await self.message.add_reaction(r)
          
    # EMPTY OBJECT VARIABLES        
    def resetVariables(self):
        self.names = []
        self.links = []
        self.pictures = []
        
animeClient = AnimeCrawler()