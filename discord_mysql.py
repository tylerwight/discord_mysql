import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from random import randint
import mysql.connector

#dotenv to keep secrets out of public repo
load_dotenv()
sqluser = os.getenv('MYSQL_USER')
sqlpass = os.getenv('MYSQL_PASS')

#mysql auth
mydb = mysql.connector.connect(
        host = "localhost",
        user = sqluser,
        password = sqlpass,
        database = "discord"
)

cursor = mydb.cursor()

#====================
#discord auth
#===================
TOKEN = os.getenv('DISCORD_TOKEN')
#intents = discord.Intents(messages=True, guilds=True)
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!",intents=intents)


#commands to be executed via discord message
@bot.command(brief="add my account to the list")
async def add_me(ctx):
    await ctx.send(f'I am trying to add {ctx.author.name} to the DB')
    duplicate = 0
    cursor.execute("SELECT * FROM accounts")
    sql_out = []
    #check for duplicate user
    for x in cursor:
        for y in x:
            if str(ctx.author.id) in y:
                print("duplicate user found!")
                duplicate = duplicate + 1
    

    if (duplicate == 0):
        sql = "INSERT INTO accounts (account_id,name) VALUES (%s, %s)"
        val = (ctx.author.id, ctx.author.name)
        cursor.execute(sql, val)
        mydb.commit()
        print(cursor.rowcount, "was inserted")
        await ctx.send(f'I inserted {cursor.rowcount} rows using {ctx.author.id} and {ctx.author.name}')
    elif (duplicate == 1):
        await ctx.send(f'I found a duplicate so I did not add user to the DB')
    else:
        await ctx.send(f'I found more than one duplicate of the same user, trying to delete (not yet gotat code that part)')
        sql = "DELETE FROM accounts WHERE account_id = {} limit 1".format(ctx.author.id)
        cursor.execute(sql)
        mydb.commit()
        print(cursor.rowcount, "records deleted")
        await ctx.send(f'I deleted {cursor.rowcount} records with the id {ctx.author.id}')


@bot.command(brief="remove my account from the list")
async def del_me(ctx):
    await ctx.send(f'I am trying to delete {ctx.author.name} from the DB')
    cursor.execute("SELECT * FROM accounts")
    found = 0
    for x in cursor:
        for y in x:
            print("printing Y")
            print(y)
            if str(ctx.author.id) in y:
                found = found + 1
    print(f'I found {found} matches')

    if (found == 0):
        await ctx.send("I did not find you in the DB, skipping")
        return
    sql = "DELETE FROM accounts WHERE account_id = {} limit 1".format(ctx.author.id)
    cursor.execute(sql)
    mydb.commit()
    print(cursor.rowcount, "records deleted")
    await ctx.send(f'I deleted {cursor.rowcount} records with the id {ctx.author.id}')



bot.run(TOKEN)
