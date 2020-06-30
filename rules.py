import discord,json
from discord.ext import commands
from discord.ext.commands import Cog

class Rule(Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def rule(self,ctx,id:int=0):
        with open("rules.json","r") as f:
            data = json.load(f)
            if id == 1:
                await ctx.send(data.get("1"))
            elif id == 2:
                await ctx.send(data.get("2"))
            elif id == 3:
                await ctx.send(data.get("3"))
            elif id == 4:
                await ctx.send(data.get("4"))
            elif id == 5:
                await ctx.send(data.get("5"))
            elif id == 6:
                await ctx.send(data.get("6"))
            elif id == 7:
                await ctx.send(data.get("6"))
            else:
                card = discord.Embed(
                title="Rules",
                color=ctx.author.color
                )
                for key,val in data.items():
                    card.add_field(name=val[0:3],value=val[3:])
                await ctx.send(embed=card)

def setup(bot):
    print("Rules loaded")
    bot.add_cog(Rule(bot))