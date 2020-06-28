import discord
from discord.ext import commands
import sqlite3 as sql


class Mod(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot
    
    
    @commands.command()
    #@commands.has_any_role("Administrator","Developer")
    async def add(self,ctx,member:discord.Member):
        db = sql.connect("data.db")
        c = db.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS mod(name TEXT,id INTEGER)")
        db.commit()
        uRole = [i.name for i in member.roles]
        if "Administrator" in uRole:
            c.execute("SELECT * FROM mod WHERE name = ?",(member.name,))
            db.commit()
            user = c.fetchone()
            if user:
                await ctx.send("Uhmm he/she already registered?")
            else:
                c.execute("INSERT INTO mod VALUES (?,?)",(member.name,member.id,))
                db.commit()
                await ctx.send("Successfully added Member!")
        else:
            await ctx.send("What?")
        db.close()


def setup(bot):
    print("Loaded")
    bot.add_cog(Mod(bot))