import discord

"""
Max Length Embed (6000)
embed=discord.Embed(title="0"*256,description="0"*2048)
embed.add_field(name="0"*256, value="0"*1024)
embed.add_field(name="0"*256, value="0"*1024)
embed.add_field(name="0"*256, value="0"*880)
"""


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
