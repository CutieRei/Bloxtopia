import discord,os,random
from discord.ext import commands
from dotenv import load_dotenv
import sqlite3 as sql


load_dotenv()
TOKEN = os.getenv("TOKEN1")

bot = commands.Bot(command_prefix="!",help_command=None)

db = sql.connect("data.db")
c = db.cursor()
c.execute("SELECT id FROM mod")
users = c.fetchall()
modid = [i[0] for i in users]
db.close()

@bot.event
async def on_ready():
    print(f"{bot.user.name} has joined!")

@bot.check
async def checks(ctx):
    if ctx.author.id in modid:
        return True
    else:
        return False
    

@bot.command()
@commands.dm_only()
async def send(ctx,id:str,*,msg=None):
    db = sql.connect("data.db")
    c = db.cursor()
    c.execute("SELECT * FROM tickets WHERE ticketid = ?",(id,))
    db.commit()
    data = c.fetchone()
    user = bot.get_user(data[2])
    if msg == None:
        msg = f"Hello {user.name} the support team has reach out to you!\n\nHello iam {ctx.author.name} and i have responded to your ticket, if you have any question feel free to ask"
    if data:
        card = discord.Embed(
        colour=discord.Colour.from_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255)),
        title="Your Ticket Response"
        )
        card.set_footer(text=ctx.author.name,icon_url=ctx.author.avatar_url_as(static_format='png'))
        card.description = msg
        await user.send(embed=card)
        await ctx.send("Success!")
    elif data == None:
        await ctx.send("That User doesn't have any tickets!")
    else:
        pass
    db.close()

@bot.command()
@commands.dm_only()
async def solved(ctx,id:str,*,msg=None):
    devs = [716503311402008577]
    col = [random.randint(0,255) for i in range(0,3)]
    db = sql.connect("data.db")
    c = db.cursor()
    c.execute("SELECT * FROM tickets WHERE ticketid = ?",(id,))
    db.commit()
    user = c.fetchone()
    users = bot.get_user(user[2])
    if msg == None:
        msg = f"Hello {users.name} the support team has marked your Ticket as solved\nIf you're problem still continue, you may create another ticket\n\n_~~Best regard {ctx.author.name}_"
    if user:
        card = discord.Embed(
        colour = discord.Colour.from_rgb(col[0],col[1],col[2]),
        title="Ticket issue solved!",
        description=msg
        )
        card.add_field(name="Ticket info",value=f"Name: **{user[1]}**\nUserID: **{user[2]}**\nTicketID: **{user[3]}**")
        await users.send(embed=card)
        c.execute("DELETE FROM tickets WHERE userid = ?",(users.id,))
        db.commit()
        await ctx.send("Successfully solved ticket issue!")
    elif user == None:
        await ctx.send("That user doesn't have any tickets")
    else:
        pass
    db.close()

bot.run(TOKEN)