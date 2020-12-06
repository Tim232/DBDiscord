from discord.ext import commands
import discord

"""
Max Length Embed (6000)
embed=discord.Embed(title="0"*256,description="0"*2048)
embed.add_field(name="0"*256, value="0"*1024)
embed.add_field(name="0"*256, value="0"*1024)
embed.add_field(name="0"*256, value="0"*880)
"""


class TooLong(commands.CommandError):
    pass


class AlreadyExists(commands.CommandError):
    pass


class NotExists(commands.CommandError):
    pass


def str2embed(string: str):
    # 256, 2304, 2560, 3584, 3840, 4864, 5120, 6000

    strings = [
        (string[0:255], string[256:2303]),
        (string[2304:2559], string[2560:3583]),
        (string[3584:3839], string[3840:4863]),
        (string[4864:5119], string[5120:5999]),
    ]

    res = 0
    for ks, vs in strings:
        if ks == "":
            ks = "None"
        if vs == "":
            vs = "None"
        strings[res] = (ks, vs)
        res += 1

    embed = discord.Embed(title=strings[0][0], description=strings[0][1])

    for ks, vs in strings[1:]:
        embed.add_field(name=ks, value=vs)

    # embed=discord.Embed(title=string[0:255],description=string[256:2303])
    # embed.add_field(name=string[2304:2559], value=string[2560:3583])
    # embed.add_field(name=string[3584:3839], value=string[3840:4863])
    # embed.add_field(name=string[4864:5119], value=string[5120:5999])
    return embed


def embed2str(embed: discord.Embed):
    # 256, 2304, 2560, 3584, 3840, 4864, 5120, 6000

    string = (embed.title if embed.title != "None" else "") + (
        embed.description if embed.description != "None" else ""
    )

    for i in range(0, 3):
        name = embed.fields[i].name
        value = embed.fields[i].value
        if name == "None":
            name = ""
        if value == "None":
            value = ""
        string += name
        string += value

    return string


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