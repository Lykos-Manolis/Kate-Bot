import os
from replit.database import db
import requests
from bs4 import BeautifulSoup
import discord

async def postPins(ctx, boardName):
  baseUrl = "https://gr.pinterest.com"
  user = os.environ['pinUser']
  boardContainerClass = "vbI XiG"
  images = []
  urls = []
  
  page = requests.get(baseUrl+user+boardName)
  soup = BeautifulSoup(page.content, "html.parser")
  
  pins = soup.find("div", class_=boardContainerClass).find_all("a")
  
  for pin in pins:
      image = pin.find('img')
      if(image!=None and image['src'] not in db["usedImages"] and "236x" in image['src']):
        db["usedImages"].append(image['src'])
        images.append(image['src'].replace("236x","736x"))
        urls.append(baseUrl+pin['href'])
          
  if len(images)>0:
    for i in range(len(images)):
      embed = discord.Embed(title="Image Link", colour=discord.Colour(0xd71782), url=urls[i])
      embed.set_image(url=images[i])
      await ctx.send(embed=embed)

  del images
  del urls
  page.close()
  return