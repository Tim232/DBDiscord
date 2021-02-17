import discord

from exceptions import *
from converters import *

class DB:
    def __init__(self, category: discord.CategoryChannel, name: str):
        self.category: discord.CategoryChannel = category
        self.name: str = name.lower()
        self.db: discord.TextChannel = discord.utils.get(
            self.category.text_channels, name=self.name
        )

        if self.db is None:
            raise NotExists(
                f"The DB {self.name} does not exist in {self.category.name}."
            )

    async def save(self, string: str):
        if len(string) > 6000:
            raise TooLong("Input cannot be longer than 6000.")

        embed = str2embed(string)

        if self.db.topic is not None:
            mss = await self.db.fetch_message(int(self.db.topic))
            await mss.edit(embed=embed)
        else:
            msg = await self.db.send(embed=embed)
            await self.db.edit(topic=str(msg.id))
        return string  # or embed?

    async def load(self):
        msg = await self.db.fetch_message(int(self.db.topic))
        embed = msg.embeds[0]
        string = embed2str(embed)
        return string

    async def delete(self):
        await self.db.delete()
        return None


class Category:
    def __init__(self, server: discord.Guild, name: str):
        self.server: discord.Guild = server
        self.name: str = name.lower()
        self.category: discord.CategoryChannel = discord.utils.get(
            self.server.categories, name=self.name
        )

        if self.category is None:
            raise NotExists(f"The Category {self.name} does not exist.")

    async def create(self, name: str):
        name = name.lower()
        if name in [channel.name for channel in self.category.text_channels]:
            raise AlreadyExists(f"DB named {name} already exists in {self.name}.")
        await self.category.create_text_channel(name)

        return DB(self.category, name)

    async def delete(self):
        for cc2 in self.category.text_channels:
            await cc2.delete()
        await self.category.delete()
        return None

    async def getDB(self, name: str):
        return DB(self.category, name)

    async def getDBs(self):
        ccs = []
        for ca in self.category.text_channels:
            dd: DB = await self.getDB(ca.name)
            ccs.append(dd)
        return ccs
    
#        ccs = [await self.getDB(ca.name) for ca in self.category.text_channels]


class Server:
    def __init__(self, server: discord.Guild):
        self.server: discord.Guild = server

    async def create(self, name: str):
        name = name.lower()
        if name in [category.name for category in self.server.categories]:
            raise AlreadyExists(f"Category named {name} already exists.")
        await self.server.create_category(name)

        return Category(self.server, name)

    async def getCategory(self, name: str):
        return Category(self.server, name)

    async def getCategories(self):
        ccs = []
        for ca in self.server.categories:
            dd: Category = await self.getCategory(ca.name)
            ccs.append(dd)
        return ccs
