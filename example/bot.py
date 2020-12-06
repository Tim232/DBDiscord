from discord.ext import commands

import DBDiscord

bot = commands.Bot(command_prefix="!!")

@bot.event
async def on_ready():
    print("SDF")
    discordserver = bot.get_guild(720561442429338282) # A Empty Server with no categories and textchannels
    bot.handler = DBDiscord.Server(discordserver) # A DB Server that has categories and DBs. It looks like Server>Category>DB .

@bot.command()
async def categories(ctx):
    cbs = await bot.handler.getCategories()
    await ctx.send(cbs)

@bot.command()
async def dbs(ctx, name):
    c = await bot.handler.getCategory(name)
    dbs = await c.getDBs()
    await ctx.send(dbs)

@bot.command()
async def createcategory(ctx, name):
    await bot.handler.create(name)

@bot.command()
async def deleteategory(ctx, name):
    c = await bot.handler.getCategory(name)
    await c.delete()

@bot.command()
async def createdb(ctx, ca, name):
    c = await bot.handler.getCategory(ca)
    await c.create(name)

@bot.command()
async def deletedb(ctx, ca, name):
    c = await bot.handler.getCategory(ca)
    d = await c.getDB(name)
    await d.delete()

@bot.command()
async def savedb(ctx, ca, db, *, thing):
    c = await bot.handler.getCategory(ca)
    d = await c.getDB(db)
    await d.save(thing)

@bot.command()
async def loaddb(ctx, ca, db):
    c = await bot.handler.getCategory(ca)
    d = await c.getDB(db)
    t = await d.load()
    await ctx.send(t)

@bot.event
async def on_command_error(ctx, err):
    if isinstance(err, DBDiscord.NotExists):
        return await ctx.send(err)
    elif isinstance(err, DBDiscord.AlreadyExists):
        return await ctx.send(err)
    raise err


bot.run('token')