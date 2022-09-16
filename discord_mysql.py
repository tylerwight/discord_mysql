import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from random import randint
import mysql.connector

load_dotenv()
sqluser = os.getenv('MYSQL_USER')
sqlpass = os.getenv('MYSQL_PASS')

mydb = mysql.connector.connect(
        host = "localhost",
        user = sqluser,
        password = sqlpass,
        database = "discord"
)

cursor = mydb.cursor()
tables = []

cursor.execute("SELECT DATABASE()")
for x in cursor:
    db = x
cursor.execute("SHOW TABLES")
for x in cursor:
    tables.append(x)
#strdb = ''
#strdb = db[0]
#strtables = ''
#strtables = tables[0]
print(type(db))
db = ''.join(db)
tables = ''.join(''.join(tup) for tup in tables)
print(type(db))
print(type(tables))
print(db)
print(tables)
#print(tables)


TOKEN = os.getenv('DISCORD_TOKEN')

#intents = discord.Intents(messages=True, guilds=True)
intents = discord.Intents.all()


client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!",intents=intents)


@bot.command(brief="add my account to the list")
async def add_me(ctx):
    await ctx.send(f'I am trying to add {ctx.author.name} to the DB')
    sql = "INSERT INTO accounts (account_id,name) VALUES (%s, %s)"
    print(ctx.author.id)
    print(ctx.author.name)
    print(type(ctx.author.id))
    print(type(ctx.author.name))
    val = (ctx.author.id, ctx.author.name)
    cursor.execute(sql, val)
    mydb.commit()
    print(cursor.rowcount, "was inserted")

# print all servers bot is connected to on startup, just for reference
#@client.event
#async def on_ready():
#    print(f'{client.user} has connected to Discord!')
#    for guild in client.guilds:
#        print(f'{guild}')


#@client.event
#async def on_message(message):
#    if message.author == client.user: return
#    if message.author.bot: return
#    channel = client.get_channel(message.channel.id) # get channel id from message and use it to create channel object
#    print (f'{channel}, {message.channel}')  # print some variables for debug
#    textSearch = "mysql"
#    if message.content.find(textSearch) != -1: # serach message for anywhere
#        print( f'{message.content}\n') # print the mesage that triggered our
        #data = cursor.execute("show databases")
#        await channel.send('I am attached to the database: ' + db + "I can see tables: " + tables)


bot.run(TOKEN)
#client.run(TOKEN)
