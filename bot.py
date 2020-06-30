import discord,random
from discord.ext import commands
import sqlite3 as sql
from typing import Optional
from discord import Colour,Embed

TOKEN = ""
with open("token.txt","r") as f:
    TOKEN = f.read()

async def set_prefix(bot,msg):
    userid = bot.user.id
    pre = ["///"]
    with sql.connect("data.db") as db:
        c = db.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS prefix(guild INTEGER,pre TEXT DEFAULT '-')")
        c.execute("SELECT pre FROM prefix WHERE guild = ?",(msg.guild.id,))
        gPre = c.fetchone()
        if gPre is None:
            pre.append("-")
        else:
            pre.append(gPre[0])
        return pre
ext = ["rules"]

bot = commands.Bot(command_prefix=set_prefix,case_insensitive=True)
bot.ready = False

for i in ext:
    bot.load_extension(i)


@bot.event
async def on_command_error(ctx,error):
    col = [random.randint(0,255) for i in range(0,3)]
    card = Embed(
    colour=Colour.from_rgb(col[0],col[1],col[2]),
    title="An error occurred"
    )
    if isinstance(error, commands.CommandNotFound):
        card.add_field(name="Invalid commmand invoked!",value=f"Command **_{ctx.invoked_with}_** not found!")
        await ctx.send(embed=card)
    elif isinstance(error,commands.MissingPermissions):
        card.add_field(name="Missing permission!",value=f"you meed to have **{','.join(error.missing_perms)}** permission, to do that")
        await ctx.send(embed=card)
    else:
        raise error

@bot.command(hidden=True)
async def meow(ctx):
  await ctx.send("Meow meow!")

@bot.command(aliases=["n1ck"],hidden=True)
async def nick(ctx):
  await ctx.send("Developer here!")
  
@bot.command(aliases=["purge"],hidden=False)
@commands.has_permissions(manage_messages=True)
async def clear(ctx,count: Optional[int] = 1):
    """
    Purge the current TextChannel should not be more than 1000 messages deleted
    """
    print("Yay executed")
    col = [random.randint(0,255) for i in range(0,3)]
    if count > 1000:
        count = 1000
    deleted = await ctx.channel.purge(limit=count)
    card = Embed(
    colour=Colour.from_rgb(col[0],col[1],col[2]),
    title=f"Cleared {len(deleted)} messages"
    )
    await ctx.send(embed=card,delete_after=3)

@bot.event
async def on_ready():
    if bot.ready == False:
        bot.ready = True
        print("Bot is ready!")
    else:
        print("Bot is ready again!")

@bot.event
async def on_connect():
    print("Connected!")

@bot.event
async def on_disconnect():
    print("Bot Disconnected")

@bot.command()
async def dc(ctx):
    """
    Disconnect the bot this happened often by ReyterGTX(Bot Owner)
    """
    isowner = await bot.is_owner(ctx.author)
    if isowner:
        await ctx.send("Disconnected!")
        await bot.logout()
    else:
        await ctx.send("You are who?")

@bot.command()
async def prefix(ctx,new: Optional [str]="-"):
    """
    This still Unstable as it can make the guild have no prefix default to '-' if not set
    """
    with sql.connect("data.db") as db:
        c = db.cursor()
        c.execute("SELECT * FROM prefix WHERE guild = ?",(ctx.guild.id,))
        gPre = c.fetchone()
        if len(new) > 5:
            await ctx.send("prefix should not be > 5 char long!")
        elif gPre == None:
            c.execute("INSERT INTO prefix VALUES (?,?)",(ctx.guild.id,new,))
            await ctx.send("New prefix added!")
        else:
            if gPre[0] == new:
                await ctx.send("That seems familiar.....")
            else:
                c.execute("UPDATE prefix SET guild = ?,pre = ? WHERE guild = ?",(ctx.guild.id,new,ctx.guild.id,))
                await ctx.send("Updated Prefix!")

bot.run(TOKEN)