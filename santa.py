import discord
from discord.ext import commands

import sys
import math
import random

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='>', intents=intents)

class Santa:
    Name= ""
    give = -1
    receive = False

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

bot.run(str(sys.argv[1]))