import discord
from discord.ext import commands

from datetime import datetime, timedelta

import sys
import math
import random
from asyncio import sleep
import subprocess

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='>', intents=intents)
intTime = datetime(2015, 2, 1, 15, 16, 17, 345)
bot.lastFight = intTime
bot.spite = True

class Santa:
    Name= ""
    give = -1
    receive = False

@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return
    server = member.guild
    disconnects = 0
    if ((datetime.utcnow() - bot.lastFight)/timedelta(minutes = 1)) <= 5:
        #print("On cooldown")
        return
        
    else:
        entries = []
        async for entry in server.audit_logs(limit=3, action = discord.AuditLogAction.member_disconnect):
            if (datetime.utcnow() - entry.created_at)/timedelta(minutes = 1) != 1:
                #print("Adding an entry")
                entries.append(entry)
                disconnects += entry.extra.count

        #Last disconnect fight was more than 3 minutes ago
        if disconnects >= 3:
            if before.channel != None:
                channel = before.channel
            elif after.channel != None:
                channel = after.channel
            bot.lastFight = datetime.utcnow()
            await wcwbf(channel)
    
async def wcwbf (channel):
    voice_channel = channel
    channel = None
    if voice_channel != None:
        channel = voice_channel.name
        vc = await voice_channel.connect()
        song = discord.FFmpegOpusAudio(source="wcwbf.mp3")
        print(song.is_opus())
        vc.play(song)
        while vc.is_playing():
            await sleep(1)
        await vc.disconnect()

def checkDone(santas):
    count = 0
    last = -1
    for x, i in enumerate(santas):
        if(i.receive == False):
            last = x
            count +=1
    if count == 1 and (santas[last].give == -1 and santas[last].receive == False):
        reset(santas)
        return False
    elif count >= 1:
        return False
    else:
        return True

def reset(santas):
    print("RESETTING")
    for i in santas:
        i.give = -1
        i.receive = False
    return


@bot.event
async def on_ready():
    print("Bot is ready to bot it up")

@bot.event
async def on_message(message):
    if message.author.id == 193508802073460736 and message.content == '-skip' and bot.spite:
        await message.author.move_to(None)
        await message.channel.send("Stop skipping tracks bitch")

    await bot.process_commands(message)

@bot.command(pass_context = True)
async def spite(ctx):
    if bot.spite and server.owner.name == ctx.author.name:
        bot.spite = False
        ctx.author.send("Kempke is no longer being spited")
    elif not bot.spite and server.owner.name == ctx.author.name:
        bot.spite = True
        ctx.author.send("Kempke is now being spited")

@bot.command(pass_context=True)  
async def santa(ctx, *args):
    server = ctx.guild
    channel = ctx.channel
    if(server.owner.name == ctx.author.name):
        role_name =(' '.join(args))
        role_id = server.roles[0]
        for role in server.roles:
            if role_name.lower() == role.name.lower():
                role_id = role
                break

        else:
            await channel.send(f"{role_name} Role does not exist")
            return

        members = role_id.members
        names = []
        
        for member in members:
            names.append(member.name)


        santas = [Santa() for i in range(len(names))]
        for i in range(0, len(santas)):
            santas[i].Name = names[i]

        while(not checkDone(santas)):
            giver = random.randint(0, len(santas)-1)                #Pick a random person to give a gift
            if(santas[giver].give != -1):                           #Check if that person is already giving a gift
                continue
            receiver = random.randint(0, len(santas)-1)           #Pick a random person to receive a gift
            while(santas[receiver].receive == True or receiver == giver):
                receiver = random.randint(0, len(santas)-1)
            santas[receiver].receive = True
            santas[giver].give = receiver

        for x, i in enumerate(santas):
            await members[x].send(f"You will be giving a gift to {santas[i.give].Name}\nThe rules and information for this year along with the addresses of everyone will be in a pinned file in the {server.name} server")

            #print("Giver: " + santas[giver].Name + " Receiver: " + santas[receiver].Name)
        
    else:
        await channel.send("Only the owner can roll for secret santa")
    #await members[0].send("test")
    #await channel.send(f"Users in {role_id}, {santas}")

bot.run(str(sys.argv[1]), bot=True)
