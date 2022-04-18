#!/usr/bin/env python3
##########Custom################
from utils import Get_Energy , Check_Wallet , All_Guilds , Wallet_Channel, Get_Info , loop
from VAR import *
#########Python3#################
import os
import re
import sqlite3
###########Discord###############
import discord
from discord.ext import commands, tasks
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option , create_choice

# Create Arguments

Max_E = 24


#####################Slash command intodcution############################

#intents = discord.Intents.default()

#intents.members = True

#client = commands.Bot(command_prefix='!',intents=intents)

client = commands.Bot(command_prefix='!',activity = discord.Game(name="/help to start"))

slash = SlashCommand(client , sync_commands=True)

######################Just on ready##############################
######################Just on ready##############################

@client.event
async def on_ready():
    #change_status.start()
    print('bot in active')

#####################################################

#@slash.slash(name = 'Energy' , description="Check the Energy Manually" , guild_ids=[GUILD_ID])   #   >>>> Add to Var file

@slash.slash(name = 'energy' , description="Run the command to set the channel for Automatic reminder and to specify your wallet")
async def Energy(ctx:SlashContext):
################Variabls for Bot ###################
    Channel_ID               = ctx.channel.id
    channel                  = client.get_channel(Channel_ID)
    Channel_Name             = ctx.channel.name
##############################Actual schdualer ##################################              #   >>>> Add to Var file


    await channel.send('''```Checking Pegas above 24 Energy```''')
    await channel.send('''This is a Free version of Pegato Energy bot .
Premium Bot will run every hour to check for energy and ping/tag scholar if the energy is above a predefined value.
Please join us at our discord server for more Details : https://pegato.io/pegaxy-bot-premium''')

    try:
        MSG_Info = Get_Info(Channel_ID)
    except Exception as e:

        print(e)

        await channel.send('''```Energy Command Failed ,
Please make sure you have already configured the bot and you are using the designated channel   ```''')
        return
    else:

        Guild_ID = MSG_Info[0]
        Owner_ID = MSG_Info[1]

    Response = []

    Response.append(Get_Energy(Owner_ID,Max_E))                                    # Removing Empty list in list of lists

    Response= [x for x in Response if x] # Removing Empty list in list of lists

    if Response:
        await ctx.defer()
        for Pega in Response:

            for i in Pega:

                i=re.sub(r'\\n|(\\.)|\,', lambda match: match.group(1) or '\n', repr(i))

                i= i.replace('\'',"").replace('[',"").replace(']',"")

                print(i)

                await channel.send(i)
        await ctx.send('Bot is Running')
    else:
        await channel.send(f'''```bash
=======================
ALL Scholers are working Hard , All pegas are below "24" Energy
=======================```''')

        await ctx.send('Bot is Running')

@slash.slash(name = 'Help' , description="Help Command to Get Started" )
async def Help(ctx):

    Masseg_ID = ctx.channel.id
    channel = client.get_channel(Masseg_ID)                                        #   >>>> Add to Var file                                      #   >>>> Add to Var file
                                                          #   >>>> Add to Var file

    if ctx.author == client.user:
        return

    await channel.send(f'''```bash
Welcome to Pegato Energy Bot :)
Bot has to be configured First in order to run .
You will have to run /configure to provide the channel and Wallet address.
Pegato Energy Bot will automatically check 2 times per day for pegas those have more than 24 energy. Premium version will check every hour.

Command List :-

 1 - "/configure"                     : Command will set the Designated channel for scheduled and manual checks , it will also Set the Wallet for the owner.
 2 - "/energy"                        : Energy Command will trigger the energy check manually.
```''')
    await ctx.send (f'''**Bot is Running**''')

@client.event
async def on_guild_join(guild):

    sqliteConnection = sqlite3.connect('Free_BOT.DB')

    cursor = sqliteConnection.cursor()

    sqlite_Guild_Join = (f""" INSERT INTO Guilds (Guild_Name, Guild_ID)
VALUES('{guild.name}','{guild.id}')""")

    cursor.execute(sqlite_Guild_Join)

    sqliteConnection.commit()

    cursor.close()

    print(f'''Guild Name : {guild.name}
Guild ID  : {guild.id}
''')


@client.event
async def on_guild_remove(guild):

    sqliteConnection = sqlite3.connect('Free_BOT.DB')

    cursor = sqliteConnection.cursor()

    sqlite_Guild_leave = (f""" DELETE FROM  Guilds WHERE Guild_ID = '{guild.id}' """)

    cursor.execute(sqlite_Guild_leave)

    sqliteConnection.commit()

    cursor.close()

    print(f'''Guild Name : {guild.name}
Guild ID  : {guild.id}
''')


@slash.slash(name = 'Configure' , description="Run the command to set the channel for Automatic reminder and to specify your wallet" ,
    options=[create_option(name='option1',description='Add your Polygon Wallet', option_type= 3 ,required = True)   ] )

async def Configure(ctx, option1):
    ################Variabls for Bot ###################
    Guild_ID                 = ctx.guild.id
    Channel_ID               = ctx.channel.id
    channel                  = client.get_channel(Channel_ID)
    Channel_Name             = ctx.channel.name
    Wallet                   = str(option1)
    Wallet_True              = Check_Wallet(Wallet)
##############################Actual schdualer ##################################
    if Wallet_True == False :
        await channel.send('''```Please enter a Valid polygon Wallet Address```''')
        await ctx.send (f'''**Bot is Running**''')
        return                        # Finsining MAssage

    Wallet_Channel(Guild_ID,Channel_ID,Channel_Name,Wallet)

    await channel.send(f'''```bash
Registration was successful
Designated Channel : "{Channel_Name}"
Wallet Address     : "{Wallet}"```''')

    await ctx.send (f'''**Bot is Running**''')

@tasks.loop(hours=12)

async def change_status():

    All_guilds = loop()

    for guild in All_guilds:

        Channel_ID = guild[0]
        channel    = client.get_channel(int(Channel_ID))
        Owner_ID   = guild[1]

        Response = []

        Response.append(Get_Energy(Owner_ID,Max_E))                                    # Removing Empty list in list of lists

        Response= [x for x in Response if x] # Removing Empty list in list of lists

        if Response:

            for Pega in Response:

                for i in Pega:

                    i=re.sub(r'\\n|(\\.)|\,', lambda match: match.group(1) or '\n', repr(i))

                    i= i.replace('\'',"").replace('[',"").replace(']',"").replace('"',"")

                    print(i)

                    await channel.send(i)

        else:
            await channel.send(f'''=======================
    ALL Scholers are working Hard , All pegas are below 24 Energy
    Keep it up guys :D
    ======= ================''')

    await ctx.send (f'''**Bot is Running**''')

client.run(TOKEN)                                                                               #  >>>>>>>>>>> Add to Var File
