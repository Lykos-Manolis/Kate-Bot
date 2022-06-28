import os
import discord
import asyncpraw
from replit.database import db

class RedditCrawler:
      
  unwantedFlairs = ['Megathread','Discussion']
  imageFormats = ['.jpg','.png','.jpeg','.gif']
      
  def __init__(self, subredditName, sort):
    self.subredditName = subredditName
    self.sort = sort
    self.foundSubmission = False
    self.login()
    
  def login(self):
    self.reddit = asyncpraw.Reddit(client_id = os.getenv('client_id'),
                      client_secret = os.getenv('client_secret'),
                      username = os.getenv('username'),
                      password = os.getenv('password'),
                      user_agent = os.getenv('user_agent'))
      
  async def crawlPost(self):
    subreddit = await self.reddit.subreddit(self.subredditName)
    if(self.sort == 'hot'):
      sortedPage = subreddit.hot(limit = 10)
    elif(self.sort == 'top'):
      sortedPage = subreddit.top(limit = 10, time_filter="month")
    
    async for submission in sortedPage:
      if (submission.link_flair_text not in self.unwantedFlairs) and any(format in submission.url for format in self.imageFormats) and (submission.id not in db["viewedPostIDs"]):
        self.foundSubmission = True
        self.post = submission
        db["viewedPostIDs"].append(submission.id)
        if len(db["viewedPostIDs"])>1000:
          db["viewedPostIDs"].pop(0)
        break
        
    await self.reddit.close()
  
  async def getPostUrl(self):
    return 'https://www.reddit.com'+self.post.permalink
  
  async def getPostTitle(self):
    return self.post.title
  
  async def getPostImage(self):
    return self.post.url



async def postGenshin(ctx, subredditName, sort='hot'):
  reactions = ['❤️‍🔥','😢','🥵','😆','🥺','🥶','😯','❓']
  subredditClient = RedditCrawler(subredditName, sort)
  await subredditClient.crawlPost()

  if(subredditClient.foundSubmission):
    try:
      postTitle = await subredditClient.getPostTitle()
      postImage = await subredditClient.getPostImage()
      postUrl = await subredditClient.getPostUrl()
      embed = discord.Embed(title=postTitle,url=postUrl)
      embed.set_image(url=postImage)
      message = await ctx.send(embed=embed)
      for reaction in reactions:
        await message.add_reaction(reaction)
    except Exception as ex:
      print('Reddit Crawler Exception:\n '+ex)
  del subredditClient