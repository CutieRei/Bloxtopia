import discord
from discord.ext import commands
from discord import Colour,Embed


def syntax(cmd):
    alias="|".join(cmd.aliases)
    

class HelpCommand(commands.HelpCommand):
    
    def __init__(self):
        super().__init__(command_att{
        "help":"show help for the bot commands"
        })
    
    @commands.command(aliases=["halp","guide"])
    async def help(self,ctx):
        card = Embed(
        title="Help",
        colour=ctx.author.color
        )
        for i in self.command