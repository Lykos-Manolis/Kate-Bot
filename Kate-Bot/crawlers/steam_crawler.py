import requests
from bs4 import BeautifulSoup


class SteamCrawler:
    itemIndex = 0
    reactions = ['◀', '▶', '⏸']

    def __init__(self):
        self.resetVariables()

# SET SALE ITEMS

    async def setSales(self, ctx, itemAmount):
        self.message = await ctx.send("Retrieving sales..")
        self.maxItems = itemAmount
        self.resetVariables()

        # get site data
        URL = "https://store.steampowered.com/search/?filter=topsellers&specials=1"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        itemContainer = soup.find(id="search_resultsRows")
        items = itemContainer.find_all('a')

        # handle invalid input
        if (self.maxItems <= 0 or self.maxItems > len(items)):
            self.maxItems = len(items)

    # store contents
        for itemIndex in range(self.maxItems):
            self.names.append(items[itemIndex].find('span', class_='title'))
            self.links.append(items[itemIndex])
            self.pictures.append(items[itemIndex].find('img'))
            self.discounts.append(items[itemIndex].find(
                'div', class_='col search_discount responsive_secondrow').text.
                                  strip())
            prices = items[itemIndex].find(
                'div',
                class_='col search_price discounted responsive_secondrow')
            originalPrice = prices.find('span').text.strip()
            discountedPrice = prices.text.replace(originalPrice, '').strip()
            self.initial_costs.append(originalPrice)
            self.discounted_costs.append(discountedPrice)

# GET STEAM SALES

    async def getSale(self):
        # check loop
        if (self.itemIndex >= self.maxItems):
            self.itemIndex = 0
        elif (self.itemIndex < 0):
            self.itemIndex = self.maxItems - 1

    # get embed link
        try:
            itemLink = self.links[self.itemIndex]['href']
        except Exception as ex:
            print('Steam Crawler Exception in getSale() :\n ' + ex)

    # create embed
        await self.message.edit(content=itemLink)

        # add reactions
        for r in self.reactions:
            await self.message.add_reaction(r)

# SEARCH STEAM TITLES

    async def Search(self, ctx, searchKeywords):
        self.resetVariables()
        self.message = await ctx.send("Searching..")

        # get site
        URL = "https://store.steampowered.com/search/?term=" + searchKeywords
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        itemContainer = soup.find(id="search_resultsRows")

        # in case no data is found
        if (itemContainer == None):
            await self.message.edit(content='No results..')
            return

    # get site data
        item = itemContainer.find('a')
        self.links.append(item)

        # get embed link
        try:
            itemLink = self.links[0]['href']
        except Exception as ex:
            print('Steam Crawler Exception in Search() :\n ' + ex)

    # create embed
        await self.message.edit(content=itemLink)

# EMPTY OBJECT VARIABLES

    def resetVariables(self):
        self.names = []
        self.links = []
        self.pictures = []
        self.discounts = []
        self.initial_costs = []
        self.discounted_costs = []
        self.itemIndex = 0

steamClient = SteamCrawler()
