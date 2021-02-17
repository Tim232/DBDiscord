from discord.ext import commands

class TooLong(commands.CommandError):
    pass


class AlreadyExists(commands.CommandError):
    pass


class NotExists(commands.CommandError):
    pass
