import discord,random,os,uuid
from dotenv import load_dotenv
import sqlite3 as sql
from discord.ext import commands,tasks
from discord.utils import get

class Ticket(commands.Cog):
    
    load_dotenv()
    GUILD_ID = os.getenv("GUILD_ID")
    
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def ticket(self,ctx):
        db = sql.connect("data.db")
        c = db.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS tickets(id INTEGER PRIMARY KEY,name TEXT,userid INTEGER,ticketid TEXT)")
        db.commit()
        c.execute("SELECT * FROM tickets WHERE userid = ?",(ctx.author.id,))
        user = c.fetchone()
        if user:
            await ctx.send("Its hard to tell you this but, you already have a ticket please be patient..!")
        else:
            id = str(uuid.uuid4())
            col = [random.randint(0,255) for i in range(0,3)]
            c.execute("INSERT INTO tickets (name,userid,ticketid) VALUES (?,?,?)",(ctx.author.name,ctx.author.id,id,))
            db.commit()
            devs = []
            devrole = get(ctx.guild.roles,id=612695545030639622)
            for i in ctx.guild.members:
                role = i.roles
                if "Administrator" in [roe.name for roe in role]:
                    devs.append(i)
            dev = random.choice(devs)
            card = discord.Embed(
            colour=discord.Colour.from_rgb(col[0],col[1],col[2]),
            title="Success!",
            description=f"Hello {ctx.author.mention}!, i see you have created a ticket now please be patient while we reach you!"
            )
            card.set_author(name=self.bot.user.name,icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=card)
            card1 = discord.Embed(
            colour=discord.Colour.from_rgb(col[0],col[1],col[2]),
            title="New Ticket!",
            description=f"New Ticket Created by **{ctx.author.name}**\nTicket ID: **{id}**\nUser ID: **{ctx.author.id}**"
            )
            card1.set_thumbnail(url=ctx.author.avatar_url_as(static_format='png'))
            await dev.send(embed=card1)
            
        db.close()

def setup(bot):
    bot.add_cog(Ticket(bot))