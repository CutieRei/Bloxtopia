import discord,random,os,asyncio
from discord.ext import commands,tasks
import sqlite3 as sql
from dotenv import load_dotenv


bot = commands.Bot(command_prefix=["?","!"])

load_dotenv()
TOKEN = os.getenv("TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
BOT_CMD = int(os.getenv("BOT_CMD"))

@bot.event
async def on_ready():
    print(f"{bot.user.name} has joined")

@bot.check
async def check(ctx):
    if ctx.channel.id != BOT_CMD and "Administrator" in [i.name for i in ctx.author.roles]:
        return True
    elif ctx.channel.id != BOT_CMD and "Administrator" not in [i.name for i in ctx.author.roles]:
        return False
    else:
        return True
@bot.command()
async def test(ctx):
    await ctx.send("Hello this is a test")

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.CheckFailure):
        await ctx.send("🚫You cannot use commands on this channel!🚫",delete_after=2)
        asyncio.sleep(1)
        await ctx.message.delete