#!/usr/bin/env python3
import requests
import os
import time
import sqlite3

def Get_Energy(Owner_ID,Max_E):

# get All horses

    horse_list_request = requests.get(f'https://api-apollo.pegaxy.io/v1/pegas/owner/user/{Owner_ID}')
######### Geting Date for Temp File ################

    Current_Unix_Time_H = int(time.time()/60/60)

    horses_list = (horse_list_request.json())

    Response = []                                                           # empty list to print

    for horse_id in horses_list:

####################Getting info from JAson File #################

        energy = horse_id['energy']

        totalRaces  =  horse_id['totalRaces']

        canRaceAt =  int(horse_id['canRaceAt']/60/60)

        Can_Race = canRaceAt - Current_Unix_Time_H

        if (energy >= Max_E) and (totalRaces > 0 ) and ( Can_Race < 0)  :
            Name= (horse_id['name'].encode(encoding="ascii",errors="ignore"))
            Decode = Name.decode("ascii")
            Response.append(f'''===================================================
Pega ID         : {horse_id['id']}
Name            : {Decode}
Wallet          : {Owner_ID}
Energy          : {horse_id['energy']}
scholar         : To Ping/Tag Scholars kindly get the Premium version
RenterAddress   : {horse_id['renterAddress']}
URL             : https://play.pegaxy.io/my-assets/pega/{horse_id['id']}
===================================================$''')
    return Response

def Check_Wallet(Schooler_W_ID):

    if (Schooler_W_ID[0] == '0') and (Schooler_W_ID[1] == 'x') and (len(Schooler_W_ID) == 42):

        Wallet = True

    else:

        Wallet = False

    return Wallet

def All_Guilds():

    sqliteConnection = sqlite3.connect('Free_BOT.DB')

    cursor = sqliteConnection.cursor()

    sqlite_select_query = (f"SELECT Guild_ID from Guilds")

    cursor.execute(sqlite_select_query)

    Result   =cursor.fetchall()

    Result_List = []

    for r in Result :

        Result_List.append(r[0])

    return Result_List

    if sqliteConnection:
        sqliteConnection.close()

def Wallet_Channel(Guild_ID,Channel_ID,Channel_Name,Wallet):

    sqliteConnection = sqlite3.connect('Free_BOT.DB')

    cursor = sqliteConnection.cursor()

    sqlite_Update = (f""" UPDATE Guilds SET
Channel_Name = '{Channel_Name}' ,
Channel_ID = '{Channel_ID}' ,
Wallet ='{Wallet}'
WHERE Guild_ID = '{Guild_ID}'  """)

    cursor.execute(sqlite_Update)

    sqliteConnection.commit()

    if sqliteConnection:
        sqliteConnection.close()

def Get_Info(Channel_ID):

    sqliteConnection = sqlite3.connect('Free_BOT.DB')

    cursor = sqliteConnection.cursor()

    get_info = (f"""SELECT Guild_ID,Wallet FROM Guilds where Channel_ID ='{Channel_ID}'  """)

    cursor.execute(get_info)

    Result   =cursor.fetchall()[0]

    if sqliteConnection:
        sqliteConnection.close()

    return Result

def loop():

    sqliteConnection = sqlite3.connect('Free_BOT.DB')

    cursor = sqliteConnection.cursor()

    sqlite_select_query = (f"SELECT Channel_ID,Wallet from Guilds")

    cursor.execute(sqlite_select_query)

    Result   =cursor.fetchall()

    return Result
